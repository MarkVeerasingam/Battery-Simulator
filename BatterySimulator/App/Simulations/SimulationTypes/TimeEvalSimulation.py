from App.Simulations.SimulationTypes.BaseSimulation import BaseSimulation

class TimeEvalSimulation(BaseSimulation):
    def run(self, t_eval):
        return self.run_simulation(t_eval=t_eval)
