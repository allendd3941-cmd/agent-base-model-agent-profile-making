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
哈囉你好大家好

"""

MODE = "generate"
url = f"http://localhost:11434/api/{MODE}"

payload = {
"model": "gpt-oss:20b",
"prompt": USER_PROMPT,
"system": SYSTEM_PROMPT,
#"format": "json",  
"think": "low",
"options": {
    "seed": 42   
},
"stream": False
}

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
    response_text = response.text

    if only_response:
        decision_making_response = response_data["response"]
    else:
        decision_making_response = response_text

    if json_output:
        print(response_data)
        raw_text = response_data.get("response", "").strip()

        # print("Ollama 原始 response 前 500 字：")
        # print(repr(raw_text[:500]))

        if not raw_text:
            raise ValueError("Ollama response 是空的，無法解析 JSON")

        agents = json.loads(raw_text)
                
        with open("test_output.json", "w", encoding="utf-8") as f:
            json.dump({"test_output":agents}, f, ensure_ascii=False, indent=2)
            print("已完成")
            
    return decision_making_response

if __name__ == "__main__":
    response = run_decision_making(json_output=True,only_response=True)
    print(response)
