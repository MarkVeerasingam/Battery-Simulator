from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import Dict

class BatteryConfiguration(BaseModel):
    battery_chemistry: StrictStr = Field(
        ..., 
        description="The chemistry name of the battery model",
        example="LFP"
    )
    bpx_battery_models: StrictStr = Field(
        ..., 
        description="The specific battery model name",
        example="lfp_18650_cell_BPX"
    )
    electrochemical_model: StrictStr = Field(
        ..., 
        description="The name of the electrochemical model",
        example="DFN"
    )

class SolverConfiguration(BaseModel):
    solver: StrictStr = Field(
    ..., 
    description="The solver used for simulation",
    example="CasadiSolver"
    )
    tolerance: Dict[str, StrictFloat] = Field(
        default={"atol": 1e-6, "rtol": 1e-6},
        description="Tolerance settings for the solver"
    )

class DriveCycleData(BaseModel):
    drive_cycle_data: Dict[StrictStr, StrictStr] = Field(
        description="Drive cycle data for each models chemistry",
        example={
            "LFP_25degC_1C": "BatterySimulator/Models/LFP/data/validation/LFP_25degC_1C.csv"
        }
    )

# print(BatteryConfiguration.schema_json(indent=2))
# print(BPXBatteryModels.schema_json(indent=2))