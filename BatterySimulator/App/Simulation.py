import pybamm
from pydantic import BaseModel
from App.BatteryModel.BatteryModel import BatteryModel
from App.ElectrochemicalModel.ElectrochemicalModel import ElectrochemicalModel
from App.Solver.Solver import ConfigSolver

class BaseSimulation(BaseModel):
    config_battery_model: BatteryModel
    config_electrochemical_model: ElectrochemicalModel
    config_solver: ConfigSolver

    def construct_simulation_model(self):
        electrochemical_model = self.config_electrochemical_model.set_electrochemical_model()
        battery_model = self.config_battery_model.set_bpx_model()
        solver = self.config_solver.set_solver()

        simulation_model = {
            "electrochemical_model": electrochemical_model,
            "battery_model": battery_model,
            "solver": solver
        }
        return simulation_model

class TimeEvaluationSimulation(BaseSimulation):
    t_eval: list

    def simulate(self):
        simulation_model = self.construct_simulation_model()

        sim = pybamm.Simulation(model=simulation_model["electrochemical_model"],
                                parameter_values=simulation_model["battery_model"],
                                solver=simulation_model["solver"])
        
        sim.solve(self.t_eval)
        self.results = sim.solution # store output results of simulation
        sim.plot()
        return self.results

class ExperimentSimulation(BaseSimulation):
    experiment: list

    def simulate(self):
        simulation_model = self.construct_simulation_model()

        sim = pybamm.Simulation(model=simulation_model["electrochemical_model"],
                                parameter_values=simulation_model["battery_model"],
                                solver=simulation_model["solver"],
                                experiment=self.experiment)
        
        sim.solve()
        sim.plot()
