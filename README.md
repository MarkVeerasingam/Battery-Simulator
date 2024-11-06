# Battery Simulator 
## A Batteries-Included API for Battery Simulations

This is a WIP API that contributes towards my final year project of a web based battery simulator for Atlantic Technological University.

Python based lithium ion battery simulator api, built on [Pybamm](https://github.com/pybamm-team/PyBaMM) - Please go check them out!

This API models batteries from the [BPX](https://github.com/FaradayInstitution/BPX) JSON Schema. 2 Lithium Ion Models are provided in this API by About:Energy,
NMC and LFP chemistries.

The API encapsulates various simulation features and functionalities that a user can call from.

### Posting to the API: http://localhost:8084/simulate
## Example Post Request
```
{
    "parameter_values": {
        "is_bpx": true,
        "parameter_value": "lfp_18650_cell_BPX",  
        "updated_parameters": {
            "Ambient temperature [K]": 298.15
        }
    },
    "electrochemical_model": {
        "electrochemical_model": "SPM", 
        "cell_geometry": "arbitrary",
        "thermal_model": "isothermal"
    },
    "solver_model": {
        "solver": "IDAKLUSolver",
        "tolerance": {
            "atol": 1e-6,
            "rtol": 1e-6
        },
        "mode": "safe"
    },
    "simulation": {
        "drive_cycle": {
            "drive_cycle_file": "LFP_25degC_DriveCycle"
        }
    },
    "display_params": ["Terminal voltage [V]", "Current [A]", "Discharge capacity [A.h]"]
}
```

## Performing Equvialent Circuit Model Simulation
```
{
    "equivalent_circuit_model": {
        "RC_pairs": 2
    },
    "parameter_values": {
        "parameter_value": "ECM_Example",
        "updated_parameters": {
            "Cell capacity [A.h]": 5,
            "Nominal cell capacity [A.h]": 5,
            "Current function [A]": 5,
            "Initial SoC": 0.5,
            "Upper voltage cut-off [V]": 4.2,
            "Lower voltage cut-off [V]": 3.0,
            "R0 [Ohm]": 0.001,
            "R1 [Ohm]": 0.0002, 
            "C1 [F]": 10000,
            "R2 [Ohm]": 0.0003,
            "C2 [F]": 40000
        }
    },
    "solver": {
        "solver": "IDAKLUSolver"
    },
    "simulation": {
        "experiment": [
            "Discharge at C/10 for 1 hour or until 3.3 V",
            "Rest for 30 minutes",
            "Rest for 2 hours",
            "Charge at 100 A until 4.1 V",
            "Hold at 4.1 V until 5 A",
            "Rest for 30 minutes",
            "Rest for 1 hour"
        ]
    },
    "display_params": ["Voltage [V]", "Current [A]", "Jig temperature [K]"]
}
```
## Performing various simultion types
### Experiment Simulation
```
"simulation": {
        "experiment": [  
             "Discharge at C/5 for 10 hours or until 2.5 V",
             "Rest for 1 hour",
             "Charge at 1 A until 3.5 V",
             "Hold at 3.5 V until 10 mA",
             "Rest for 1 hour"
         ]
    },
```
### Time Evaluation Simulation
```
"simulation": {
         "t_eval": [0, 3600]  // simulate for one hour
    },
```
### Drive Cycle Simulation
```
"simulation": {
        "drive_cycle": {
            "drive_cycle_file": "LFP_25degC_DriveCycle"
        }
    },
```