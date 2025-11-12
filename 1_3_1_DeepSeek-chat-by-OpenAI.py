import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL"), api_key=os.getenv("DEEPSEEK_API_KEY")
)

model = "deepseek-reasoner"

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "你好，你是?"}],
)

print("推理内容:", response.choices[0].message.reasoning_content)
print("最终答案:", response.choices[0].message.content)
