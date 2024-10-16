import pybamm
from config.ParameterValues import ParameterValueConfiguration
from App.ParameterValues.ParameterValueTypes.StandardParameterValues import StandardParameterValues
from App.ParameterValues.ParameterValueTypes.BPX import BPXParameterValues

class ParameterValuesRunner:
    @staticmethod
    def create(config: ParameterValueConfiguration):
        """
        Creates parameter values based on the provided configuration.
        :param config: An instance of ParameterValueConfiguration, which specifies whether to use a BPX model
                       or a standard pybamm model, and includes any optional updated parameters.
        :return: A pybamm.ParameterValues object with the desired configuration.
        """
        parameter_values = config.parameter_value
        is_bpx = config.is_bpx

        if is_bpx:
            param_values = BPXParameterValues.create(parameter_values)
        else:
            param_values = StandardParameterValues.create(parameter_values)

        return param_values