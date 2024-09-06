import pandas as pd
import pybamm
import json
from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration, ElectrochemicalConfiguration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES

class Simulation:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration, electrochemical_config: ElectrochemicalConfiguration):
        self.battery_config = battery_config
        self.solver_config = solver_config
        self.electrochemical_model = electrochemical_config

        # Create the electrochemical model, battery model, and solver model
        self.electrochemical_model = ElectrochemicalModel.create(electrochemical_config)
        self.battery_model = BatteryModel.create(battery_config)
        self.solver = Solver.create(solver_config)

        # To store results
        self.results = None

    # Separate function for running time_eval simulations
    def run_time_eval(self, t_eval):
        sim = pybamm.Simulation(
            model=self.electrochemical_model,
            parameter_values=self.battery_model,
            solver=self.solver
        )
        # Solve the simulation over the time evaluation period
        solution = sim.solve(t_eval)
        self.results = solution
        return solution

    # Separate function for running experiment-based simulations
    def run_experiment(self, experiment):
        sim = pybamm.Simulation(
            model=self.electrochemical_model,
            parameter_values=self.battery_model,
            solver=self.solver,
            experiment=experiment
        )
        # Solve the simulation based on the experiment conditions
        solution = sim.solve()
        self.results = solution
        return solution

    # Run drive cycle
    def run_driveCycle(self, driveCycle: DriveCycleFile, temperature: float = 25.0):
        # Same as before
        self.electrochemical_model.events = []

        selected_driveCycle = next((dc for dc in AVAILABLE_DRIVE_CYCLES if dc.name == driveCycle.drive_cycle_file), None)
        if selected_driveCycle is None:
            raise ValueError(f"Invalid drive cycle name: {driveCycle.drive_cycle_file}.")
        
        file_path = selected_driveCycle.path
        if not file_path:
            raise ValueError("Drive cycle file path is empty")

        data = pd.read_csv(file_path, comment="#").to_numpy()
        time_data = data[:, 0]
        current_data = data[:, 1]

        current_interpolant = pybamm.Interpolant(time_data, -current_data, pybamm.t, interpolator="linear")
        self.battery_model.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        sol = self.run_time_eval(t_eval=None)
        return sol

    # Main function to execute simulation based on configuration
    def execute_simulation(self, config: SimulationConfiguration):
        if config.drive_cycle:
            return self.run_driveCycle(driveCycle=config.drive_cycle)
        elif config.experiment:
            return self.run_experiment(experiment=config.experiment)
        elif config.t_eval:
            return self.run_time_eval(t_eval=config.t_eval)
        else:
            raise ValueError("No valid simulation configuration provided.")
