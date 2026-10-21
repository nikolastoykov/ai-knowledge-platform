import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

# Import the route with placeholder credentials; the SDK call is mocked below.
with patch.dict(
    os.environ,
    {
        "OPENAI_API_KEY": "test-api-key",
        "OPENAI_MODEL": "test-model",
        "OPENAI_EMBEDDING_MODEL": "test-embedding-model",
        "EMBEDDING_DIMENSIONS": "1536",
        "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
    },
):
    from app.api import generation


class GenerateEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def test_generate_forwards_prompt_and_returns_generated_text(self):
        prompt = "Explain hybrid search in one sentence."
        generated_text = "Hybrid search combines semantic and keyword retrieval."
        sdk_response = SimpleNamespace(
            id="response-test",
            output_text=generated_text,
            output=[],
        )

        with patch.object(
            generation.llm_provider.client.responses,
            "create",
            new_callable=AsyncMock,
            return_value=sdk_response,
        ) as create_response:
            response = await generation.generate(
                generation.GenerateRequest(prompt=prompt)
            )

        self.assertEqual(response.model_dump(), {"text": generated_text})
        create_response.assert_awaited_once()
        self.assertEqual(create_response.await_args.kwargs["input"], prompt)


if __name__ == "__main__":
    unittest.main()
