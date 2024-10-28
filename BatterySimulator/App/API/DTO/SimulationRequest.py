from App.Simulations.ECMSimulationRunner import ECM_SimulationRunner
from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Models.PhysicsBasedModel import ElectrochemicalModelConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from pydantic import BaseModel
from typing import Optional, List
import uuid

class BaseSimulationRequest(BaseModel):
    task_id: Optional[str] = None

    def generate_task_id(self):
        if not self.task_id:
            self.task_id = str(uuid.uuid4()) 

class ECM_SimulationRequest(BaseSimulationRequest):
    equivalent_circuit_model: ECMConfiguration
    parameter_values: ParameterValueConfiguration
    solver: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]]

class Physics_SimulationRequest(BaseSimulationRequest):
    parameter_values: ParameterValueConfiguration 
    electrochemical_model: ElectrochemicalModelConfiguration 
    solver_model: SolverConfiguration
    simulation: SimulationConfiguration 
    display_params: Optional[List[str]] 