from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from App.Simulations.ECMSimulationRunner import SimulationRunner
from config.ParameterValues.ParameterValues import ParameterValueConfiguration
from config.Models.EquivalentCircuitModel import ECMConfiguration
from config.Simulation import SimulationConfiguration
from config.Solver import SolverConfiguration
from typing import Optional, List
import pybamm

ecm_app = FastAPI()

# Enable CORS
ecm_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    equivalent_circuit_model: ECMConfiguration
    parameter_values: ParameterValueConfiguration
    solver: SolverConfiguration
    simulation: SimulationConfiguration
    display_params: Optional[List[str]] = None

pybamm.set_logging_level("INFO")

@ecm_app.post("/")
async def simulate(request: SimulationRequest):
    try:
        parameter_value_config = request.parameter_values
        equivalent_circuit_model_config = request.equivalent_circuit_model
        solver_config = request.solver
        simulation_config = request.simulation

        sim_runner = SimulationRunner(parameter_value_config=parameter_value_config,
                                      solver_config=solver_config,
                                      ecm_config=equivalent_circuit_model_config)
        
        sim_runner.run_simulation(simulation_config)

        display_params = request.display_params or ["Voltage [V]", "Current [A]", "Jig temperature [K]"]
        results = sim_runner.display_results(display_params)
        
        return results
    
    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")