from App.Model import ConfigModel
from App.Solver import ConfigSolver
from App.Simulation import TimeEvaluationSimulation, ExperimentSimulation

class SimulationRunner:
    def __init__(self):
        self.model_params = {"bpx_model": "LFP", "electrochemical_model": "DFN"}
        self.solver_params = {"solver": "CasadiSolver", "atol": 1e-6, "rtol": 1e-6}

        self.t_eval = [0, 3700]
        self.experiment = [
            (
                "Discharge at C/5 for 10 hours or until 2.5 V",
                "Rest for 1 hour",
                "Charge at 1 A until 3.5 V",
                "Hold at 3.5 V until 10 mA",
                "Rest for 1 hour",
            ),
        ] * 2

        self.config_model = ConfigModel.create_from_config(**self.model_params)
        self.config_solver = ConfigSolver.create_from_config(**self.solver_params)

    def set_model_config(self, model_config):
        self.model_params.update(model_config)
        self.config_model = ConfigModel.create_from_config(**self.model_params)

    def set_solver_config(self, solver_config):
        self.solver_params.update(solver_config)
        self.config_solver = ConfigSolver.create_from_config(**self.solver_params)

    def set_experiment(self, experiment):
        self.experiment = experiment

    def get_experiment(self):
        return self.experiment
    
    def set_time_eval(self, t_eval):
        self.t_eval = t_eval

    def get_time_eval(self):
        return self.t_eval

    def run_time_evaluation_simulation(self):
        simulation = TimeEvaluationSimulation(
            config_model=self.config_model,
            config_solver=self.config_solver,
            t_eval=self.t_eval
        )
        simulation.simulate()

    def run_experiment_simulation(self):
        simulation = ExperimentSimulation(
            config_model=self.config_model,
            config_solver=self.config_solver,
            experiment=self.experiment
        )
        simulation.simulate()
