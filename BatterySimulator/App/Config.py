from pydantic import BaseModel, StrictStr, StrictFloat

class Configuration(BaseModel):
    battery_model: StrictStr
    electrochemical_model: StrictStr
    solver: StrictStr
    atol: StrictFloat = 1e-6
    rtol: StrictFloat = 1e-6