from celery import Celery
from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
import pybamm
import logging

pybamm.set_logging_level("INFO")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class SimulationService:
    @staticmethod
    def register_tasks():
        celery.tasks.register(SimulationService.run_physics_simulation)
        celery.tasks.register(SimulationService.run_ecm_simulation)
        logger.info("Registered tasks: %s", celery.tasks.keys())

    @celery.task
    def run_physics_simulation(request: Physics_SimulationRequest):
        # request = Physics_SimulationRequest(**request_dict)

        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params)

        return results

    @celery.task
    def run_ecm_simulation(request: ECM_SimulationRequest):
        # request = ECM_SimulationRequest(**request_dict)

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

        return results

SimulationService.register_tasks()