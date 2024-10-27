from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from App.API.DTO.SimulationRequest import Physics_SimulationRequest, ECM_SimulationRequest
from App.API.tasks import run_physics_simulation, run_ecm_simulation 
from celery.result import AsyncResult
from config.Utils.logger import setup_logger

simulation_app = FastAPI()

simulation_app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

logger = setup_logger(__name__)

@simulation_app.post("/physics")
async def physics_simulate(request: Physics_SimulationRequest):
    try:
        request_dict = request.dict()
        logger.info("Received request_dict: %s", request_dict)

        task = run_physics_simulation.delay(request_dict)
        return JSONResponse({"task_id": task.id}, status_code=202)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@simulation_app.post("/ecm")
async def ecm_simulate(request: ECM_SimulationRequest):
    try:
        request_dict = request.dict()
        logger.info("Received request_dict: %s", request_dict)

        task = run_ecm_simulation.delay(request_dict)
        return JSONResponse({"task_id": task.id}, status_code=202)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
@simulation_app.post("/webhook")
async def webhook_listener(request: Request):
    if request.method != 'POST':
        raise HTTPException(status_code=400, detail="Method not allowed, only POST is allowed.")
    
    data = await request.json()
    logger.info("Received webhook notification: %s", data)

    return JSONResponse({"status": "received"}, status_code=200)
    
# @simulation_app.get("/results/{task_id}")
# async def get_result(task_id: str):
#     result = AsyncResult(task_id)
#     if result.state == 'PENDING':
#         return JSONResponse({"task_id": task_id, "status": "pending"}, status_code=202)
#     elif result.state != 'FAILURE':
#         return JSONResponse({"task_id": task_id, "status": result.state, "result": result.result}, status_code=200)
#     else:
#         return JSONResponse({"task_id": task_id, "status": "failure", "error": str(result.result)}, status_code=500)