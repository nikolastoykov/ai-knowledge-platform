from typing import Protocol, TypeVar

from pydantic import BaseModel

from app.ai.models import AIRequest, AIResponse, ToolResult, ToolDefinition


T = TypeVar("T", bound=BaseModel)


class LLMProvider(Protocol):

    async def generate(self, request: AIRequest) -> AIResponse:
        ...

    async def generate_structured(self, request: AIRequest, output_type: type[T]) -> T:
        ...

    async def continue_with_tool_results(self, response_id: str, tool_results: list[ToolResult], instructions: str, tools: list[ToolDefinition]) -> AIResponse:
        ...