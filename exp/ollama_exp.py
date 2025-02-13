import asyncio
import requests
from ollama import AsyncClient

host = 'http://localhost:11434'
model = "llama3.2-vision:latest"

async def chat():
    message = {
        'role': 'user',
        'content': "你好"
    }

    # 启用流式传输
    async for part in await AsyncClient(
            host=host,
    ).chat(model=model, messages=[message], stream=True):
        print(part['message']['content'], end='', flush=True)


# 运行异步函数
asyncio.run(chat())
