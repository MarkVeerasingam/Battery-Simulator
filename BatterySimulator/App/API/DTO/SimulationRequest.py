from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4

class ECM_SimulationRequest(BaseModel):
    user_id: str
    task_id: str   
    equivalent_circuit_model: ECMConfiguration
    parameter_values: ParameterValueConfiguration
    solver: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]]

class Physics_SimulationRequest(BaseModel):
    user_id: str
    task_id: str 
    parameter_values: ParameterValueConfiguration 
    electrochemical_model: ElectrochemicalModelConfiguration 
    solver_model: SolverConfiguration
    simulation: SimulationConfiguration 
    display_params: Optional[List[str]] 