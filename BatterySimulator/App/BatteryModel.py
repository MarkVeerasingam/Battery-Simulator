import pybamm
from pydantic import BaseModel, StrictStr, validator

NMC = r"BatterySimulator\Models\NMC\AE_gen1_BPX.json"
LFP = r"BatterySimulator\Models\LFP\lfp_18650_cell_BPX.json"

class BatteryModel(BaseModel):
    bpx_model: StrictStr 

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
        if self.bpx_model == "LFP":
            parameter_values = pybamm.ParameterValues.create_from_bpx(LFP)
        elif self.bpx_model == "NMC":
            parameter_values = pybamm.ParameterValues.create_from_bpx(NMC)
        else:
            raise ValueError(f"Invalid BPX Model Type: {self.bpx_model}. Use LFP or NMC")
        
        return parameter_values
    
    def update_model(self, bpx_model=None):
        if bpx_model:
            self.bpx_model = bpx_model

