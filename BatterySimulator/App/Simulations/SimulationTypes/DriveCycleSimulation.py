import pybamm
from config.Config import DriveCycleFile
from App.Simulations.Utils.drive_cycle_utils import read_drive_cycle_data, interpolate_drive_cycle_data
from App.Simulations.SimulationTypes.BaseSimulation import BaseSimulation

class DriveCycleSimulation(BaseSimulation):
    def run(self, drive_cycle: DriveCycleFile, temperature: float = 25.0):
        # Clear any existing model events
        self.electrochemical_model.events = []

        time_data, current_data = read_drive_cycle_data(drive_cycle.drive_cycle_file)

        # Create an interpolant for the current function
        current_interpolant = interpolate_drive_cycle_data(time_data, current_data)

        # Update parameter values
        self.parameter_values.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        sol = self.run_simulation()  
        return sol