from fastapi import FastAPI
import uvicorn
from App.api.PhysicsSimulator import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084, log_level="debug")
