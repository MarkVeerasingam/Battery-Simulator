import pandas as pd
import pybamm
from config.Config import DriveCycleFile
from libraries.DriveCycleLibrary import AVAILABLE_DRIVE_CYCLES 
from App.Simulations.SimulationTypes.BaseSimulation import BaseSimulation

class DriveCycleSimulation(BaseSimulation):
    def run(self, drive_cycle: DriveCycleFile, temperature: float = 25.0):
        # Clear any existing events
        self.electrochemical_model.events = []

        # Select the drive cycle based on the provided drive cycle name
        selected_drive_cycle = next(
            (dc for dc in AVAILABLE_DRIVE_CYCLES if dc.name == drive_cycle.drive_cycle_file), 
            None
        )
        if selected_drive_cycle is None:
            raise ValueError(f"Invalid drive cycle name: {drive_cycle.drive_cycle_file}.")

        # Get the file path for the selected drive cycle
        file_path = selected_drive_cycle.path
        if not file_path:
            raise ValueError("Drive cycle file path is empty.")

        # Load the drive cycle data
        try:
            data = pd.read_csv(file_path, comment="#").to_numpy()
        except FileNotFoundError:
            raise ValueError(f"Drive cycle file '{file_path}' not found.")
        except Exception as e:
            raise ValueError(f"An error occurred while reading the drive cycle file: {str(e)}")

        time_data = data[:, 0]
        current_data = data[:, 1]

        # Create an interpolant for the current function
        current_interpolant = pybamm.Interpolant(time_data, -current_data, pybamm.t, interpolator="linear")
        
        # Update parameter values
        self.parameter_values.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        sol = self.run_simulation()  
        return sol
