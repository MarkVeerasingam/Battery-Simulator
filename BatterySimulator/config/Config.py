from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import Dict, Optional

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

# need to make this so we can filter what chemistry that is availble for a given drive cycle
# The difference between declaring this class and not one for Battery BPX models is that
# 'BatteryConfiguration class already includes the necessary fields to specify the battery 
# chemistry and model, leveraging the AVAILABLE_BATTERY_MODELS dictionary to validate and load the appropriate file.
class DriveCycleFile(BaseModel):
    chemistry: StrictStr = Field(
        ..., 
        description="Chemistry of the battery for the drive cycle",
        example="LFP"
    )
    drive_cycle_file: StrictStr = Field(
        ..., 
        description="Drive cycle data file name",
        example="LFP_25degC_1C.csv"
    )

class SimulationConfiguration(BaseModel):
    t_eval: Optional[Dict[str, float]]= None
    experiment: Optional[str] = None
    drive_cycle: Optional[DriveCycleFile] = None

# print(BatteryConfiguration.schema_json(indent=2))
# print(BPXBatteryModels.schema_json(indent=2))s