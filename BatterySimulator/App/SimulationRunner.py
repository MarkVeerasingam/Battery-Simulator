from App.Model import ConfigModel
from App.Solver import ConfigSolver
from App.Simulation import TimeEvaluationSimulation, ExperimentSimulation

class SimulationRunner():
    model_config = {"bpx_model": "LFP", "electrochemical_model": "DFN"}
    config_solver = {"solver": "CasadiSolver", "atol": 1e-6, "rtol": 1e-6}

    t_eval = [0, 3700]
    experiment =[
                    (
                        "Discharge at C/5 for 10 hours or until 2.5 V",
                        "Rest for 1 hour",
                        "Charge at 1 A until 3.5 V",
                        "Hold at 3.5 V until 10 mA",
                        "Rest for 1 hour",
                    ),
                ]*2

    config_model = ConfigModel.create_from_config(**model_config)
    config_solver = ConfigSolver.create_from_config(**config_solver)

    simulation = TimeEvaluationSimulation(config_model=config_model,
                                        config_solver=config_solver,
                                        t_eval=t_eval)
    # simulation = ExperimentSimulation(config_model=config_model,
    #                                     config_solver=config_solver,
    #                                     experiment=experiment)
    simulation.simulate()

if __name__ == "__main__":
    SimulationRunner()