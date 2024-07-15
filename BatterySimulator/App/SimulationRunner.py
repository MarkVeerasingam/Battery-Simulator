# SimulationRunner.py
from App.BatteryModel import BatteryModel
from App.ElectrochemicalModel import ElectrochemicalModel
from App.Solver import ConfigSolver
from App.Simulation import TimeEvaluationSimulation, ExperimentSimulation

class SimulationRunner:
    def __init__(self):
        self._model_params = {"bpx_model": "LFP", "electrochemical_model": "DFN"}
        self._solver_params = {"solver": "CasadiSolver", "atol": 1e-6, "rtol": 1e-6}

        self._t_eval = [0, 3700]
        self._experiment = [
            (
                "Discharge at C/5 for 10 hours or until 2.5 V",
                "Rest for 1 hour",
                "Charge at 1 A until 3.5 V",
                "Hold at 3.5 V until 10 mA",
                "Rest for 1 hour",
            ),
        ] * 2

        self._config_battery_model = BatteryModel.create_from_config(self._model_params["bpx_model"])
        self._config_electrochemical_model = ElectrochemicalModel.create_from_config(self._model_params["electrochemical_model"])
        self._config_solver = ConfigSolver.create_from_config(**self._solver_params)

    @property
    def model_params(self):
        return self._model_params

    @model_params.setter
    def model_params(self, model_config):
        self._model_params.update(model_config)
        self._config_battery_model.update_model(bpx_model=self._model_params["bpx_model"])
        self._config_electrochemical_model.update_model(electrochemical_model=self._model_params["electrochemical_model"])

    @property
    def solver_params(self):
        return self._solver_params

    @solver_params.setter
    def solver_params(self, solver_config):
        self._solver_params.update(solver_config)
        self._config_solver.update_solver(**self._solver_params)

    @property
    def experiment(self):
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment
    
    @property
    def t_eval(self):
        return self._t_eval

    @t_eval.setter
    def t_eval(self, t_eval):
        self._t_eval = t_eval

    def run_time_evaluation_simulation(self):
        simulation = TimeEvaluationSimulation(
            config_battery_model=self._config_battery_model,
            config_electrochemical_model=self._config_electrochemical_model,
            config_solver=self._config_solver,
            t_eval=self._t_eval
        )
        simulation.simulate()

    def run_experiment_simulation(self):
        simulation = ExperimentSimulation(
            config_battery_model=self._config_battery_model,
            config_electrochemical_model=self._config_electrochemical_model,
            config_solver=self._config_solver,
            experiment=self._experiment
        )
        simulation.simulate()