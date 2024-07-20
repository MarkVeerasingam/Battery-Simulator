import time
from App.CreateBatteryModel.Config import BatteryConfiguration, SolverConfiguration
from App.Simulation import Simulation
from App.SimulationRunner import SimulationRunner
from App.DriveCycleSimulation import DriveCycleSimulation

def experiment():
    battery_config = BatteryConfiguration(
        battery_chemistry="NMC",
        bpx_battery_models="AE_gen1_BPX",
        electrochemical_model="SPM"
    )

    solver_config = SolverConfiguration(
        solver="CasadiSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6}
    )

    sim_runner = SimulationRunner(battery_config, solver_config)

    # Uncomment one of these to set the simulation type
    # sim_runner.set_t_eval([0, 7200])
    sim_runner.set_experiment([
        (
            "Discharge at C/5 for 5 hours or until 2.5 V",
            "Rest for 30 minutes",
            "Charge at 2 A until 3.5 V",
            "Hold at 3.5 V until 20 mA",
            "Rest for 1 hour",
        ),
    ] * 4)

    sim_runner.run_simulation()

def drive_cycle():
    config = BatteryConfiguration(
        battery_chemistry="NMC",
        bpx_battery_models="AE_gen1_BPX",
        electrochemical_model="DFN",
        solver="CasadiSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6}
    )

    solver_config = SolverConfiguration(
        solver="CasadiSolver",
        tolerance={"atol": 1e-6, "rtol": 1e-6}
    )
    
    sim = Simulation(config, solver_config)

    drive_cycle_simulation = DriveCycleSimulation(sim)

    temperature = 25  # Example temperature in °C
    filename = "LFP_25degC_1C.csv"  

    drive_cycle_simulation.solve(temperature=temperature, filename=filename)

if __name__ == '__main__':
    start_time = time.time()

    experiment()    
    # drive_cycle()
    
    print(f"Time(s): {time.time() - start_time:.2f}")