import pybamm

class BaseSimulation:
    def __init__(self, model, parameter_values, solver):
        """ This class handles common logic between simulation types."""
        self.model = model
        self.parameter_values = parameter_values
        self.solver = solver

    def run_simulation(self, t_eval=None, experiment=None):
        """Run a PyBaMM simulation based on provided t_eval or experiment."""
        sim = pybamm.Simulation(
            model=self.model,
            parameter_values=self.parameter_values,
            solver=self.solver,
            experiment=experiment
        )
        return sim.solve(t_eval)