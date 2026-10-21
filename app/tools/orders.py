from app.ai.models import ToolDefinition
from app.tools.base import Tool


ORDERS = {
    "123": {
        "id": "123",
        "customer_id": "1",
        "status": "shipped",
        "carrier": "Speedy",
    },
    "456": {
        "id": "456",
        "customer_id": "2",
        "status": "processing",
        "carrier": None,
    },
}

def get_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)

    if order is None:
        return {
            "found": False,
            "order_id": order_id,
        }

    return {
        "found": True,
        **order,
    }


GET_ORDER_DEFINITION = ToolDefinition(
    name="get_order",
    description="Get the current information for an order by its ID.",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID.",
            },
        },
        "required": ["order_id"],
        "additionalProperties": False,
    },
)

GET_ORDER_TOOL = Tool(
    definition=GET_ORDER_DEFINITION,
    handler=get_order
)