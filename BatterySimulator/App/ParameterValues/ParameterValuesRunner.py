from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.ParameterValues.ECM_Parameters.ECM_Parameters import TheveninParameters
from App.ParameterValues.ParameterValueTypes.StandardParameterValues import StandardParameterValues
from App.ParameterValues.ParameterValueTypes.BPX import BPXParameterValues
from App.ParameterValues.Utils.ParameterValueUtils import ParameterValueUtils
from config.Models.EquivalentCircuitModel import ECMConfiguration


# new idea. config: ParameterValueConfiguration could be parmaetersets, or parmaeterValuePathing. With its purpose to path you to parmaeter sets, like "Chen2020" or a bpx file. 
# Right now I only need ECM_Parameters but i could have a Physics_parameters, both have their respective parameter sets that the user may want to tweak manually.
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
        updated_param_values = config.updated_parameters
        is_bpx = config.is_bpx

        if is_bpx:
            param_values = BPXParameterValues.create(parameter_values)
        else:
            param_values = StandardParameterValues.create(parameter_values)

        if updated_param_values:
            param_values = ParameterValueUtils.update_ParameterValues(parameter_values=param_values, 
                                                                      updated_parameters=updated_param_values)

        return param_values
    
    @staticmethod
    def create_ecm(config: ParameterValueConfiguration, ecm_config: ECMConfiguration):

        parameter_values = config.parameter_value
        updated_param_values = config.updated_parameters
        is_bpx = config.is_bpx

        if is_bpx:
            param_values = BPXParameterValues.create(parameter_values)
        else:
            param_values = StandardParameterValues.create(parameter_values)

        if updated_param_values:
            param_values = ParameterValueUtils.update_rc_parameter_values(parameter_values=param_values, 
                                                                          updated_parameters=updated_param_values,
                                                                          ecm_config=ecm_config)

        return param_values