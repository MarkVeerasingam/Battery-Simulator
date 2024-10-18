from pydantic import BaseModel, StrictStr, Field
from typing import Optional, List

class DriveCycleFile(BaseModel):
    drive_cycle_file: StrictStr = Field(
        ...,
        description="Drive cycle data file name",
        example="LFP_25degC_1C.csv"
    )

class SimulationConfiguration(BaseModel):
    drive_cycle: Optional[DriveCycleFile] = None
    experiment: Optional[List[str]] = Field(
        default=None,
        description="List of experimental conditions.",
        example=[
            "Discharge at C/5 for 10 hours or until 2.5 V",
            "Rest for 1 hour",
            "Charge at 1 A until 3.5 V",
            "Hold at 3.5 V until 10 mA",
            "Rest for 1 hour"
        ]
    )
    t_eval: Optional[List[int]] = Field(
        default=None,
        description="Time evaluation conditions for the simulation.",
        example=[0, 7200]
    )