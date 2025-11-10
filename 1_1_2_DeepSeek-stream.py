import os

import dotenv
import requests

dotenv.load_dotenv()

with requests.request(
    "POST",
    "https://api.deepseek.com/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
    },
    json={
        "model": "deepseek-reasoner",
        "messages": [{"role": "user", "content": "你好，你是?"}],
        "stream": True,  # 流式输出
    },
) as response:
    for line in response.iter_lines(decode_unicode=True):
        if line:
            if line.startswith("data:"):
                data = line.lstrip("data:").strip()
                print("data:", data)
