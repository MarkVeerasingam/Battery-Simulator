from fastapi import APIRouter
from ecm_test import test_ecm_simulation

ecm_app = APIRouter()

@ecm_app.get("/test")
async def run_ecm_test():
    """
    Endpoint to run the ECM simulation test.
    """
    result = test_ecm_simulation()
    return {"status": "success", "data": result}