from App.Simulations.SimulationRunner import SimulationRunner
from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest

class SimulationService:
    @staticmethod
    def run_physics_simulation(request: Physics_SimulationRequest):
        battery_config = request.parameter_values
        electrochemical_config = request.electrochemical_model
        solver_config = request.solver_model
        simulation_config = request.simulation

        sim_runner = SimulationRunner(battery_config, solver_config, electrochemical_config)
        sim_runner.run_simulation(config=simulation_config)

        display_params = request.display_params or ["Terminal voltage [V]"]
        results = sim_runner.display_results(display_params)

        return results

    @staticmethod
    def run_ecm_simulation(request: ECM_SimulationRequest):
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