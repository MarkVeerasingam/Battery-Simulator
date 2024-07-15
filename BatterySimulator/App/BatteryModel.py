import os
import json
import requests
import pybamm
from pydantic import BaseModel, StrictStr, validator

# NMC = r"BatterySimulator\Models\NMC\AE_gen1_BPX.json"
# LFP = r"BatterySimulator\Models\LFP\lfp_18650_cell_BPX.json"

class BatteryModel(BaseModel):
    bpx_model: StrictStr 

    def config_loader(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, "r") as f:
            config = json.load(f)
        return config

    @staticmethod
    def create_from_config(bpx_model: str):
        return BatteryModel(bpx_model=bpx_model)

    @validator("bpx_model")
    def validate_chemistry(cls, bpx_model):
        if bpx_model not in {"LFP", "NMC"}:
            raise ValueError(f"Invalid BPX Model Type: {bpx_model}. Use LFP or NMC")
        return bpx_model
        
    # needs to be way more fault tolerrent. make it an index that looks up from the battery_chemistries.config
    def set_bpx_model(self):

        config = self.config_loader()
        try:
            bpx_path = config["bpx_battery_models"][self.bpx_model]
            parameter_values = pybamm.ParameterValues.create_from_bpx(bpx_path)
            return parameter_values
        except KeyError:
            raise ValueError(f"Invalid BPX Model Type: {self.bpx_model}. Use LFP or NMC")
        # if self.bpx_model == "LFP":
        #     parameter_values = pybamm.ParameterValues.create_from_bpx(LFP)
        # elif self.bpx_model == "NMC":
        #     parameter_values = pybamm.ParameterValues.create_from_bpx(NMC)
        # else:
        #     raise ValueError(f"Invalid BPX Model Type: {self.bpx_model}. Use LFP or NMC")
        # return parameter_values
    
    def update_model(self, bpx_model=None):
        if bpx_model:
            self.bpx_model = bpx_model

class ElectrochemicalModel(BaseModel):
    electrochemical_model: StrictStr

    @staticmethod
    def create_from_config(electrochemical_model: str):
        return ElectrochemicalModel(electrochemical_model=electrochemical_model)

    @validator("electrochemical_model")
    def validate_electrochemical_model(cls, electrochemical_model):
        if electrochemical_model not in {"DFN", "SPM", "SPMe"}:
            raise ValueError(f"Invalid Electrochemical Model Type: {electrochemical_model}. Model must be defined as DFN, SPM or SPMe")
        return electrochemical_model
    
    def set_electrochemical_model(self):
        if self.electrochemical_model == "DFN":
            model = pybamm.lithium_ion.DFN()
        elif self.electrochemical_model == "SPM":
            model = pybamm.lithium_ion.SPM()
        elif self.electrochemical_model == "SPMe":
            model = pybamm.lithium_ion.SPMe()
        else:
            raise ValueError(f"Invalid electrochemical model: {self.electrochemical_model}")
        
        return model
    
    def update_model(self, electrochemical_model=None):
        if electrochemical_model:
            self.electrochemical_model = electrochemical_model