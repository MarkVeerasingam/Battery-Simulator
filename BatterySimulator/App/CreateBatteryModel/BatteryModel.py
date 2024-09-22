import pybamm
from config.Config import BatteryConfiguration
from libraries.CellLibrary import AVAILABLE_BPX_BATTERY_MODELS

class BatteryModel:
    @staticmethod
    def create(config: BatteryConfiguration):
        model = config.parameter_value
        is_bpx = config.is_bpx

        if (is_bpx == True):
            available_models = AVAILABLE_BPX_BATTERY_MODELS

            # look for a bpx model + it's path from AVAILABLE_BPX_BATTERY_MODELS 
            model = next((m for m in available_models if m.name == model), None)

            # simple check if the model exists or not. Not sure how to handle the built in parameter set error handling, maybe pray that the UI is intiutive for users to not break it?
            if model is None:
                    raise ValueError(f"Invalid BPX model: {model}. Available models: {[m.name for m in available_models]}")

            return pybamm.ParameterValues.create_from_bpx(model.path)
        else:
            return pybamm.ParameterValues(model)