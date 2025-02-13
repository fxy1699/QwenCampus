import asyncio
import httpx
from pydantic import BaseModel
from ollama import AsyncClient


# 定义结构化输出的 Pydantic 模型
class Object(BaseModel):
    name: str
    confidence: float
    attributes: str


class ImageDescription(BaseModel):
    summary: str
    objects: list[Object]
    scene: str
    colors: list[str]
    time_of_day: str
    setting: str
    text_content: str | None = None


async def main():
    # 获取网络图片的 URL
    image_url = input("请输入图片的 URL: ")

    # 下载图片内容
    async with httpx.AsyncClient() as client_http:
        response = await client_http.get(image_url)
        response.raise_for_status()  # 确保请求成功
        image_data = response.content  # 获取图片的二进制数据

    # 初始化异步客户端
    client = AsyncClient()

    # 定义结构化输出的 schema
    schema = ImageDescription.model_json_schema()

    # 调用多模态模型进行图片分析
    # 注意：client.chat 是一个协程，需要先调用它，获取返回的异步迭代器
    async_chat_response = client.chat(
        model="llama3.2-vision",  # 使用支持视觉的模型
        messages=[
            {
                "role": "user",
                "content": "Analyze this image and return a detailed JSON description including objects, scene, colors and any text detected. If you cannot determine certain details, leave those fields empty.",
                "images": [image_data],  # 传递图片数据
            }
        ],
        format=schema,  # 使用 Pydantic 生成的 schema
        options={"temperature": 0},  # 设置温度为 0，使输出更确定
        stream=True,  # 启用流式传输
    )

    # 使用 await 调用协程，获取异步迭代器
    async for part in await async_chat_response:
        # 打印流式传输的每部分结果
        print(part.message.content, end="", flush=True)

    print("\n分析完成！")


if __name__ == "__main__":
    asyncio.run(main())