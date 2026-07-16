import json

from app.core.config import settings
from app.core.openai_client import client


class ForgetExtractor:

    @staticmethod
    def extract(message: str) -> str | None:

        prompt = f"""
You are an AI memory deletion system.

The user may ask to forget one of their memories.

User message:

{message}

Return JSON only.

Examples:

{{"memory": "My favorite language is Rust."}}

{{"memory": "I love FastAPI."}}

If the user is NOT asking to forget anything:

{{"memory": null}}
"""

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        data = json.loads(response.output_text)

        return data["memory"]