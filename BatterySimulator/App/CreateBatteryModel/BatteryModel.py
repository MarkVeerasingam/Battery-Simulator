import pybamm
from App.CreateBatteryModel.Config import BatteryConfiguration, BPXBatteryModels

class BatteryModel:
    @staticmethod
    def create(model_type: str, bpx_models: BPXBatteryModels):
        if model_type not in bpx_models.bpx_battery_models:
            raise ValueError(f"Invalid BPX Model Type: {model_type}. Use one of {list(bpx_models.bpx_battery_models.keys())}")
        
        bpx_path = bpx_models.bpx_battery_models[model_type]
        return pybamm.ParameterValues.create_from_bpx(bpx_path)