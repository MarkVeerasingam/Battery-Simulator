import pandas as pd
import pybamm
import json
from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES
from libraries.CellLibrary import AVAILABLE_BATTERY_MODELS

class Simulation:
    def __init__(self, battery_config: BatteryConfiguration, solver_config: SolverConfiguration):
        self.battery_config = battery_config
        self.solver_config = solver_config

        # we need to gain access to the results of the simulation, this will represent the results of the simulation
        self.results = None

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
            solution = sim.solve(t_eval) # time evalulation needs to be solved inside the simulation as an input field. Every other simulation is okay with a regular solve()
        else:
            solution = sim.solve()

        self.results = solution # store the results of the simulation

        # # get the key list of all the models output simulation parameters.
        # keys = list(self.electrochemical_model.variables.keys())
        # with open('simulation_keys.json', 'w') as f:
        #     json.dump({"output_data": keys}, f, indent=4)

        # sim.plot()
        
        return solution
    
    def run_driveCycle(self, driveCycle: DriveCycleFile, temperature: float = 25.0, title=""):
        # Access and modify the electrochemical model to disable events
        self.electrochemical_model.events = []

        # this should be it's def in utils for retrieving drive cycles and parsing it
        # Check if the chemistry is in the available drive cycles
        if driveCycle.chemistry not in AVAILABLE_DRIVE_CYCLES:
            raise ValueError(f"Invalid battery chemistry: {driveCycle.chemistry}. Use one of {list(AVAILABLE_DRIVE_CYCLES.keys())}")

        # Retrieve the drive cycles for the specified chemistry
        available_driveCycles = AVAILABLE_DRIVE_CYCLES[driveCycle.chemistry].driveCycle
        # Find the drive cycle with the specified name
        selected_driveCycle = next((dc for dc in available_driveCycles if dc.name == driveCycle.drive_cycle_file), None)

        if selected_driveCycle is None:
            raise ValueError(f"Invalid drive cycle name: {driveCycle.drive_cycle_file}. Available cycles: {[dc.name for dc in available_driveCycles]}")

        file_path = selected_driveCycle.path

        # Check if file path is empty
        if not file_path:
            raise ValueError("Drive cycle file path is empty")

        print(f"Loading data from: {file_path}")
        
        # Load the drive cycle data
        data = pd.read_csv(file_path, comment="#").to_numpy()
        print(f"Data loaded. Shape: {data.shape}")

        # Extract time and current data
        time_data = data[:, 0]
        current_data = data[:, 1]

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