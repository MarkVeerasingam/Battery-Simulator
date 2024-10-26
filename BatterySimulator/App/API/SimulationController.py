from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
from App.API.SimulationService import SimulationService
from celery.result import AsyncResult
import logging

simulation_app = FastAPI()

simulation_app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@simulation_app.post("/physics")
async def physics_simulate(request: Physics_SimulationRequest):
    try:
        request_dict = request.dict()

        logger.info("Received request_dict: %s", request_dict)

        
        task = SimulationService.run_physics_simulation.delay(request_dict)
        return JSONResponse({"task_id": task.id}, status_code=202)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@simulation_app.post("/ecm")
async def ecm_simulate(request: ECM_SimulationRequest):
    try:
        request_dict = request.dict()

        logger.info("Received request_dict: %s", request_dict)
        
        task = SimulationService.run_ecm_simulation.delay(request_dict)
        return JSONResponse({"task_id": task.id}, status_code=202)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@simulation_app.get("/results/{task_id}")
async def get_result(task_id: str):
    result = AsyncResult(task_id)
    if result.state == 'PENDING':
        return JSONResponse({"task_id": task_id, "status": "pending"}, status_code=202)
    elif result.state != 'FAILURE':
        return JSONResponse({"task_id": task_id, "status": result.state, "result": result.result}, status_code=200)
    else:
        return JSONResponse({"task_id": task_id, "status": "failure", "error": str(result.result)}, status_code=500)

