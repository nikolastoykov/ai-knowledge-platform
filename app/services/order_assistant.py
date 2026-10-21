import json

from app.ai.llm_provider import LLMProvider
from app.ai.models import AIRequest, ToolResult
from app.tools.orders import GET_ORDER_TOOL
from app.ai import llm_provider
from app.tools.customers import GET_CUSTOMER_TOOL


class OrderAssistantService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.tools = {
            GET_ORDER_TOOL.definition.name: GET_ORDER_TOOL,
            GET_CUSTOMER_TOOL.definition.name: GET_CUSTOMER_TOOL,
        }

    async def answer(self, question: str) -> str:
        instructions = """
        You are an order support assistant.
        Use the available tools when needed.

        Do not invent order information.
        """

        tool_definitions = [
            tool.definition
            for tool in self.tools.values()
        ]

        response = await self.llm_provider.generate(
            AIRequest(
                instructions=instructions,
                input=question,
                tools=tool_definitions,
            )
        )

        max_iterations = 5
        iteration = 0

        while response.tool_calls and iteration < max_iterations:
            iteration += 1

            tool_results = []

            for tool_call in response.tool_calls:
                tool = self.tools.get(tool_call.name)

                if tool is None:
                    continue

                result = await tool.execute(
                    tool_call.arguments
                )

                tool_results.append(
                    ToolResult(
                        call_id=tool_call.call_id,
                        result=result,
                    )
                )

            if not tool_results:
                break

            response = await self.llm_provider.continue_with_tool_results(
                response_id=response.response_id,
                tool_results=tool_results,
                instructions=instructions,
                tools=tool_definitions,
            )

        if response.tool_calls:
            raise RuntimeError("Maximum tool-call iterations reached.")

        return response.text


order_assistant_service = OrderAssistantService(llm_provider)