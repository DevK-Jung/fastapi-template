from collections.abc import AsyncGenerator
from typing import List, Dict, Optional

import litellm

from fastapi_template.core.util.id_generator import generate_run_id
from fastapi_template.infra.llm.model.llm_model import AIChunkModel


class LLMClient:
    def __init__(self, model: str, api_base: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model
        self.api_base = api_base
        self.api_key = api_key

    async def chat_stream(self,
                          prompt: Optional[str] = None,
                          messages: Optional[List[Dict[str, str]]] = None,
                          system_prompt: Optional[str] = None,
                          temperature: float = 0.7,
                          max_tokens: Optional[int] = None) -> AsyncGenerator[AIChunkModel]:
        """Streaming 호출 전용"""
        msg_list = self._build_messages(prompt, messages, system_prompt)

        _id = generate_run_id()

        response = await litellm.acompletion(
            model=self.model,
            messages=msg_list,
            api_key=self.api_key,
            api_base=self.api_base,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        async for chunk in response:
            content = chunk.choices[0].delta.get("content", "")
            if content:
                yield AIChunkModel(content=content, id=_id)

    def chat(self,
             prompt: Optional[str] = None,
             messages: Optional[List[Dict[str, str]]] = None,
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> str:
        """일반 호출 전용"""
        msg_list = self._build_messages(prompt, messages, system_prompt)

        response = litellm.completion(
            model=self.model,
            messages=msg_list,
            api_key=self.api_key,
            api_base=self.api_base,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )

        return response['choices'][0]['message']['content']

    @staticmethod
    def _build_messages(prompt, messages, system_prompt):
        msg_list = []
        if system_prompt:  # 시스템 프롬프트
            msg_list.append({"role": "system", "content": system_prompt})
        if messages:  # 전체 대화 기록
            msg_list.extend(messages)
        elif prompt:  # 단순 사용자 질문
            msg_list.append({"role": "user", "content": prompt})
        return msg_list
