from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.ParameterValues import ParameterValues
from App.CreateBatteryModel.Solver import Solver
from App.Simulations.ExperimentSimulation import ExperimentSimulation
from App.Simulations.TimeEvalSimulation import TimeEvalSimulation
from config.Config import BatteryConfiguration, SolverConfiguration, SimulationConfiguration, ElectrochemicalConfiguration
from typing import List

class SimulationRunner:
    def __init__(self, battery_config, solver_config, electrochemical_config):
            """
            Initialize the SimulationRunner by creating the battery model components.

            Parameters:
            - battery_config: The configuration for the battery model (parameters, chemistry).
            - solver_config: The configuration for the solver (type, tolerance).
            - electrochemical_config: The configuration for the electrochemical model (thermal, geometry).
            """
            # Create the electrochemical model
            self.electrochemical_model = ElectrochemicalModel.create(electrochemical_config)

            # Create the parameter values (either BPX or built-in pybamm sets)
            self.parameter_values = ParameterValues.create(battery_config)

            # Create the solver (CasadiSolver, IDAKLUSolver, etc.)
            self.solver = Solver.create(solver_config)    

    def run_simulation(self, config):
        """
        Run the simulation based on the provided configuration.
        
        Parameters:
        - config: The configuration for the simulation (experiment, t_eval, drive cycle).
        """
        if config.experiment:
            experiment_simulation = ExperimentSimulation(
                electrochemical_model=self.electrochemical_model,
                parameter_values=self.parameter_values,
                solver=self.solver
            )
            return experiment_simulation.run(experiment=config.experiment)

        elif config.t_eval:
            time_eval_simulation = TimeEvalSimulation(
                electrochemical_model=self.electrochemical_model,
                parameter_values=self.parameter_values,
                solver=self.solver
            )
            return time_eval_simulation.run(t_eval=config.t_eval)
        
        # do drive cycle simulation logic next
        
        else:
            raise ValueError("Invalid simulation type provided.")

    def display_results(self, selected_params: List[str]):
        """
        this is the idea of how i want to display the results of parameters based on a rapid protoype form a jupyter notebook.
        
        solution = simulation.solve([0,3600]) # not exclusive to only time_eval, can work with any

        selected_parameters = ['Voltage [V]', 'Current [A]', 'Battery open-circuit voltage [V]', 'Discharge capacity [A.h]']

        for param in selected_parameters:
                try:
                    # Access the data using the parameter names as keys
                    data = solution[param]
                    print(f"\nData for {param}:")
                    print(data.entries)
                except KeyError:
                    print(f"\nParameter '{param}' not found in the simulation results.")
        """

        if self.results is None:
            print("No results to display. Please run the simulation first.")
            return

        results = {}
        time_s = self.results["Time [s]"].entries

        for i, current_time in enumerate(time_s):
            time_label = f"{current_time}s"
            results[time_label] = {}
            for param in selected_params:
                try:
                    data = self.results[param].entries
                    results[time_label][param] = data[i]
                except KeyError:
                    results[time_label][param] = None
                    print(f"Warning: Parameter '{param}' not found in the simulation results.")

        for time, params in results.items():
            print(f"\nTime: {time} s")
            for param, value in params.items():
                print(f"{param}: {value}")

        return results
