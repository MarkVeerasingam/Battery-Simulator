# SimulationRunner.py
from App.BatteryModel.BatteryModel import BatteryModel
from App.ElectrochemicalModel.ElectrochemicalModel import ElectrochemicalModel
from App.Solver.Solver import ConfigSolver
from App.Simulation import TimeEvaluationSimulation, ExperimentSimulation

class SimulationRunner:
    def __init__(self):
        self._electrochemical_params = {"electrochemical_model": "DFN"}
        self._battery_params = {"battery_model": "LFP"}
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

        self._config_battery_model = BatteryModel.create_from_config(self._battery_params["battery_model"])
        self._config_electrochemical_model = ElectrochemicalModel.create_from_config(self._electrochemical_params["electrochemical_model"])
        self._config_solver = ConfigSolver.create_from_config(**self._solver_params)

    @property
    def electrochemical_params(self):
        return self.electrochemical_params
    
    @electrochemical_params.setter
    def electrochemical_params(self, electrochemical_config):
        if "electrochemical_model" in electrochemical_config:
            # Create a new instance of ElectrochemicalModel 
            new_electrochemical_model = ElectrochemicalModel.create_from_config(electrochemical_config["electrochemical_model"])
            self._config_electrochemical_model = new_electrochemical_model 
        self._electrochemical_params.update(electrochemical_config)

    @property
    def battery_params(self):
        return self._battery_params

    @battery_params.setter
    def battery_params(self, model_config):
        if "battery_model" in model_config:
            # Create a new instance of BatteryModel 
            new_battery_model = BatteryModel.create_from_config(model_config["battery_model"])
            self._config_battery_model = new_battery_model
        self._battery_params.update(model_config)

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