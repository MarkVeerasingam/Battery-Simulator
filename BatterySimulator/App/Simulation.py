import pandas as pd
import pybamm
from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES

class Simulation:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration):
        # create the electrochemical model to be used in the simulation
        self.electrochemical_model = ElectrochemicalModel.create(battery_config)
        
        # create the battery model to be used in the simulation
        self.battery_model = BatteryModel.create(battery_config)
        
        # create the solver to be used in the simulation
        self.solver = Solver.create(solver_config)

    # run the simulation
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
    
    def run_driveCycle(self, driveCycle: DriveCycleFile, temperature: float = 25.0, title=""):
        # Access and modify the electrochemical model to disable events
        self.electrochemical_model.events = []
        
        # Load drive cycle data from driveCycleLibrary 
        if driveCycle.chemistry not in AVAILABLE_DRIVE_CYCLES:
            raise ValueError(f"Invalid battery chemistry: {driveCycle.chemistry}. Use one of {list(AVAILABLE_DRIVE_CYCLES.keys())}")
        
        available_driveCycle = AVAILABLE_DRIVE_CYCLES[driveCycle.chemistry].driveCycle
        driveCycle = next((dc for dc in available_driveCycle if dc.name == driveCycle.drive_cycle_file), None)

        if driveCycle is None:
            raise ValueError(f"Invalid drive cycle name: {driveCycle.drive_cycle_file}. Available cycles: {[dc.name for dc in available_driveCycle]}")

        file_path =  driveCycle.path
        print(f"Loading data from: {file_path}")
        
        data = pd.read_csv(file_path, comment="#").to_numpy()
        print(f"Data loaded. Shape: {data.shape}")

        # This will only work for the exisint data provided from A:E BXP Models.
        # to take in a file with current and voltage, this would break. - need to make a parser or smth..?

        # Extract time, current, and voltage data
        time_data = data[:, 0]
        current_data = data[:, 1]
        voltage_data = data[:, 2]

        # Create current interpolant
        current_interpolant = pybamm.Interpolant(
            time_data, -current_data, pybamm.t, interpolator="linear"
        )

        # Update battery model parameters
        self.battery_model.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        # Run simulation
        sol = self.run()
        
        return sol
    
    def execute_simulation(self, config: SimulationConfiguration):
        if config.drive_cycle:
            return self.run_driveCycle(driveCycle=config.drive_cycle)
        elif config.experiment:
            return self.run(experiment=config.experiment)
        elif config.t_eval:
            return self.run(t_eval=config.t_eval)
        else:
            raise ValueError("No valid simulation configuration provided.")