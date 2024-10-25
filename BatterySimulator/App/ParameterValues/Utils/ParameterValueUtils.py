from typing import Union, Dict
from App.ParameterValues.ParameterValueTypes.StandardParameterValues import StandardParameterValues
from config.ParameterValues.Electrochemical_Parameters.Electrochemical_Parameters import ElectrochemicalParameters
import pybamm

class ParameterValueUtils:
    @staticmethod
    def update_ParameterValues(parameter_value: pybamm.ParameterValues, updated_parameters: Union[Dict, ElectrochemicalParameters]):
        
        if updated_parameters:
            if isinstance(updated_parameters, ElectrochemicalParameters):
                updated_parameters = updated_parameters.dict(exclude_unset=False, by_alias=True)

            invalid_params = [key for key in updated_parameters if key not in parameter_value.keys()]
            if invalid_params:
                raise ValueError(f"Invalid parameters provided: {invalid_params}")

            try:
                parameter_value.update(updated_parameters)
            except pybamm.ModelError as e:
                raise ValueError(f"Parameter error occurred: {e}")

        return parameter_value