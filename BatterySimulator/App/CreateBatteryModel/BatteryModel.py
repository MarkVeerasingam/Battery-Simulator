import pybamm
import json

CONFIG_PATH = 'BatterySimulator/config/config.json'

class BatteryModel:
    @staticmethod
    def create(model_type: str):
        if model_type not in {"LFP", "NMC"}:
            raise ValueError(f"Invalid BPX Model Type: {model_type}. Use LFP or NMC")
        
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        
        bpx_path = config["bpx_battery_models"][model_type]
        return pybamm.ParameterValues.create_from_bpx(bpx_path)