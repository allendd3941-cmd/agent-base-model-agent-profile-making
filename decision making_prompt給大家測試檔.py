#decision making
import json
from pathlib import Path
import threading
import time 
import requests

#system prompt打在這
SYSTEM_PROMPT = """

"""

#你要他做的是打在這
USER_PROMPT = f"""
哈囉

"""

MODE = "generate"
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
url = f"http://localhost:11434/api/{MODE}"

def print_elapsed_time(start_time, done_event, interval=60):
    while not done_event.wait(interval):
        elapsed = time.perf_counter() - start_time
        print(f"仍在等待 Ollama 回應，已運行 {elapsed:.0f} 秒")

def run_decision_making(json_output: bool= False, only_response: bool=False):
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
    
    if only_response:
        response = response.json()
        decision_making_response = response["response"]
    else:
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
    response = run_decision_making(json_output=False,only_response=True)
    print(response)
