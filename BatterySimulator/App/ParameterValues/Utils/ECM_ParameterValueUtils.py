from config.ParameterValues.ECM_Parameters import CircuitComponent, CircuitConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
import pybamm

# NOTE: Ideally i need to make a App/Config/ECM/Parameters.py class or something. in here i would add all the components (RC pairs) and all CircuitConfigurations (Initial SoC, Capacity, upper/lower voltage etc...)
# down the line if this is to work with a ECM RC Parameter identification service that uses optimization and parameterization. I want that server to find the ideal RC values and pass them here?
# additionally the user of ECM directly through the api will need to configure all the ECM values here

class ECM_ParameterValueUtils:
    @staticmethod
    def update_rc_parameter_values(ecm_config: ECMConfiguration, parameter_values: pybamm.ParameterValues, updated_parameters: dict):
        updated_parameters = {
            "Cell capacity [A.h]": 5,
            "Nominal cell capacity [A.h]": 5,
            "Current function [A]": 5,
            "Initial SoC": 0.5,
            "Element-1 initial overpotential [V]": 0,
            "Upper voltage cut-off [V]": 4.2,
            "Lower voltage cut-off [V]": 3.0,
            "R0 [Ohm]": 1e-3,
            "R1 [Ohm]": 2e-4,
            "C1 [F]": 1e4,
            "Open-circuit voltage [V]": pybamm.equivalent_circuit.Thevenin().default_parameter_values[
                "Open-circuit voltage [V]"
            ],
        }
        parameter_values.update(updated_parameters)

        if ecm_config.RC_pairs == 2:
            updated_parameters = {
                "R2 [Ohm]": 0.0003,
                "C2 [F]": 40000,
                "Element-2 initial overpotential [V]": 0,
            }
            parameter_values.update(updated_parameters, check_already_exists=False)
        
        return parameter_values