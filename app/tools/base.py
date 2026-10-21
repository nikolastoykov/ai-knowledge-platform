from collections.abc import Callable
from dataclasses import dataclass
from inspect import isawaitable

from app.ai.models import ToolDefinition


@dataclass
class Tool:
    definition: ToolDefinition
    handler: Callable

    async def execute(self, arguments: dict):
        result = self.handler(**arguments)

        if isawaitable(result):
            result = await result

        return result