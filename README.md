# Study

## Env

```sh
cd study-code
nv init --python 3.12
nv venv
```

## 1_1 DeepSeek Chat and Stream

```sh
uv add requests python-dotenv
```

## 1_2 Kimi text and image

## 1_3 OpenAI_SDK

```sh
uv add openai
```

```sh
# DeepSeek
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 使用 OpenAI SDK 去使用 deepseek 模型
OPENAI_BASE_URL=${DEEPSEEK_BASE_URL}
OPENAI_API_KEY=${DEEPSEEK_API_KEY}
```

## 1_4 DeepSeek Calculate Tool

example query:

1. 请问你是？
2. 123\*456 等于多数？
3. 我刚刚提的问题是？

## 1_5 Pydantic

```sh
# Mac zsh
uv add 'pydantic[email]'
```

## 1_6 Stream with tool

## 2_1 Tokenizer

```sh
uv add transformers
uv add jinja2
```

## 2_2 Chat with CoT

## 2_3 sync and async

## 2_4 FastAPI

```sh
# install
uv add fastapi 'uvicorn[standard]'
```

```sh
uv run uvicorn 2_4_1_FastAPI-demo:app --reload
```

```md
http://localhost:8000

http://localhost:8000/apps/123?q=ping

http://localhost:8000/apps/error?q=ping
```