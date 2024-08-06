from config.Config import BatteryConfiguration, SolverConfiguration, SimulationConfiguration
from App.Simulation import Simulation
from typing import List

class SimulationRunner:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration):
        self.simulation = Simulation(battery_config=battery_config, solver_config=solver_config)
    
    def run_simulation(self, config: SimulationConfiguration):
        return self.simulation.execute_simulation(config)

    def display_results(self, selected_params: List[str]):
        # Check if the simulation results are available
        if self.simulation.results is None:
            print("No results to display. Run the simulation first.")
            return

        results = {}

        time_s = self.simulation.results["Time [s]"].entries

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

        for i, current_time in enumerate(time_s):
            time_label = f"Time(s): {current_time}"
            results[time_label] = {}
            for param in selected_params:
                try:
                    data = self.simulation.results[param].entries
                    results[time_label][param] = data[i]
                except KeyError:
                    results[time_label][param] = None  # Parameter wasnt found

        for time, params in results.items():
            print(f"\nTime: {time} s")
            for param, value in params.items():
                print(f"{param}: {value}")

        # return results as a dict
        return results 

    