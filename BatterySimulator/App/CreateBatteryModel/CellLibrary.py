from pydantic import BaseModel
from typing import Dict, List

class BPXModel(BaseModel):
    name: str
    path: str

class DriveCycle(BaseModel):
    name: str
    path: str

class ChemistryModels(BaseModel):
    models: List[BPXModel]

class ChemistryDriveCycles(BaseModel):
    models: List[DriveCycle]

# A library of all avaible BPX Schema models of their given chemistry
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

# A library of all avaible Drive cycles for models of their given chemistry
AVAILABLE_DRIVE_CYCLES: Dict[str, ChemistryDriveCycles] = {
    "NMC": ChemistryDriveCycles(models=[
        DriveCycle(name="NMC_25degC_1C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_1C.csv"),
        DriveCycle(name="NMC_25degC_2C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_2C.csv"),
        DriveCycle(name="NMC_25degC_Co2", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co2.csv"),
        DriveCycle(name="NMC_25degC_Co20", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co20.csv"),
        DriveCycle(name="NMC_25degC_DriveCycle", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_DriveCycle.csv"),
    ]),
    "LFP": ChemistryDriveCycles(models=[
        DriveCycle(name="LFP_25degC_1C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_1C.csv"),
        DriveCycle(name="LFP_25degC_2C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_2C.csv"),
        DriveCycle(name="LFP_25degC_Co2", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co2.csv"),
        DriveCycle(name="LFP_25degC_Co20", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co20.csv"),
        DriveCycle(name="LFP_25degC_DriveCycle", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_DriveCycle.csv"),
    ])
}