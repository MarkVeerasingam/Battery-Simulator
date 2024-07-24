from config.Config import BatteryConfiguration, SolverConfiguration, SimulationConfiguration
from App.Simulation import Simulation

class SimulationRunner:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration):
        self.simulation = Simulation(battery_config=battery_config, solver_config=solver_config)
    
    def run_simulation(self, config: SimulationConfiguration):
        return self.simulation.execute_simulation(config)
