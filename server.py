from fastapi import FastAPI
from pydantic import BaseModel
from agent_profile import run_agent_profile
from perception import run_perception
from decision_making import run_decision_making

#uvicorn server:app --host 127.0.0.1 --port 8000 --reload
#檔名:伺服器名 -> server:app
app = FastAPI()

class GamaRequest(BaseModel):
    cycle: int
    agent_id: str
    x: float
    y: float
    value: float

@app.post("/from-gama")
def receive_from_gama(gama_body: GamaRequest):
    print("收到 GAMA 請求")

    agent_profile = run_agent_profile(output=False)
    perception = run_perception(gama_body, output=False)
    decision_making = run_decision_making(agent_profile, perception, output=False)

    return decision_making




