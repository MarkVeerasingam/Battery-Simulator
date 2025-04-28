from celery import Celery, shared_task
from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest, ParameterizedECMRequest
from config.Utils.logger import setup_logger
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import numpy as np
import pybamm
import redis
import json

load_dotenv()
logger = setup_logger(__name__)

REDIS_URL = 'redis://redis:6379/0'

# using celeray for a distrubted systems and async simulations. the broker most likely will be rabbitMQ or kafka with a backend of redis
# Initialize a Celery instance with a Redis broker and backend
celery = Celery(
    'tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.update(
    accept_content=['json'],  
    result_serializer='json', 
    task_serializer='json'     
)   

def publish_to_simulation_results_queue(payload):
    try:
        # Connect to Redis
        r = redis.StrictRedis.from_url(REDIS_URL)

        # Publish the payload (results) to a Redis channel/queue
        r.publish('simulation_results', json.dumps(payload))  

    except Exception as e:
        logger.error(f"Failed to publish message to RabbitMQ: {str(e)}")
        raise

@celery.task()
def run_physics_simulation(simulation_request):
    try:
        # celery expects a dictionary that contains all necessary parameters
        # Deserialize the request_dict into the DTO 
        # I'm doing this because Pydantic enforces type safety and remains consistent with the whole simulation process.
        # will at some stage do a check for the header types for the request
        request = Physics_SimulationRequest(**simulation_request)

        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params) # result is in dict, where {time(s):{output_variables}}

        payload = {
            "task_id": request.task_id,
            "status": "success",
            "results": results,            
        }

        # response = requests.post(WEBHOOK_URL, json=payload)
        # logger.info(f"Webhook response: {response.status_code}, {response.text}")

        publish_to_simulation_results_queue(payload)

        return results
    except Exception as e:
        error_message = f"simulation failed: {str(e)}"
        logger.error(error_message)
        
        payload = {
            "task_id": request.task_id,
            "status": "success",
            "results": results,            
        }
        
        # response = requests.post(WEBHOOK_URL, json=payload)
        # logger.info(f"Webhook failure notification response: {response.status_code}, {response.text}")

        publish_to_simulation_results_queue(payload)

        raise

@celery.task()
def run_ecm_simulation(simulation_request):
    try:
        logger.info(f"Received message: {simulation_request}")
        
        request = ECM_SimulationRequest(**simulation_request)

        parameter_value_config = request.parameter_values
        equivalent_circuit_model_config = request.equivalent_circuit_model
        solver_config = request.solver
        simulation_config = request.simulation

        sim_runner = ECM_SimulationRunner(
            parameter_value_config=parameter_value_config,
            solver_config=solver_config,
            ecm_config=equivalent_circuit_model_config,
        )
        sim_runner.run_simulation(simulation_config)

        display_params = request.display_params or ["Voltage [V]", "Current [A]", "Jig temperature [K]"]
        results = sim_runner.display_results(display_params)
                
        payload = {
            "task_id": request.task_id,
            "status": "success",
            "results": results,            
        }

        # response = requests.post(WEBHOOK_URL, json=payload)
        # logger.info(f"Webhook response: {response.status_code}, {response.text}")

        publish_to_simulation_results_queue(payload)

        return results
    except Exception as e:
        error_message = f"simulation failed: {str(e)}"
        logger.error(error_message)

        payload = {
            "task_id": simulation_request.get("task_id"),
            "status": "failure",
            "error": error_message,
        }

        # response = requests.post(WEBHOOK_URL, json=payload)
        # logger.info(f"Webhook failure notification response: {response.status_code}, {response.text}")

        publish_to_simulation_results_queue(payload)

        raise

@celery.task()
def run_parameterized_ecm_simulation(simulation_request):
    try:
        # Extract task parameters
        request = ParameterizedECMRequest(**simulation_request)
        
        # MongoDB client setup
        client = MongoClient("mongodb://mongodb:27017/")
        db = client["BatteryData"]
        collection = db["ECM_LUT"]

        battery_label = request.battery_label
        cycle_number = request.cycle_number

        # Load data from MongoDB
        mongo_query = {"battery_label": battery_label, "cycle": cycle_number}
        document = collection.find_one(mongo_query)

        if not document:
            raise ValueError(f"No data found for battery {battery_label}, cycle {cycle_number}")

        # Convert MongoDB document data to DataFrame
        loaded_data = pd.DataFrame(document["data"])
        loaded_data = loaded_data.drop_duplicates(subset=['SoC'], keep='first')
        loaded_data = loaded_data.sort_values('SoC')

        # Extract parameters
        soc_values = np.array(loaded_data["SoC"])
        voltage_values = np.array(loaded_data["voltage"])
        R0_values = np.array(loaded_data["r0"])
        R1_values = np.array(loaded_data["r1"])
        C1_values = np.array(loaded_data["c1"])
        R2_values = np.array(loaded_data["r2"])
        C2_values = np.array(loaded_data["c2"])

        # Create interpolation functions for parameters
        def ocv(soc):
            return pybamm.Interpolant(soc_values, voltage_values, soc, name="OCV", interpolator="linear", extrapolate=True)

        def r0(soc):
            return pybamm.Interpolant(soc_values, R0_values, soc, name="R0", interpolator="linear", extrapolate=True)

        def r1(soc):
            return pybamm.Interpolant(soc_values, R1_values, soc, name="R1", interpolator="linear", extrapolate=True)

        def c1(soc):
            return pybamm.Interpolant(soc_values, C1_values, soc, name="C1", interpolator="linear", extrapolate=True)

        def r2(soc):
            return pybamm.Interpolant(soc_values, R2_values, soc, name="R2", interpolator="linear", extrapolate=True)

        def c2(soc):
            return pybamm.Interpolant(soc_values, C2_values, soc, name="C2", interpolator="linear", extrapolate=True)

        # Pass the interpolators to the model runner
        parameter_values = pybamm.ParameterValues("ECM_Example")
        updated_data = {
            "Open-circuit voltage [V]": ocv,
            "R0 [Ohm]": r0,
            "R1 [Ohm]": r1,
            "C1 [F]": c1,
            "R2 [Ohm]": r2,
            "C2 [F]": c2,
            "Element-1 initial overpotential [V]": 0,
            "Element-2 initial overpotential [V]": 0,
            "Initial SoC": 1.0,
        }
        parameter_values.update(updated_data, check_already_exists=False)

        # Initialize the ECM simulation runner
        sim_runner = ECM_SimulationRunner(
            parameter_value_config=request.parameter_values,
            solver_config=request.solver,
            ecm_config=request.equivalent_circuit_model
        )
        
        # Run the simulation
        sim_runner.run_simulation(config=request.simulation)

        # Get the results
        results = sim_runner.display_results(request.display_params or ["Voltage [V]", "Current [A]"])

        # Prepare the result payload
        payload = {
            "task_id": request.task_id,
            "status": "success",
            "results": results,
        }

        publish_to_simulation_results_queue(payload)

        return results

    except Exception as e:
        error_message = f"simulation failed: {str(e)}"
        logger.error(error_message)

        payload = {
            "task_id": simulation_request.get("task_id"),
            "status": "failure",
            "error": error_message,
        }

        publish_to_simulation_results_queue(payload)
        raise