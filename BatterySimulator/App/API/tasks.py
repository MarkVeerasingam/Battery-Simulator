from celery import Celery
from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
from config.Utils.logger import setup_logger
import requests

logger = setup_logger(__name__)

# using celeray for a distrubted systems and async simulations. the broker most likely will be rabbitMQ or kafka with a backend of redis
# Initialize a Celery instance with a Redis broker and backend
celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.update(
    accept_content=['json'],  
    result_serializer='json', 
    task_serializer='json'     
)

webhook_url = 'http://localhost:8084/simulate/webhook'

@celery.task(bind=True) 
def run_physics_simulation(self, request_dict):
    try:
        # celery expects a dictionary that contains all necessary parameters
        # Deserialize the request_dict into the DTO 
        # I'm doing this because Pydantic enforces type safety and remains consistent with the whole simulation process.
        # will at some stage do a check for the header types for the request
        request = Physics_SimulationRequest(**request_dict)

        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]

        results = sim_runner.display_results(display_params)
        
        requests.post(webhook_url, json={"task_id": self.request.id, "result": results})

        return results
    except Exception as e:
        logger.error(f"Physics simulation failed: {str(e)}")
        requests.post(webhook_url, json={"task_id": self.request.id, "error": str(e)})

@celery.task(bind=True) 
def run_ecm_simulation(self, request_dict):
    try:
        request = ECM_SimulationRequest(**request_dict)

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

        requests.post(webhook_url, json={"task_id": self.request.id, "result": results})

        return results
    except Exception as e:
            logger.error(f"Physics simulation failed: {str(e)}")
            requests.post(webhook_url, json={"task_id": self.request.id, "error": str(e)})
