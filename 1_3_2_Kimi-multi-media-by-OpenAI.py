import base64
import os

import dotenv
import requests
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    base_url=os.getenv("MOONSHOT_BASE_URL"), api_key=os.getenv("MOONSHOT_API_KEY")
)

model = "moonshot-v1-8k-vision-preview"

image_path = "./resources/广州塔.jpeg"

with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# 使用python标准的base64.b64encode函数将图片编码成base64字符串
image_base64 = base64.b64encode(image_data).decode("utf-8")
image_url = f"data:image/jpeg;base64,{image_base64}"

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述下这张图片，这张图片所在位置是哪里呢?"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }
    ],
)

print(response.choices[0].message.content)
