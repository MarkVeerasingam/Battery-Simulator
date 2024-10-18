import pybamm

class StandardParameterValues:
    @staticmethod
    def create(parameter_value: str):
        return pybamm.ParameterValues(parameter_value)