#timer
import time 
def print_elapsed_time(start_time, done_event, interval=60):
    while not done_event.wait(interval):
        elapsed = time.perf_counter() - start_time
        print(f"仍在等待 Ollama 回應，已運行 {elapsed:.0f} 秒")