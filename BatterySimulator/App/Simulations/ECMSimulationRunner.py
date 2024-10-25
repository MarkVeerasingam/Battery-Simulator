from App.BatteryModel.ModelRunner import ModelRunner
from App.ParameterValues.ParameterValuesRunner import ParameterValuesRunner
from App.Solvers.SolverRunner import SolverRunner
from App.Simulations.SimulationTypes import DriveCycleSimulation, ExperimentSimulation, TimeEvalSimulation
from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from typing import List

class SimulationRunner:
    def __init__(self, parameter_value_config: ParameterValueConfiguration, solver_config: SolverConfiguration, 
                 ecm_config: ECMConfiguration):
        """
        Initialize the SimulationRunner by creating the battery model components.

        Parameters:
        - battery_config: The configuration for the parameter values of the model (parameter_values, optional BPX).
        - solver_config: The configuration for the solver (type, tolerance).
        - electrochemical_config: The configuration for the electrochemical model (thermal, geometry).
        """
        self.equivalent_circuit_model = ModelRunner.create_ecm(ecm_config)
        self.parameter_values = ParameterValuesRunner.create_ecm(config=parameter_value_config, ecm_config=ecm_config)
        self.solver = SolverRunner.create(solver_config)

        # stores simulation results
        self.results = None
        
    # sepearting out for easier seperation of conern, physics based and ecm primary simulation runnder handlers should be seperated as this is what handles the heavy compute 
    def run_simulation(self, config: SimulationConfiguration):
        """
        Run the simulation based on the provided configuration.
        
        Parameters:
        - config: The configuration for the simulation (experiment, t_eval, drive cycle).
        """
        
        if config.drive_cycle:
            drive_cycle_sim = DriveCycleSimulation(self.equivalent_circuit_model, self.parameter_values, self.solver)
            run_sim = drive_cycle_sim.run(config.drive_cycle) 
            self.results = run_sim  
        elif config.experiment:
            experiment_sim = ExperimentSimulation(self.equivalent_circuit_model, self.parameter_values, self.solver)
            run_sim = experiment_sim.run(config.experiment)  
            self.results = run_sim 
        elif config.t_eval:
            time_eval_sim = TimeEvalSimulation(self.equivalent_circuit_model, self.parameter_values, self.solver)
            run_sim = time_eval_sim.run(config.t_eval)  
            self.results = run_sim 
        else:
            raise ValueError("No valid simulation configuration provided.")

    def display_results(self, selected_params: List[str]):
        """
        Legacy Code: This will be replaced with argument output_variables and output_variables will contain values of list[str] variables

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
        