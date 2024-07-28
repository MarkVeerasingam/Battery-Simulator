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

        # Access the data from the solution
        for param in selected_params:
            try:
                # Access the data using the parameter names as keys
                # self.results = Solution in Simulation.py, we need to access this to get the entries of the simulation's output data
                data = self.simulation.results[param].entries
                # Convert numpy array to list for JSON serialization
                results[param] = data.tolist()  
                print(f"\nData for {param}:")
                print(data)
            except KeyError:
                print(f"\nParameter '{param}' not found in the simulation results.")
                results[param] = f"Parameter '{param}' not found in the simulation results."
        
        # return results as a dictionary
        return results 

    