from pydantic import BaseModel
import json

from src.toodlo_ai.AI.client import client


class TestResponse(BaseModel):
    title: str
    priority: str


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Create a TODO for studying Python. Return its title and priority."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "test_response",
            "schema": TestResponse.model_json_schema()
        }
    }
)

result = TestResponse.model_validate(
    json.loads(response.choices[0].message.content)
)

print(result)