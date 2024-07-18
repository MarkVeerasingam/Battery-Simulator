from App.CreateBatteryModel.Config import Configuration
from App.Simulation import Simulation

class SimulationRunner:
    def __init__(self, config: Configuration):
        self.simulation = Simulation(config)
        self.t_eval = None
        self.experiment = None

    def set_t_eval(self, t_eval):
        self.t_eval = t_eval

    def set_experiment(self, experiment):
        self.experiment = experiment

    def run_simulation(self):
        return self.simulation.run(t_eval=self.t_eval, experiment=self.experiment)