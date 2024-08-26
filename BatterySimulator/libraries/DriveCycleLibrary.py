from pydantic import BaseModel
from typing import Dict, List

class DriveCycle(BaseModel):
    name: str
    path: str

# class ChemistryDriveCycles(BaseModel):
#     driveCycle: List[DriveCycle]

# A library of all avaible Drive cycles for models of their given chemistry
# AVAILABLE_DRIVE_CYCLES: Dict[str, ChemistryDriveCycles] = {
#     "NMC": ChemistryDriveCycles(driveCycle=[
#         DriveCycle(name="NMC_25degC_1C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_1C.csv"),
#         DriveCycle(name="NMC_25degC_2C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_2C.csv"),
#         DriveCycle(name="NMC_25degC_Co2", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co2.csv"),
#         DriveCycle(name="NMC_25degC_Co20", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co20.csv"),
#         DriveCycle(name="NMC_25degC_DriveCycle", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_DriveCycle.csv"),
#     ]),
#     "LFP": ChemistryDriveCycles(driveCycle=[
#         DriveCycle(name="LFP_25degC_1C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_1C.csv"),
#         DriveCycle(name="LFP_25degC_2C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_2C.csv"),
#         DriveCycle(name="LFP_25degC_Co2", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co2.csv"),
#         DriveCycle(name="LFP_25degC_Co20", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co20.csv"),
#         DriveCycle(name="LFP_25degC_DriveCycle", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_DriveCycle.csv"),
#     ])
# }
    
# removed the filter by chemistry approach. More generalistic now
AVAILABLE_DRIVE_CYCLES: List[DriveCycle] = [
        DriveCycle(name="NMC_25degC_1C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_1C.csv"),
        DriveCycle(name="NMC_25degC_2C", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_2C.csv"),
        DriveCycle(name="NMC_25degC_Co2", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co2.csv"),
        DriveCycle(name="NMC_25degC_Co20", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_Co20.csv"),
        DriveCycle(name="NMC_25degC_DriveCycle", path="BatterySimulator/Models/NMC/data/validation/NMC_25degC_DriveCycle.csv"),
        DriveCycle(name="LFP_25degC_1C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_1C.csv"),
        DriveCycle(name="LFP_25degC_2C", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_2C.csv"),
        DriveCycle(name="LFP_25degC_Co2", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co2.csv"),
        DriveCycle(name="LFP_25degC_Co20", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_Co20.csv"),
        DriveCycle(name="LFP_25degC_DriveCycle", path="BatterySimulator/Models/LFP/data/validation/LFP_25degC_DriveCycle.csv"),
]