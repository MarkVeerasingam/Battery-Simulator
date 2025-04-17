from celery import Celery, shared_task
from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
from config.Utils.logger import setup_logger
from dotenv import load_dotenv
import redis
import json

load_dotenv()
logger = setup_logger(__name__)

WEBHOOK_URL = 'http://simulationNotificationService:8082/notification'
# RABBITMQ_URL = os.getenv('RABBITMQ_URL')
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

@shared_task() 
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
