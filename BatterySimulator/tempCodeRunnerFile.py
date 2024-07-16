from App.SimulationRunner import SimulationRunner

if __name__ == '__main__':
    simRunner = SimulationRunner()

    # DEFINE TYPE OF SIMULATION
    simRunner.electrochemical_params = {"electrochemical_model": "DFN"}
    simRunner.battery_params = {"bpx_model": "LFP"}
    simRunner.solver_params = {"solver": "CasadiSolver", "atol": 1e-6, "rtol": 1e-6}

    # TIME EVALULATION SIMULATION
    t_eval = [0, 7200]
    simRunner.t_eval = t_eval

    # EXPERIMENT SIMULATION
    # outline a new experiment for the simulation
    new_experiment = [
        (
            "Discharge at C/5 for 5 hours or until 2.5 V",
            "Rest for 30 minutes",
            "Charge at 2 A until 3.5 V",
            "Hold at 3.5 V until 20 mA",
            "Rest for 1 hour",
        ),
    ] * 2
    simRunner.experiment = new_experiment

    # RUN SIMULATION
    simRunner.run_experiment_simulation()
    # simRunner.run_time_evaluation_simulation()

