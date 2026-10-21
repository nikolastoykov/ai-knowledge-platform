from app.ai.models import ToolDefinition
from app.tools.base import Tool


CUSTOMERS = {
    "1": {
        "id": "1",
        "name": "Ivan Petrov",
        "email": "ivan@example.com",
    },
    "2": {
        "id": "2",
        "name": "Maria Georgieva",
        "email": "maria@example.com",
    },
}

def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "found": False,
            "customer_id": customer_id
        }

    return {
        "found": True,
        **customer
    }

GET_CUSTOMER_DEFINITION = ToolDefinition(
    name="get_customer",
    description="Get customer information by customer ID.",
    parameters={
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer ID.",
            },
        },
        "required": ["customer_id"],
        "additionalProperties": False,
    },
)

GET_CUSTOMER_TOOL = Tool(
    definition=GET_CUSTOMER_DEFINITION,
    handler=get_customer,
)