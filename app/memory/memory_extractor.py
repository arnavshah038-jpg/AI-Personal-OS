from app.core.openai_client import client
from app.core.config import settings


class MemoryExtractor:

    @staticmethod
    def extract(message: str):

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a memory extraction engine.\n\n"
                        "Extract only long-term useful user memories.\n\n"
                        "Examples:\n"
                        "- My name is Arnav.\n"
                        "- I live in Delhi.\n"
                        "- My favorite language is Python.\n"
                        "- I use Redis.\n\n"
                        "Ignore greetings, jokes, temporary requests, "
                        "and casual conversation.\n\n"
                        'If nothing should be remembered, reply only with: NONE'
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        return response.output_text.strip()