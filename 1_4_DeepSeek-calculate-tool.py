import json
import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()


def calculator(expression: str) -> str:
    """一个简单的计算器，可以执行数学表达式"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": f"无效表达式, 错误信息: {str(e)}"})


class ReActAgent:
    def __init__(self):
        self.model = "deepseek-chat"
        self.client = OpenAI(
            base_url=os.getenv("DEEPSEEK_BASE_URL"),
            api_key=os.getenv("DEEPSEEK_API_KEY"),
        )

        self.messages = [
            {
                "role": "system",
                "content": "你是一个强大的聊天机器人，请根据用户的提问进行答复，如果需要调用工具请直接调用，不知道请直接回复不清楚",
            }
        ]

        self.available_tools = {"calculator": calculator}
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "一个简单的计算器，可以执行数学表达式",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "需要计算的数学表达式，例如：'123+456+789'",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            }
        ]

    def process_query(self, query: str) -> str:
        """使用deepseek处理用户输出"""
        self.messages.append({"role": "user", "content": query})

        # 调用deepseek发起请求
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
        )

        # 获取响应消息+工具响应
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 将模型第一次回复添加到历史消息中
        self.messages.append(response_message.model_dump())

        # 如果存在工具调用，则调用工具
        if tool_calls:
            # 循环执行工具调用
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                print("Tool Call: ", tool_name)
                tool_args = json.loads(tool_call.function.arguments)
                print("Tool Args: ", tool_args)
                # 调用工具
                tool_result = self.available_tools[tool_name](**tool_args)
                print("Tool Result: ", tool_result)

                # 将工具结果添加到历史消息中
                self.messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_result,
                    }
                )

            # 再次调用模型，让它基于工具调用的结果生成最终回复内容
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="none",  # 不使用工具，只使用模型生成回复
            )

            self.messages.append(second_response.choices[0].message.model_dump())
            return "Assistant: " + second_response.choices[0].message.content
        # 如果不需要工具调用，则直接返回模型生成的回复
        else:
            return "Assistant: " + response_message.content

    def chat_loop(self):
        """运行循环对话"""
        while True:
            try:
                # 获取用户的输入
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                print(self.process_query(query))
            except Exception as e:
                print(f"\nError: {str(e)}")


if __name__ == "__main__":
    ReActAgent().chat_loop()
