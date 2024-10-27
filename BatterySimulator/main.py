from fastapi import FastAPI
from App.API.SimulationController import simulation_app  
import uvicorn

app = FastAPI()

app.mount("/simulate", app=simulation_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084, log_level="debug")