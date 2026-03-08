import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import json

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL")
        self.model = os.getenv("LLM_MODEL", "deepseek-chat")
        
        if not self.api_key or self.api_key == "your_api_key_here":
            print("Warning: LLM_API_KEY is not set. LLM features will not work.")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    async def generate_response(self, query: str, context: str):
        """
        Generate a structured response using the LLM based on the provided context.
        """
        if not self.client:
            return {
                "answer": "API Key 未配置，无法调用大模型。请在 backend/.env 文件中配置 LLM_API_KEY。",
                "suggested_actions": [],
                "related_conditions": []
            }

        system_prompt = """
        你是一个专业的个人健康助手。请基于提供的【权威上下文】回答用户的【问题】。
        
        你的回答必须严格遵守以下规则：
        1. 优先依据提供的上下文回答。
        2. 如果上下文不包含相关信息（或提示使用通用知识），请基于你的通用医学知识回答，但必须在回答开头声明：'（注：以下内容基于通用医学知识，非本地权威指南）'。
        3. 语言通俗易懂，但必须保持医学严谨性。
        4. 即使上下文很短，也要尽量组织成流畅的语言。
        5. 最后必须以 JSON 格式输出，不要包含 Markdown 代码块标记（如 ```json）。
        
        JSON 输出格式要求：
        {
            "answer": "这里是你的核心回答文本...",
            "suggested_actions": ["建议1", "建议2"],
            "related_conditions": ["相关疾病1", "相关疾病2"]
        }
        """

        user_prompt = f"""
        【权威上下文】:
        {context}

        【问题】:
        {query}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Simple cleanup if LLM wraps in code blocks despite instructions
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return {
                "answer": f"抱歉，生成回答时出现错误：{str(e)}",
                "suggested_actions": ["重试", "联系管理员"],
                "related_conditions": []
            }

    async def stream_response(self, query: str, context: str):
        """
        Stream the response text from LLM.
        Note: Streaming mode focuses on the text answer to ensure smooth UX.
        Structured data (actions) are omitted in this mode for simplicity or could be extracted later.
        """
        if not self.client:
            yield "API Key 未配置，无法调用大模型。"
            return

        system_prompt = """
        你是一个专业的个人健康助手。请基于提供的【权威上下文】回答用户的【问题】。
        
        你的回答必须严格遵守以下规则：
        1. 优先依据提供的上下文回答。
        2. 如果上下文不包含相关信息（或提示使用通用知识），请基于你的通用医学知识回答，但必须在回答开头声明：'（注：以下内容基于通用医学知识，非本地权威指南）'。
        3. 语言通俗易懂，但必须保持医学严谨性。
        4. 直接输出回答内容，不要输出 JSON，也不要包含 "answer": 等前缀。
        """

        user_prompt = f"""
        【权威上下文】:
        {context}

        【问题】:
        {query}
        """

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
        except Exception as e:
            print(f"LLM Stream Error: {e}")
            yield f" [生成出错: {str(e)}]"


llm_service = LLMService()
