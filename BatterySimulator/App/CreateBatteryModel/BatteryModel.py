import pybamm
from config.Config import BatteryConfiguration
from libraries.CellLibrary import AVAILABLE_BPX_BATTERY_MODELS

class BatteryModel:
    @staticmethod
    def create(config: BatteryConfiguration):
        # chemistry = config.battery_chemistry
        # bpx_models = config.bpx_battery_models

        # # look for a valid chemistry
        # if chemistry not in AVAILABLE_BATTERY_MODELS:
        #     raise ValueError(f"Invalid battery chemistry: {chemistry}. Use one of {list(AVAILABLE_BATTERY_MODELS.keys())}")
        
        # # look for a valid model type for this chemistry
        # available_models = AVAILABLE_BATTERY_MODELS[chemistry].models
        # model = next((m for m in available_models if m.name == bpx_models), None)

        # if model is None:
        #     raise ValueError(f"Invalid battery model: {bpx_models}. Available models for {chemistry}: {[m.name for m in available_models]}")
        
        # return pybamm.ParameterValues.create_from_bpx(model.path)

        '''new logic to handle updated cell library so it no longer takes bpx without relying on a given chemistry'''

        model = config.parameter_value
        is_bpx = config.is_bpx

        if (is_bpx == True):
            available_models = AVAILABLE_BPX_BATTERY_MODELS

            # look for a bpx model + it's path from AVAILABLE_BPX_BATTERY_MODELS 
            model = next((m for m in available_models if m.name == model), None)

            return pybamm.ParameterValues.create_from_bpx(model.path)
        else:
            return pybamm.ParameterValues(model)