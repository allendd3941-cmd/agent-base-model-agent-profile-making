#perception
import json
from pathlib import Path
import requests
import time 
import threading
from requests.exceptions import ReadTimeout

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"

#收到gama的模擬環境初始結構資料
#資料量如果很大，可先轉成自然語言之後embedding，讓生成出行計畫的時候要用再用
#因為那麼多路的狀態，又不是每條路都有人走，不用全部送到prompt裡面
gama_struc_data="gg"

MODE = "generate"
url = f"http://localhost:11434/api/{MODE}"

USER_PROMPT = f'''
請閱讀以下結構化資料，完整生成以自然語言描述的當前模擬環境狀況。

你需要自我檢查是否有包含完整結構化資料狀況。

結構化資料如下:
{gama_struc_data}
'''