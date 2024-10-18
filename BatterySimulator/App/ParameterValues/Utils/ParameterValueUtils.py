import pybamm

class ParameterValueUtils:
    @staticmethod
    def update_ParameterValues(parameter_value: pybamm.ParameterValues, updated_parameters: dict):
        
        # very simple logic, need to throw exception if a paramere is not in the parameter set
        if updated_parameters:
            parameter_value.update(updated_parameters)

        return parameter_value