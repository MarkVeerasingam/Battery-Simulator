import pybamm
from config.ParameterValues import ParameterValueConfiguration
from libraries.CellLibrary import AVAILABLE_BPX_BATTERY_MODELS

class ParameterValues:
    @staticmethod
    def create(config: ParameterValueConfiguration):
        parameter_values = config.parameter_value
        is_bpx = config.is_bpx

        if (is_bpx == True):
            available_models = AVAILABLE_BPX_BATTERY_MODELS

            # look for a bpx model + it's path from AVAILABLE_BPX_BATTERY_MODELS 
            parameter_values = next((m for m in available_models if m.name == parameter_values), None)

            # simple check if the model exists or not. Not sure how to handle the built in parameter set error handling, maybe pray that the UI is intiutive for users to not break it?
            if parameter_values is None:
                    raise ValueError(f"Invalid BPX model: {parameter_values}. Available models: {[m.name for m in available_models]}")

            return pybamm.ParameterValues.create_from_bpx(parameter_values.path)
        else:
            return pybamm.ParameterValues(parameter_values)