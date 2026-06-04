"""LLM 服务 - 通过 OpenAI 兼容接口调用大模型"""

from openai import AsyncOpenAI
from typing import AsyncGenerator

from app.config import settings

# 创建 OpenAI 兼容客户端
_client: AsyncOpenAI | None = None


def get_llm_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
        )
    return _client


SYSTEM_PROMPT_TEMPLATE = """你是"{avatar_name}"，灵山胜境景区的AI导游。

## 你的特点
{personality}

## 对话要求
1. 根据提供的知识库内容准确回答游客问题
2. 语言生动有趣，像一位专业且亲切的导游
3. 如果知识库中没有相关信息，诚实告知并提供有用的建议
4. 回答控制在200字以内，适合语音播报
5. 适当使用emoji增添趣味性

## 参考知识
{context}
"""


async def chat_completion(
    message: str,
    context: str = "",
    history: list[dict] = None,
    avatar_name: str = "小灵",
    personality: str = "热情友善，知识渊博，善于用生动的语言描述景区特色。",
) -> str:
    """同步对话生成"""
    client = get_llm_client()

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        avatar_name=avatar_name,
        personality=personality,
        context=context if context else "暂无特定知识库内容，请根据你的导游知识回答。",
    )

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history[-10:])  # 保留最近5轮对话
    messages.append({"role": "user", "content": message})

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content


async def chat_completion_stream(
    message: str,
    context: str = "",
    history: list[dict] = None,
    avatar_name: str = "小灵",
    personality: str = "热情友善，知识渊博。",
) -> AsyncGenerator[str, None]:
    """流式对话生成"""
    client = get_llm_client()

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        avatar_name=avatar_name,
        personality=personality,
        context=context if context else "暂无特定知识库内容。",
    )

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history[-10:])
    messages.append({"role": "user", "content": message})

    stream = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=500,
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
