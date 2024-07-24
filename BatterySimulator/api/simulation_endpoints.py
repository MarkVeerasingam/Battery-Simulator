from config.Config import DriveCycleFile
from App.Simulation import Simulation
from App.SimulationRunner import SimulationRunner, DriveCycleSimulation
from api.configuration_endpoints import battery, solver

def experiment():
    battery_config = battery() # set the battery model configuration
    solver_config = solver()   # set the simulation solver configuration 
    
    sim_runner = SimulationRunner(battery_config, solver_config)

    experiment =  [
        (
            "Discharge at C/5 for 10 hours or until 3.3 V",
            "Rest for 1 hour",
            "Charge at 1 A until 4.1 V",
            "Hold at 4.1 V until 10 mA",
            "Rest for 1 hour",
        ),
    ] * 4

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

    simulation = Simulation(battery_config, solver_config)

    drive_cycle_simulation = DriveCycleSimulation(simulation=simulation)

    driveCycle_config = DriveCycleFile(
        chemistry="NMC",
        drive_cycle_file="NMC_25degC_DriveCycle"
    )
    
    drive_cycle_simulation.set_drive_cycle(driveCycle_config)
    drive_cycle_simulation.run_simulation()