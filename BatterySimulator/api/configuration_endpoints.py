from config.Config import BatteryConfiguration, SolverConfiguration

def battery():
    battery_config = BatteryConfiguration(
        battery_chemistry="LFP",
        bpx_battery_models="lfp_18650_cell_BPX",
        electrochemical_model="DFN"
    )
    return battery_config

def solver():
    solver_config = SolverConfiguration(
        solver="CasadiSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6}
    )
    return solver_config