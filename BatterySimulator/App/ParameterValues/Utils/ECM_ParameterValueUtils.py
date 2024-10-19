import pybamm

# NOTE: Ideally i need to make a App/Config/ECM/Parameters.py class or something. in here i would add all the components (RC pairs) and all CircuitConfigurations (Initial SoC, Capacity, upper/lower voltage etc...)
# down the line if this is to work with a ECM RC Parameter identification service that uses optimization and parameterization. I want that server to find the ideal RC values and pass them here?
# additionally the user of ECM directly through the api will need to configure all the ECM values here

class ECM_ParameterValueUtils:
    @staticmethod
    def update_1RC_thevenin_ParameterValues(parameter_values: pybamm.ParameterValues, updated_parameters: dict):
        # very simple logic, need to throw exception if a paramere is not in the parameter set. in theory this wont ever be raised as all parameters are hardcoded below as of right now
        if updated_parameters:
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

        return parameter_values
    
    # NOTE: this can only run if the Thevenin Model has 2RC options. options={'number of rc elements':2}  pybamm.equivalent_circuit.Thevenin(options)
    @staticmethod
    def update_2RC_thevenin_ParameterValues(parameter_values: pybamm.ParameterValues, updated_parameters: dict):
        
        # This is how to setup thevenin 2RC parameters, super niche way that was undocumented, but it works so ¯\_(ツ)_/¯
        # https://github.com/pybop-team/PyBOP/blob/develop/examples/notebooks/equivalent_circuit_identification.ipynb
        updated_parameters = {
            "R2 [Ohm]": 0.0003,
            "C2 [F]": 40000,
            "Element-2 initial overpotential [V]": 0,
        }
        parameter_values.update(updated_parameters, check_already_exists=False)
    
        return parameter_values