import pandas as pd
from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration, ElectrochemicalConfiguration
from App.CreateBatteryModel.ParameterValues import ParameterValues
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES


class SimulationService:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration,
                 electrochemical_model: ElectrochemicalModel, parameter_values: ParameterValues,
                 solver: Solver):

        self.battery_config = battery_config
        self.solver_config = solver_config
        self.electrochemical_model = electrochemical_model
        self.parameter_values = parameter_values
        self.solver = solver

    def execute_simulation(self, config: SimulationConfiguration):
        """
        Main function to execute the appropriate simulation based on the configuration.
        Delegates to the appropriate simulation class.
        """
        if config.drive_cycle:
            drive_cycle_sim = DriveCycleSimulation(self.electrochemical_model, self.parameter_values, self.solver)
            return drive_cycle_sim.run(config.drive_cycle)
        elif config.experiment:
            experiment_sim = ExperimentSimulation(self.electrochemical_model, self.parameter_values, self.solver)
            return experiment_sim.run(config.experiment)
        elif config.t_eval:
            time_eval_sim = TimeEvaluationSimulation(self.electrochemical_model, self.parameter_values, self.solver)
            return time_eval_sim.run(config.t_eval)
        else:
            raise ValueError("No valid simulation configuration provided.")
