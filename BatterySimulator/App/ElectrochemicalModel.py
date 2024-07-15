import pybamm
from pydantic import BaseModel, StrictStr, validator

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