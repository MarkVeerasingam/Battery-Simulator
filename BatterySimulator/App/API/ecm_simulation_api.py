from fastapi import FastAPI

ecm_app  = FastAPI()

@ecm_app .post("/")
async def read_root():
    return {"message": "ECM Simulation Results will go here"}