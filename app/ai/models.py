from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict

@dataclass
class AIRequest:
    input: str
    instructions: str | None = None
    tools: list[ToolDefinition] = field(default_factory=list)

@dataclass
class ToolCall:
    name: str
    arguments: dict
    call_id: str

@dataclass
class ToolResult:
    call_id: str
    result: Any

@dataclass
class AIResponse:
    text: str
    response_id: str
    tool_calls: list[ToolCall] = field(default_factory=list)