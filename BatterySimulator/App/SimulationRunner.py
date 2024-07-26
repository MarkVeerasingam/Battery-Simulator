from config.Config import BatteryConfiguration, SolverConfiguration, SimulationConfiguration
from App.Simulation import Simulation
from typing import List

class SimulationRunner:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration):
        self.simulation = Simulation(battery_config=battery_config, solver_config=solver_config)
    
    def run_simulation(self, config: SimulationConfiguration):
        return self.simulation.execute_simulation(config)

    def display_results(self, selected_params: List[str]):
        if self.simulation.results is None:
            print("No results to display. Run the simulation first.")
            return

        # Access the data from the solution
        for param in selected_params:
            try:
                # Access the data using the parameter names as keys
                data = self.simulation.results[param].entries
                print(f"\nData for {param}:")
                print(data)
            except KeyError:
                print(f"\nParameter '{param}' not found in the simulation results.")