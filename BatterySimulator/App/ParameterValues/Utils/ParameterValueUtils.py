from typing import Union, Dict
from App.ParameterValues.ParameterValueTypes.StandardParameterValues import StandardParameterValues
from config.ParameterValues.Electrochemical_Parameters.Electrochemical_Parameters import Update_Electrochemical_Parameters
import pybamm

class ParameterValueUtils:
    @staticmethod
    def update_ParameterValues(parameter_value: pybamm.ParameterValues, updated_parameters: Union[Dict, Update_Electrochemical_Parameters]):
        
        if updated_parameters:
            if isinstance(updated_parameters, Update_Electrochemical_Parameters):
                updated_parameters = updated_parameters.dict(exclude_unset=False, by_alias=True)


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
                parameter_value.update(updated_parameters)
            except pybamm.ModelError as e:
                raise ValueError(f"Parameter error occurred: {e}")

        return parameter_value