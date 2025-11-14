import os

import dotenv
from openai import OpenAI
from pydantic import BaseModel, EmailStr, Field

dotenv.load_dotenv()


class UserInfo(BaseModel):
    """传递用户的信息进行数据提取&处理，涵盖name、age、email"""

    name: str = Field(..., description="用户名字")
    age: int = Field(..., gt=0, description="用户年龄，必须是正整数")
    email: EmailStr = Field(..., description="用户的电子邮件")


client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL"), api_key=os.getenv("DEEPSEEK_API_KEY")
)

model = "deepseek-chat"

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "我叫泽辉呀，今年18岁，我的联系方式是zehuiya@163.com",
        }
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": UserInfo.__name__,
                "description": UserInfo.__doc__,
                "parameters": UserInfo.model_json_schema(),
            },
        }
    ],
    tool_choice={"type": "function", "function": {"name": UserInfo.__name__}},
)

tool_args = response.choices[0].message.tool_calls[0].function.arguments

user_info = UserInfo.model_validate_json(tool_args)

print(user_info)
