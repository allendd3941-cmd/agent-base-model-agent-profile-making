# ollama api
import json
from pathlib import Path
import requests
import time 
import threading
from requests.exceptions import ReadTimeout

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"
USER_PROMPT_PATH = BASE_DIR / "user_prompt.txt"

with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(USER_PROMPT_PATH, "r", encoding="utf-8") as f:
    USER_PROMPT = f.read()

MODE = "generate"
url = f"http://localhost:11434/api/{MODE}"

payload = {
    "model": "school_intern",
    "prompt": USER_PROMPT,
    "system": SYSTEM_PROMPT,
    #"format": "json",  # 強制以 JSON 格式輸出，方便解析
    "think": "low",
    "options": {
        "temperature": 0.8,
        "top_p": 0.9,
        "seed": 42   # 改變 seed 增加多樣性
    },
    "stream": False
}

def print_elapsed_time(start_time, done_event, interval=60):
    while not done_event.wait(interval):
        elapsed = time.perf_counter() - start_time
        print(f"仍在等待 Ollama 回應，已運行 {elapsed:.0f} 秒")

done_event = threading.Event()
start_time = time.perf_counter()

timer_thread = threading.Thread(
    target=print_elapsed_time,
    args=(start_time, done_event),
    daemon=True
)
timer_thread.start()
print("開始等待回應")
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # 確保 HTTP 狀態碼為 200
finally:
    done_event.set()
    timer_thread.join(timeout=1)

elapsed_time = time.perf_counter() - start_time
print(f"已收到 response，總運行時間 {elapsed_time:.2f} 秒")
    
response_data = response.json()
        
with open("agents_samples.json", "w", encoding="utf-8") as f:
    json.dump(response_data, f, ensure_ascii=False, indent=2)
    print("已完成")