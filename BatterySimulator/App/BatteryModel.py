import json
import pybamm
from pydantic import BaseModel, StrictStr, validator

CONFIG_PATH = 'BatterySimulator/config/config.json'

class BatteryModel(BaseModel):
    bpx_model: StrictStr 

    def config_loader(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
            return config
        except FileNotFoundError: 
            raise FileNotFoundError("Config file not found!")

    @staticmethod
    def create_from_config(bpx_model: str):
        return BatteryModel(bpx_model=bpx_model)

    @validator("bpx_model")
    def validate_chemistry(cls, bpx_model):
        if bpx_model not in {"LFP", "NMC"}:
            raise ValueError(f"Invalid BPX Model Type: {bpx_model}. Use LFP or NMC")
        return bpx_model
        
    def set_bpx_model(self):
        config = self.config_loader()
        try:
            bpx_path = config["bpx_battery_models"][self.bpx_model]
            parameter_values = pybamm.ParameterValues.create_from_bpx(bpx_path)
            return parameter_values
        except KeyError:
            raise ValueError(f"Invalid BPX Model Type: {self.bpx_model}. Use LFP or NMC")
    
    def update_model(self, bpx_model=None):
        if bpx_model:
            self.bpx_model = bpx_model