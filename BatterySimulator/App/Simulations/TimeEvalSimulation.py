from App.Simulations.BaseSimulation import BaseSimulation

class TimeEvalSimulation(BaseSimulation):
    def run(self, t_eval):
        """
        Run a simulation over a specified time period.
        
        Parameters:
        - t_eval: List of time points over which the simulation will be evaluated.
        """
        return self.run_simulation(t_eval=t_eval)
