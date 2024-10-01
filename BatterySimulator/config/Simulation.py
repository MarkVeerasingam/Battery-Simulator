from pydantic import BaseModel, StrictStr, Field
from typing import Optional, List

class DriveCycleFile(BaseModel):
    drive_cycle_file: StrictStr = Field(
        ..., 
        description="Drive cycle data file name",
        example="LFP_25degC_1C.csv"
    )

class SimulationConfiguration(BaseModel):
    t_eval: Optional[List[float]] = None  
    experiment: Optional[List[str]] = None 
    drive_cycle: Optional[DriveCycleFile] = None