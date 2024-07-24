from pydantic import BaseModel
from typing import Dict, List

class BPXModel(BaseModel):
    name: str
    path: str

class ChemistryModels(BaseModel):
    models: List[BPXModel]

# A library of all avaible BPX Schema models of their given chemistry
AVAILABLE_BATTERY_MODELS: Dict[str, ChemistryModels] = {
    "NMC": ChemistryModels(models=[
        BPXModel(name="AE_gen1_BPX", path="BatterySimulator/Models/NMC/AE_gen1_BPX.json"),
        BPXModel(name="NMC_Pouch_cell", path="BatterySimulator/Models/NMC/nmc_pouch_cell_BPX.json"),
    ]),
    "LFP": ChemistryModels(models=[
        BPXModel(name="lfp_18650_cell_BPX", path="BatterySimulator/Models/LFP/lfp_18650_cell_BPX.json"),
        BPXModel(name="LFP_model2", path="BatterySimulator/Models/LFP/LFP_model2.json"),
    ]),
}

