import pybamm
from App.CreateBatteryModel.Config import BatteryConfiguration, BPXBatteryModels

class BatteryModel:
    @staticmethod
    def create(battery_config: BatteryConfiguration, bpx_models: BPXBatteryModels, model_name: str):
        chemistry = battery_config.battery_chemistry

        # look for a valid chemistry
        if chemistry not in bpx_models.bpx_battery_models:
            raise ValueError(f"Invalid battery chemistry: {chemistry}. Use one of {list(bpx_models.bpx_battery_models.keys())}")
        
        # look for a valid model type in said chemistry
        available_models = bpx_models.bpx_battery_models[chemistry]
        if model_name not in available_models:
            raise ValueError(f"No BPX models available for battery chemistry: {chemistry}")

        bpx_path = bpx_models.bpx_battery_models[model_name]
        return pybamm.ParameterValues.create_from_bpx(bpx_path)