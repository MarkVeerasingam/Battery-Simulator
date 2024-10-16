from fastapi import FastAPI
import uvicorn
from App.API.physics_simulation_api import physics_app
from App.API.ecm_simulation_api import ecm_app 

app = FastAPI()

# Mount sub-apps
app.mount("/simulate/physics", physics_app)
app.mount("/simulate/ecm", ecm_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084, log_level="debug")
