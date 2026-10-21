from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.models import AIRequest, ToolResult
from app.tools.base import Tool


class AgentService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def run(self, task: str, tools: list[Tool]) -> str:
        if not task.strip():
            raise ValueError("Task cannot be empty.")

        tool_definitions = [tool.definition for tool in tools]

        response = await self.llm_provider.generate(
            AIRequest(
                instructions="You are an agent. Use the available tools when needed to solve the user's task. Continue until the task is complete, then return the final answer.",
                input=task,
                tools=tool_definitions,
            )
        )

        for _ in range(5):
            if not response.tool_calls:
                return response.text

            tool_results = []

            for tool_call in response.tool_calls:
                tool = next(
                    (
                        tool
                        for tool in tools
                        if tool.definition.name == tool_call.name
                    ),
                    None,
                )

                if tool is None:
                    raise RuntimeError(f"Unknown tool: {tool_call.name}")

                result = await tool.execute(tool_call.arguments)

                tool_results.append(
                    ToolResult(
                        call_id=tool_call.call_id,
                        result=result,
                    )
                )

            response = await self.llm_provider.continue_with_tool_results(
                response_id=response.response_id,
                tool_results=tool_results,
                instructions="Continue solving the user's task. Use additional tools if needed. Return the final answer only when the task is complete.",
                tools=tool_definitions,
            )

        raise RuntimeError("Agent exceeded maximum tool iterations.")


agent_service = AgentService(llm_provider=llm_provider)