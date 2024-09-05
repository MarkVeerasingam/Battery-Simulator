from pydantic import BaseModel
from typing import Dict, List

class DriveCycle(BaseModel):
    name: str
    path: str

AVAILABLE_DRIVE_CYCLES: List[DriveCycle] = [
        DriveCycle(name="NMC_25degC_1C", path="/app/Models/NMC/data/validation/NMC_25degC_1C.csv"),
        DriveCycle(name="NMC_25degC_2C", path="/app/Models/NMC/data/validation/NMC_25degC_2C.csv"),
        DriveCycle(name="NMC_25degC_Co2", path="/app/Models/NMC/data/validation/NMC_25degC_Co2.csv"),
        DriveCycle(name="NMC_25degC_Co20", path="/app/Models/NMC/data/validation/NMC_25degC_Co20.csv"),
        DriveCycle(name="NMC_25degC_DriveCycle", path="/app/Models/NMC/data/validation/NMC_25degC_DriveCycle.csv"),
        DriveCycle(name="LFP_25degC_1C", path="/app/Models/LFP/data/validation/LFP_25degC_1C.csv"),
        DriveCycle(name="LFP_25degC_2C", path="/app/Models/LFP/data/validation/LFP_25degC_2C.csv"),
        DriveCycle(name="LFP_25degC_Co2", path="/app/Models/LFP/data/validation/LFP_25degC_Co2.csv"),
        DriveCycle(name="LFP_25degC_Co20", path="/app/Models/LFP/data/validation/LFP_25degC_Co20.csv"),
        DriveCycle(name="LFP_25degC_DriveCycle", path="/app/Models/LFP/data/validation/LFP_25degC_DriveCycle.csv"),
]