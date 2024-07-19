from App.CreateBatteryModel.Config import Configuration
from App.Simulation import Simulation

class SimulationRunner:
    def __init__(self, config: Configuration):
        self.simulation = Simulation(config)
        self.t_eval = None
        self.experiment = None
        self.drive_cycle = None

    def set_t_eval(self, t_eval):
        self.t_eval = t_eval

    def set_experiment(self, experiment):
        self.experiment = experiment

    def set_drive_cycle(self, drive_cycle):
        self.drive_cycle = drive_cycle

    def run_simulation(self):
        return self.simulation.run(t_eval=self.t_eval, experiment=self.experiment, drive_cycle=self.drive_cycle)