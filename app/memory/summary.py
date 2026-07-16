from app.core.openai_client import client
from app.core.config import settings


class ConversationSummary:

    @staticmethod
    def summarize(messages):

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Summarize the conversation in a concise way. "
                        "Preserve important user facts, preferences, goals, "
                        "and ongoing tasks."
                    ),
                },
                *messages,
            ],
        )

        return response.output_text