from config.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile, SimulationConfiguration
from App.SimulationRunner import SimulationRunner

def battery():
    battery_config = BatteryConfiguration(
        battery_chemistry="NMC",
        bpx_battery_models="NMC_Pouch_cell",
        electrochemical_model="DFN"
    )
    return battery_config

def solver():
    solver_config = SolverConfiguration(
        solver="CasadiSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6}
    )
    return solver_config

def experiment():
    battery_config = battery()  # set the battery model configuration
    solver_config = solver()    # set the simulation solver configuration
    
    simulation_config = SimulationConfiguration(
        experiment=[
            "Discharge at C/5 for 10 hours or until 2.5 V",
            "Rest for 1 hour",
            "Charge at 1 A until 3.5 V",
            "Hold at 3.5 V until 10 mA",
            "Rest for 1 hour",
        ] * 4
    )

    sim_runner = SimulationRunner(battery_config, solver_config)
    sim_runner.run_simulation(config=simulation_config)
    sim_runner.display_results(["Time [s]", "Terminal voltage [V]"])

def time_eval():
    battery_config = battery()
    solver_config = solver()

    simulation_config = SimulationConfiguration(
        t_eval=[0, 7200]
    )

    sim_runner = SimulationRunner(battery_config, solver_config)
    sim_runner.run_simulation(config=simulation_config)
    sim_runner.display_results(["Time [s]", "Terminal voltage [V]"])

def drive_cycle():
    battery_config = battery()
    solver_config = solver()

    simulation_config = SimulationConfiguration(
        drive_cycle=DriveCycleFile(
            chemistry="NMC",
            drive_cycle_file="NMC_25degC_1C"
        )
    )

    sim_runner = SimulationRunner(battery_config, solver_config)
    sim_runner.run_simulation(config=simulation_config)
    sim_runner.display_results(["Time [s]", "Terminal voltage [V]"])