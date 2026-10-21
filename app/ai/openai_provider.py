from openai import AsyncOpenAI
from app.ai.models import AIRequest, AIResponse, ToolCall, ToolResult, ToolDefinition
from app.config import settings
from app.ai.llm_provider import LLMProvider

from typing import TypeVar

from pydantic import BaseModel

import json


T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(LLMProvider):

    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
        )

    async def generate(self, request: AIRequest) -> AIResponse:
        tools = []

        for tool in request.tools:
            tools.append(
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                    "strict": True
                }
            )

        response = await self.client.responses.create(
            model=settings.openai_model,
            instructions=request.instructions,
            input=request.input,
            tools=tools
        )
        
        tool_calls = []

        for item in response.output:
            if item.type == "function_call":
                tool_calls.append(
                    ToolCall(
                        name=item.name,
                        arguments=json.loads(item.arguments),
                        call_id=item.call_id,
                    )
                )

        return self._build_ai_response(response)

    async def generate_structured(self, request: AIRequest, output_type: type[T]) -> T:
        response = await self.client.responses.parse(
            model=settings.openai_model,
            instructions=request.instructions,
            input=request.input,
            text_format=output_type
            )

        return response.output_parsed

    async def continue_with_tool_results(self, response_id: str, tool_results: list[ToolResult], instructions: str, tools: list[ToolDefinition]) -> AIResponse:
            tool_outputs = []

            for tool_result in tool_results:
                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_result.call_id,
                        "output": json.dumps(tool_result.result),
                    }
                )

            openai_tools = []

            for tool in tools:
                openai_tools.append(
                    {
                        "type": "function",
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                        "strict": True,
                    }
                )

            response = await self.client.responses.create(
                model=settings.openai_model,
                previous_response_id=response_id,
                instructions=instructions,
                input=tool_outputs,
                tools=openai_tools,
            )

            return self._build_ai_response(response)

    def _build_ai_response(self, response) -> AIResponse:
        tool_calls = []

        for item in response.output:
            if item.type == "function_call":
                tool_calls.append(
                    ToolCall(
                        name=item.name,
                        arguments=json.loads(item.arguments),
                        call_id=item.call_id
                    )
                )
        return AIResponse(text=response.output_text, response_id=response.id, tool_calls=tool_calls)