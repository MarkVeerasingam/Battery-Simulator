import pybamm
from App.CreateBatteryModel.Config import Configuration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver

class Simulation:
    def __init__(self, config: Configuration):
        self.electrochemical_model = ElectrochemicalModel.create(config.electrochemical_model)
        self.battery_model = BatteryModel.create(config.battery_model)
        self.solver = Solver.create(config.solver, config.atol, config.rtol)

    def run(self, t_eval=None, experiment=None):
        # Create simulation object
        sim = pybamm.Simulation(
            model=self.electrochemical_model,
            parameter_values=self.battery_model,
            solver=self.solver,
            experiment=experiment
        )
        
        # Solve the simulation
        if t_eval is not None:
            solution = sim.solve(t_eval)
        else:
            solution = sim.solve()

        # sim.plot()
        
        return solution