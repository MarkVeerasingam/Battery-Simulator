from App.Simulations.SimulationTypes.BaseSimulation import BaseSimulation

class ExperimentSimulation(BaseSimulation):
    def run(self, experiment):
        return self.run_simulation(experiment=experiment)