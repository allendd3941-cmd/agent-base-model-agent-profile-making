# ollama api
import json
from pathlib import Path
import requests
import time 
from timer import print_elapsed_time
import threading
from requests.exceptions import ReadTimeout
from RAG import RAG
from llm_config import OLLAMA_URL, OLLAMA_MODE, OLLAMA_MODEL


BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"
USER_PROMPT_PATH = BASE_DIR / "user_prompt.txt"

with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(USER_PROMPT_PATH, "r", encoding="utf-8") as f:
    USER_PROMPT = f.read()

# MODE = "generate"
# url = f"http://localhost:11434/api/{MODE}"

def run_agent_profile(json_output: bool= False):
    url = f"{OLLAMA_URL}{OLLAMA_MODE}"

    payload = {
        "model": OLLAMA_MODEL,
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
    print("開始等待agent profile回應")
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 確保 HTTP 狀態碼為 200
    finally:
        done_event.set()
        timer_thread.join(timeout=1)

    elapsed_time = time.perf_counter() - start_time
    print(f"已收到 response，agent profile總運行時間 {elapsed_time:.2f} 秒")
        
    agent_profile_response = response.text

    if json_output:
        response_data = response.json()
        print(response_data)
        raw_text = response_data.get("response", "").strip()

        # print("Ollama 原始 response 前 500 字：")
        # print(repr(raw_text[:500]))

        if not raw_text:
            raise ValueError("Ollama agent profile response 是空的，無法解析 JSON")

        agents = json.loads(raw_text)
                
        with open("agents_samples.json", "w", encoding="utf-8") as f:
            json.dump({"agents":agents}, f, ensure_ascii=False, indent=2)
            print("已完成agent profile")
    return agent_profile_response

if __name__ == "__main__":
    run_agent_profile(json_output=False)

