from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
# from agent_profile import run_agent_profile
# from perception import run_perception
# from decision_making import run_decision_making

BASE_DIR = Path(__file__).resolve().parent
AGENT_PROFILE_DIR = BASE_DIR / "output" / "agent_profile_output_1.txt"

# if not AGENT_PROFILE_DIR.exists:
#     run_agent_profile(output=True)

#uvicorn server:app --host 127.0.0.1 --port 8000 --reload
#檔名:伺服器名 -> server:app
app = FastAPI()

class GamaRequest(BaseModel):
    cycle: int
    vehicles: int
    # memory: str #收到之後combine進agent profile然後再進short term memory

@app.post("/from-gama")
def receive_from_gama(gama_body: GamaRequest):
    print("收到 GAMA 請求")
    decision_making = "test success"
    # agent_profile = Path.read_text(AGENT_PROFILE_DIR, encoding="utf-8")

    # perception = run_perception(gama_body, output=False)
    # decision_making = run_decision_making(agent_profile, perception, output=False)

    return decision_making




