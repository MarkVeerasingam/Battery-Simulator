from App.SimulationRunner import SimulationRunner

if __name__ == '__main__':

    simRunner = SimulationRunner()

    # update the model configuration with a setter method made from SimulationRunner
    simRunner.set_model_config({"bpx_model": "LFP", "electrochemical_model": "DFN"})
    simRunner.set_solver_config({"solver": "CasadiSolver", "atol": 1e-6, "rtol": 1e-6})

    # run simulation
    new_experiment = [
        (
            "Discharge at C/5 for 5 hours or until 2.5 V",
            "Rest for 30 minutes",
            "Charge at 2 A until 3.5 V",
            "Hold at 3.5 V until 20 mA",
            "Rest for 1 hours",
        ),
    ] * 2
    simRunner.set_experiment(new_experiment)

    simRunner.run_experiment_simulation()
    # simRunner.run_time_evaluation_simulation()