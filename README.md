# Battery Simulator 
## A Batteries-Included API for Battery Simulations

This is a WIP API that contributes towards my final year project of a web based battery simulator for Atlantic Technological University.

Python based lithium ion battery simulator api, built on [Pybamm](https://github.com/pybamm-team/PyBaMM) - Please go check them out!

This API models batteries from the [BPX](https://github.com/FaradayInstitution/BPX) JSON Schema. 2 Lithium Ion Models are provided in this API by About:Energy,
NMC and LFP chemistries.

The API encapsulates various simulation features and functionalities that a user can call from.

### Posting to the API:
## http://localhost:8084/simulate
### "simulation" -> "type": tells the simulator what type of simulation to perform (experiment, drive_cycle or time_eval(time evaluation))
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
        // "experiment": [  
        //     "Discharge at C/5 for 10 hours or until 2.5 V",
        //     "Rest for 1 hour",
        //     "Charge at 1 A until 3.5 V",
        //     "Hold at 3.5 V until 10 mA",
        //     "Rest for 1 hour"
        // ],
        // "t_eval": [0, 7200]  
    },
    "display_params": ["Terminal voltage [V]", "Current [A]", "Discharge capacity [A.h]"]
}
```