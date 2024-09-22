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

            return pybamm.ParameterValues.create_from_bpx(model.path)
        else:
            return pybamm.ParameterValues(model)