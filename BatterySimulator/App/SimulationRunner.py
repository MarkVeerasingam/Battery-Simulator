from App.CreateBatteryModel.Config import BatteryConfiguration
from App.Simulation import Simulation
from App.DriveCycleSimulation import DriveCycleSimulation

class SimulationRunner:
    def __init__(self, config: BatteryConfiguration):
        self.config = config
        self.simulation = Simulation(config)
        self.experiment = None
        self.t_eval = None

    def set_t_eval(self, t_eval):
        self.t_eval = t_eval

    def set_experiment(self, experiment):
        self.experiment = experiment

    def set_drive_cycle(self, drive_cycle):
        self.drive_cycle = drive_cycle

    def run_simulation(self):
        if self.experiment:
            return self.simulation.run(t_eval=self.t_eval, experiment=self.experiment)
        elif self.drive_cycle:
            drive_cycle_simulation = DriveCycleSimulation(self.simulation)
            temperature = 25  # Example temperature in °C
            filename = self.drive_cycle
            return drive_cycle_simulation.solve(temperature=temperature, filename=filename)
        else:
            raise ValueError("No experiment or drive cycle set.")
