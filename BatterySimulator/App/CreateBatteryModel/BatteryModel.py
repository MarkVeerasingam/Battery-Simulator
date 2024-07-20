import pybamm
from App.CreateBatteryModel.Config import BatteryConfiguration

class BatteryModel:
    @staticmethod
    def create(config: BatteryConfiguration):
        chemistry = config.battery_chemistry
        bpx_models = config.bpx_battery_models

        # look for a valid chemistry
        if chemistry not in bpx_models:
            raise ValueError(f"Invalid battery chemistry: {chemistry}. Use one of {list(bpx_models.keys())}")
        
        # look for a valid model type for this chemistry
        available_models = bpx_models[chemistry]
        if not available_models:
            raise ValueError(f"No BPX models available for battery chemistry: {chemistry}")
        
        model_name, bpx_path = next(iter(available_models.items()))

        return pybamm.ParameterValues.create_from_bpx(bpx_path)
