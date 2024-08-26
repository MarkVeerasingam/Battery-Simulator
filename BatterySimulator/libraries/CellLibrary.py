from pydantic import BaseModel
from typing import Dict, List

class BPXModel(BaseModel):
    name: str
    path: str

class ChemistryModels(BaseModel):
    models: List[BPXModel]

# Ensure paths are correct and absolute
AVAILABLE_BATTERY_MODELS: Dict[str, ChemistryModels] = {
    "NMC": ChemistryModels(models=[
        BPXModel(name="AE_gen1_BPX", path="/app/Models/NMC/AE_gen1_BPX.json"),
        BPXModel(name="NMC_Pouch_cell", path="/app/Models/NMC/nmc_pouch_cell_BPX.json"),
    ]),
    "LFP": ChemistryModels(models=[
        BPXModel(name="lfp_18650_cell_BPX", path="/app/Models/LFP/lfp_18650_cell_BPX.json"),
        BPXModel(name="LFP_model2", path="/app/Models/LFP/LFP_model2.json"),
    ]),
}
