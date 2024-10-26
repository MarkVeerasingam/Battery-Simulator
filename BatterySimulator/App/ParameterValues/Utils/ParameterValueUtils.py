from typing import Union, Dict
from config.ParameterValues.Electrochemical_Parameters.Electrochemical_Parameters import Update_Electrochemical_Parameters
from config.ParameterValues.ECM_Parameters.ECM_Parameters import TheveninParameters
from config.Models.EquivalentCircuitModel import ECMConfiguration
import pybamm

class ParameterValueUtils:
    @staticmethod
    def update_ParameterValues(parameter_values: pybamm.ParameterValues, updated_parameters: Union[Dict, Update_Electrochemical_Parameters]):
        
        if updated_parameters:
            if isinstance(updated_parameters, Update_Electrochemical_Parameters):
                updated_parameters = updated_parameters.dict(exclude_unset=True, by_alias=True)


            """Okay so. My thoughts were like, hey lets make a class of updatable parameters for physics based modelling
                that way the user can have programmatically fixed values they know they want plus more maintainable with the drawback on 
                original flexability of just updating from a dict. without knowledge of what to update.
                At some point i'll reimplement the logic of updating from a object class that of updatable params but for now
                it'll be a dict until I figure out what params the users *needs to update*

                side note: might want to look at helper api calls that call to the model/parmaeter set the user is using
                and can update what values they want to include into their list that way

                i also used aliases for this process to just automatically assign something like 
                'ambient_temperature' to 'Ambient temperature [K]' so it can be understood by pybamm
            """
            # invalid_params = [key for key in updated_parameters if key not in parameter_value.keys()]
            # if invalid_params:
            #     raise ValueError(f"Invalid parameters provided: {invalid_params}")

            try:
                parameter_values.update(updated_parameters)
            except pybamm.ModelError as e:
                raise ValueError(f"Parameter error occurred: {e}")

        return parameter_values
    
    # used in ECM Thevenin model only
    @staticmethod
    def update_rc_parameter_values(parameter_values: pybamm.ParameterValues, updated_parameters: TheveninParameters, ecm_config: ECMConfiguration):

        if isinstance(updated_parameters, TheveninParameters):
                updated_parameters = updated_parameters.dict(exclude_unset=True, by_alias=True)

        # invalid_params = [key for key in updated_parameters if key not in parameter_values.keys()]
        # if invalid_params:
        #     raise ValueError(f"Invalid parameters provided: {invalid_params}")

        try:
            parameter_values.update(updated_parameters, 
                                    {"Element-1 initial overpotential [V]": 0},
                                    pybamm.equivalent_circuit.Thevenin().default_parameter_values["Open-circuit voltage [V]"])
            
            # if the Thevenin model is a 2RC simulation, then updated the second resistor and capacitor
            if ecm_config.RC_pairs == 2:
                missing_params = []
                if "R2 [Ohm]" and "C2 [F]" not in updated_parameters:
                    missing_params.append("R2 [Ohm], " + "C2 [F]")
                if missing_params:
                    raise ValueError(f"2RC configuration is enabled but missing parameters: {', '.join(missing_params)}.")
                
                parameter_values.update({
                    "Element-2 initial overpotential [V]": 0,
                    "R2 [Ohm]": updated_parameters["R2 [Ohm]"],
                    "C2 [F]": updated_parameters["C2 [F]"]
                    }, check_already_exists=False)
                    
        except pybamm.ModelError as e:
            raise ValueError(f"Parameter error occurred: {e}")
        
        return parameter_values