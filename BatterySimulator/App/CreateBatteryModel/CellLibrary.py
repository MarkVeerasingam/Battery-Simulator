from pydantic import BaseModel
from typing import Dict, List

class BPXModel(BaseModel):
    name: str
    path: str

class ChemistryModels(BaseModel):
    models: List[BPXModel]

# A library of all avaible BPX Schema models for a given chemistry
AVAILABLE_BATTERY_MODELS: Dict[str, ChemistryModels] = {
    "NMC": ChemistryModels(models=[
        BPXModel(name="AE_gen1_BPX", path="BatterySimulator/Models/NMC/AE_gen1_BPX.json"),
        BPXModel(name="NMC_model2", path="BatterySimulator/Models/NMC/NMC_model2.json"),
    ]),
    "LFP": ChemistryModels(models=[
        BPXModel(name="lfp_18650_cell_BPX", path="BatterySimulator/Models/LFP/lfp_18650_cell_BPX.json"),
        BPXModel(name="LFP_model2", path="BatterySimulator/Models/LFP/LFP_model2.json"),
    ]),
}