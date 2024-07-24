import time
from App.CreateBatteryModel.Config import BatteryConfiguration, SolverConfiguration, DriveCycleFile
from App.Simulation import Simulation
from App.SimulationRunner import SimulationRunner
from App.DriveCycleSimulation import DriveCycleSimulation

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
    battery_config = battery()
    solver_config = solver()
    
    sim_runner = SimulationRunner(battery_config, solver_config)

    experiment =  [
        (
            "Discharge at C/5 for 10 hours or until 2.5 V",
            "Rest for 1 hour",
            "Charge at 1 A until 3.5 V",
            "Hold at 3.5 V until 10 mA",
            "Rest for 1 hour",
        ),
    ] * 2

    sim_runner.set_experiment(experiment=experiment)

    sim_runner.run_simulation()

def time_eval():
    battery_config = battery()
    solver_config = solver()

    sim_runner = SimulationRunner(battery_config, solver_config)

    sim_runner.set_t_eval([0, 7200])

    sim_runner.run_simulation()

def drive_cycle():
    battery_config = battery()
    solver_config = solver()

    sim = Simulation(battery_config, solver_config)

    drive_cycle_simulation = DriveCycleSimulation(simulation=sim)

    driveCycle_config = DriveCycleFile(
        chemistry="NMC",
        drive_cycle_file="NMC_25degC_DriveCycle"
    )
    
    drive_cycle_simulation.solve(config=driveCycle_config, temperature=25)

if __name__ == '__main__':
    start_time = time.time()

    # time_eval()
    # experiment()    
    drive_cycle()
    
    print(f"Time(s): {time.time() - start_time:.2f}")