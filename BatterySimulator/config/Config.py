from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import Dict, Optional, List

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

class ElectrochemicalConfiguration(BaseModel):
    electrochemical_model: StrictStr = Field(
        default="DFN",
        description="The name of the electrochemical model",
        example="DFN"
    )
    # set these as optional, however the default pybamm options of the electrochemical is cell_geometry: 'arbitrary', thermal: 'isothermal'
    # https://docs.pybamm.org/en/stable/source/examples/notebooks/models/using-model-options_thermal-example.html
    thermal_model: Optional[StrictStr] = Field(
        description="The thermal model option for the battery simulation",
        example="isothermal"
    )
    cell_geometry: Optional[StrictStr] = Field(
        description="The cell geometry option for the battery simulation",
        example="arbitrary"
    )

class SolverConfiguration(BaseModel):
    solver: StrictStr = Field(
        ..., 
        description="The solver used for simulation",
        example="CasadiSolver"
    )
    tolerance: Dict[str, StrictFloat] = Field(
        default={"atol": 1e-6, "rtol": 1e-6},
        description="The relative and absolute tolerance for the solver, default is 1e-6."
    )
    mode: Optional[StrictStr] = Field(
        default="safe",
        description="The solver speed of CasadiSolver, can be fast or safe. Default is safe.",
        example="safe"
    )

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