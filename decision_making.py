#decision making
from RAG import RAG
from agent_profile import run_agent_profile
from perception import run_perception
import json
from pathlib import Path
from timer import print_elapsed_time
import threading
import time 
import requests

BASE_DIR = Path(__file__).resolve().parent

SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"

with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

MODE = "generate"
url = f"http://localhost:11434/api/{MODE}"

def run_decision_making(agent_profile_data, perception_data, json_output: bool= False):
    #在單測檔案的時候再uncommand
    # agent_profile_data = run_agent_profile()
    # perception_data = run_perception()

    retrieved_texts =RAG(agent_profile_data, perception_data)

    USER_PROMPT = f"""
    請幫我依據以下資料，生成每位agents的完整出行計畫。
    格式如下:
    待補
    資料如下:
    {retrieved_texts}
    """
    payload = {
    "model": "gpt-oss:20b",
    "prompt": USER_PROMPT,
    "system": SYSTEM_PROMPT,
    #"format": "json",  # 強制以 JSON 格式輸出，方便解析
    "think": "low",
    "options": {
        "seed": 42   # 改變 seed 增加多樣性
    },
    "stream": False
    }

    done_event = threading.Event()
    start_time = time.perf_counter()

    timer_thread = threading.Thread(
        target=print_elapsed_time,
        args=(start_time, done_event),
        daemon=True
    )
    timer_thread.start()
    print("開始等待decision_making回應")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 確保 HTTP 狀態碼為 200
    finally:
        done_event.set()
        timer_thread.join(timeout=1)

    elapsed_time = time.perf_counter() - start_time
    print(f"已收到 response，decision_making總運行時間 {elapsed_time:.2f} 秒")

    decision_making_response = response.text

    if json_output:
        response_data = response.json()
        print(response_data)
        raw_text = response_data.get("response", "").strip()

        # print("Ollama 原始 response 前 500 字：")
        # print(repr(raw_text[:500]))

        if not raw_text:
            raise ValueError("Ollama decision_making response 是空的，無法解析 JSON")

        agents = json.loads(raw_text)
                
        with open("decision_making.json", "w", encoding="utf-8") as f:
            json.dump({"decision_making":agents}, f, ensure_ascii=False, indent=2)
            print("已完成decision_making")
            
    return decision_making_response

if __name__ == "__main__":
    run_decision_making(json_output=False)

#agent profile 的 response還要改，目前的prompt是叫他生成json