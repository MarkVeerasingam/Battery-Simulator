import time
from App.Config import Configuration
from App.SimulationRunner import SimulationRunner

if __name__ == '__main__':
    start_time = time.time()

    config = Configuration(
        battery_model="LFP",
        electrochemical_model="DFN",
        solver="CasadiSolver",
        atol=1e-6,
        rtol=1e-6
    )

    sim_runner = SimulationRunner(config)

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
    ] * 2)

    sim_runner.run_simulation()

    print(f"Time(s):{time.time()-start_time:.2f}")