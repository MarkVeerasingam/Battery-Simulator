from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
from App.API.SimulationService import SimulationService
import pybamm

simulation_app = FastAPI()

simulation_app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pybamm.set_logging_level("INFO")

@simulation_app.post("/physics")
async def physics_simulate(request: Physics_SimulationRequest):
    try:
        results = SimulationService.run_physics_simulation(request)
        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@simulation_app.post("/ecm")
async def ecm_simulate(request: ECM_SimulationRequest):
    try:
        results = SimulationService.run_ecm_simulation(request)
        return results

    except pybamm.SolverError as e:
        raise HTTPException(status_code=500, detail=f"SolverError occurred: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")