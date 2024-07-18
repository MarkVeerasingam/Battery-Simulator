import pybamm
from App.CreateBatteryModel.Config import Configuration
from App.CreateBatteryModel.BatteryModel import BatteryModel
from App.CreateBatteryModel.ElectrochemicalModel import ElectrochemicalModel
from App.CreateBatteryModel.Solver import Solver

class Simulation:
    def __init__(self, config: Configuration):
        self.electrochemical_model = ElectrochemicalModel.create(config.electrochemical_model)
        self.battery_model = BatteryModel.create(config.battery_model)
        self.solver = Solver.create(config.solver, config.atol, config.rtol)

    def run(self, t_eval=None, experiment=None):
        sim = pybamm.Simulation(
            model=self.electrochemical_model,
            parameter_values=self.battery_model,
            solver=self.solver,
            experiment=experiment
        )
        
        if t_eval:
            solution = sim.solve(t_eval)
        else:
            solution = sim.solve()
        
        #sim.plot()
        return solution

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pybamm

class DriveCycleSimulation:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
    
    def solve(self, temperature, filename, title=""):
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        
        # Load drive cycle data
        data = pd.read_csv(
            "BatterySimulator\\Models\\LFP\\data\\validation\\" + filename,
            comment="#",
        ).to_numpy()

        # Split out time [s] vs voltage [V]
        voltage_data = data[:, [0, 2]]

        # Split out time [s] vs current [A]
        current_data = data[:, [0, 1]]

        # Create current interpolant
        # timescale = self.simulation.electrochemical_model.timescale
        current_interpolant = pybamm.Interpolant(
            current_data[:, 0], -current_data[:, 1], pybamm.t, interpolator="linear")

        # Update parameter values for drive cycle and temperature
        self.simulation.battery_model.update({
            "Current function [A]": current_interpolant,
            "Ambient temperature [K]": 273.15 + temperature,
            "Initial temperature [K]": 273.15 + temperature,
        })

        # Run the simulation
        sol = self.simulation.run()

        # Plot results
        ax[0].plot(voltage_data[:, 0], voltage_data[:, 1], "--", label=f"Experiment ({temperature}°C)")
        ax[0].plot(sol["Time [s]"].entries, sol["Terminal voltage [V]"].entries, "-", label=f"Model ({temperature}°C)")
        ax[1].plot(
            voltage_data[:, 0], 
            (sol["Terminal voltage [V]"](t=voltage_data[:, 0]) - voltage_data[:, 1]) * 1000,
        )
        rmse = np.sqrt(
            np.nanmean((voltage_data[:, 1] - sol["Terminal voltage [V]"](t=voltage_data[:, 0]))**2)
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
