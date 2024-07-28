# Lithium Ion Battery Simulator
## A Batteries-Included API for Battery Simulations

This is a WIP API that contributes towards my final year project of a web based battery simulator for Atlantic Technological University.

Python based lithium ion battery simulator api, built on [Pybamm](https://github.com/pybamm-team/PyBaMM) - Please go check them out!

This API models batteries from the [BPX](https://github.com/FaradayInstitution/BPX) JSON Schema. 2 Lithium Ion Models are provided in this API by About:Energy,
NMC and LFP chemistries.

The API encapsulates various simulation features and functionalities that a user can call from.

### Posting to the API:
## http://localhost:8084/simulate
## Drive Cycle Simulation raw JSON
```
{
    "battery_chemistry": "NMC",
    "bpx_battery_models": "NMC_Pouch_cell",
    "electrochemical_model": "DFN",
    "solver": "CasadiSolver",
    "tolerance": {
        "atol": 1e-6,
        "rtol": 1e-6
    },
    "simulation_type": "drive_cycle",
    "drive_cycle": {
        "chemistry": "NMC",
        "drive_cycle_file": "NMC_25degC_1C"
    },
    "display_params": ["Time [s]", "Terminal voltage [V]", "Current [A]"]
}
```
## Experiment Simulation raw JSON
```
{
    "battery_chemistry": "LFP",
    "bpx_battery_models": "lfp_18650_cell_BPX",
    "electrochemical_model": "DFN",
    "solver": "CasadiSolver",
    "tolerance": {"atol": 1e-6, "rtol": 1e-6},
    "simulation_type": "experiment",
    "experiment": [
        "Discharge at C/5 for 10 hours or until 2.5 V",
        "Rest for 1 hour",
        "Charge at 1 A until 3.5 V",
        "Hold at 3.5 V until 10 mA",
        "Rest for 1 hour"
    ],
    "display_params": ["Time [s]", "Terminal voltage [V]", "Current [A]"]
}
```
## Time-Evaluation Simulation raw JSON
```
{
    "battery_chemistry": "NMC",
    "bpx_battery_models": "NMC_Pouch_cell",
    "electrochemical_model": "DFN",
    "solver": "CasadiSolver",
    "tolerance": {
        "atol": 1e-6,
        "rtol": 1e-6
    },
    "simulation_type": "time_eval",
    "t_eval": [0, 7200],
    "display_params": ["Time [s]", "Terminal voltage [V]", "Current [A]"]
}
```
