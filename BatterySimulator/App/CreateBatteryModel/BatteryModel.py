import pybamm
from config.Config import BatteryConfiguration
from libraries.CellLibrary import AVAILABLE_BATTERY_MODELS

class BatteryModel:
    @staticmethod
    def create(config: BatteryConfiguration):
        # chemistry = config.battery_chemistry
        model = config.bpx_battery_models

        # # look for a valid chemistry
        # if chemistry not in AVAILABLE_BATTERY_MODELS:
        #     raise ValueError(f"Invalid battery chemistry: {chemistry}. Use one of {list(AVAILABLE_BATTERY_MODELS.keys())}")
        
        # look for a valid model type for this chemistry
        available_models = AVAILABLE_BATTERY_MODELS
        model = next((m for m in available_models if m.name == model), None)

        # if model is None:
        #     raise ValueError(f"Invalid battery model: {bpx_models}. Available models for {chemistry}: {[m.name for m in available_models]}")

        if model is None:
            raise ValueError(f"Invalid battery model: {model}. Available models: {[m.name for m in AVAILABLE_BATTERY_MODELS]}")

        
        return pybamm.ParameterValues.create_from_bpx(model.path)