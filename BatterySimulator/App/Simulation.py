import pybamm
from App.CreateBatteryModel.Config import BatteryConfiguration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver

class Simulation:
    def __init__(self, config: BatteryConfiguration):
        self.electrochemical_model = ElectrochemicalModel.create(config.electrochemical_model)
        self.battery_model = BatteryModel.create(config.battery_chemistry)

        atol = config.tolerance.get("atol", 1e-6)
        rtol = config.tolerance.get("rtol", 1e-6)

        self.solver = Solver.create(config.solver, atol, rtol)

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

        sim.plot()
        
        return solution