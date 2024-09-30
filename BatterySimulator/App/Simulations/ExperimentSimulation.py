import pybamm
from App.Simulations.BaseSimulation import BaseSimulation

class ExperimentSimulation(BaseSimulation):
    def run(self, experiment):
        return self.run_simulation(experiment=experiment)