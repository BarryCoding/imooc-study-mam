# Study

## Env

```sh
cd study-code
nv init --python 3.12
nv venv
```

## 1_DeepSeek_API

```sh
uv add requests python-dotenv
```

## 3_OpenAI_SDK

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
