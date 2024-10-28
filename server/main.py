from fastapi import FastAPI, Request, HTTPException
import uvicorn
import logging
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()
        
        task_id = payload.get("task_id")
        results = payload.get("results")
        
        logger.info("Task ID: %s", task_id)
        logger.info("Simulation Results: %s", results)
        
        return JSONResponse(content={"message": "success"}, status_code=200)

    except Exception as e:
        logger.error("Error processing webhook: %s", str(e))
        
        raise HTTPException(status_code=500, detail="An error occurred while processing the webhook.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)
