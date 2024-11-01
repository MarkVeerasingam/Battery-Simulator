from fastapi import FastAPI, Request, HTTPException
import uvicorn
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

simulation_results_store = {}
def store_simulation_results(task_id, results):
    simulation_results_store[task_id] = results

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    task_id = payload.get("task_id")
    results = payload.get("results")
    status = payload.get("status")
    error = payload.get("error")
    
    if status == "success":
        store_simulation_results(task_id, results)
        logger.info(f"Stored results for task_id {task_id}: {results}")
    elif status == "failure":
        logger.warning(f"Received failure notification for task_id {task_id}: {error}")        
    else:
        logger.warning(f"No results or error received for task_id {task_id}")

    return JSONResponse(content={"message": "success"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
