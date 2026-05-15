from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from agent_profile import run_agent_profile
from perception import run_perception
from decision_making import run_decision_making
from od_converter import convert_to_od_csv

BASE_DIR = Path(__file__).resolve().parent
AGENT_PROFILE_DIR = BASE_DIR / "output" / "agent_profile_output_1.txt"
OUTPUT_PATH = BASE_DIR / "output" 

if not AGENT_PROFILE_DIR.exists:
    run_agent_profile(output=True)

#uvicorn server:app --host 127.0.0.1 --port 8000 --reload
#檔名:伺服器名 -> server:app
app = FastAPI()

class GamaRequest(BaseModel):
    cycle: int
    vehicles: int
    # memory: str #收到之後combine進agent profile然後再進short term memory


#要寫一個迴圈，step總數到了就要break
@app.post("/from-gama")
def receive_from_gama(gama_body: GamaRequest):
    print("收到 GAMA 請求:\n", gama_body)
    #decision_making = "test success"
    agent_profile = Path.read_text(AGENT_PROFILE_DIR, encoding="utf-8")

    perception = run_perception(gama_body, output=True)
    decision_making = run_decision_making(agent_profile, perception, output=True)
    action = convert_to_od_csv(source=decision_making, output_csv=OUTPUT_PATH / "final_od.csv")
    action_response = action[0] #出發點(o)、目的地(d)、出發時間

    return action_response




