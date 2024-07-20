import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pybamm
from App.Simulation import Simulation

class DriveCycleSimulation:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
    
    def solve(self, temperature, filename, title=""):
        # Load drive cycle data
        file_path = "BatterySimulator/Models/LFP/data/validation/" + filename
        print(f"Loading data from: {file_path}")
        
        data = pd.read_csv(file_path, comment="#").to_numpy()
        print(f"Data loaded. Shape: {data.shape}")

        # Extract time, current, and voltage data
        time_data = data[:, 0]
        current_data = data[:, 1]
        voltage_data = data[:, 2]

        # Create current interpolant
        current_interpolant = pybamm.Interpolant(
            time_data, -current_data, pybamm.t, interpolator="linear"
        )

        # Update battery model parameters
        self.simulation.battery_model.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        # Run simulation
        sol = self.simulation.run(t_eval=time_data)

        # Plot results
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        ax[0].plot(time_data, voltage_data, "--", label=f"Experiment ({temperature}°C)")
        ax[0].plot(sol["Time [s]"].entries, sol["Terminal voltage [V]"].entries, "-", label=f"Model ({temperature}°C)")
        ax[1].plot(
            time_data, 
            (sol["Terminal voltage [V]"](t=time_data) - voltage_data) * 1000
        )
        rmse = np.sqrt(
            np.nanmean((voltage_data - sol["Terminal voltage [V]"](t=time_data))**2)
        ) * 1000

        print(f"RMSE = {rmse:.3f} mV \n")

        ax[1].text(0.8, 0.2, f"RMSE: {rmse:.3f} mV ({temperature}°C)",
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax[1].transAxes,
                )  

        ax[0].set_xlabel("Time [s]")
        ax[0].set_ylabel("Voltage [V]")
        ax[0].legend()
        ax[1].set_xlabel("Time [s]")
        ax[1].set_ylabel("Error [mV]")
        plt.suptitle(title)
        plt.tight_layout()
        plt.show()
        
        return sol
