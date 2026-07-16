from app.core.config import settings
from app.core.openai_client import client


class MemoryImportance:

    @staticmethod
    def score(memory: str) -> int:

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a memory ranking engine.\n\n"
                        "Rate how important this memory is for a long-term AI assistant.\n\n"
                        "Rules:\n"
                        "10 = Core identity (name, birthday, family, profession)\n"
                        "8-9 = Strong long-term preferences and goals\n"
                        "5-7 = Frequently useful facts\n"
                        "1-4 = Weak preferences or low-value information\n\n"
                        "Return ONLY a single integer from 1 to 10."
                    ),
                },
                {
                    "role": "user",
                    "content": memory,
                },
            ],
        )

        try:
            score = int(response.output_text.strip())
            return max(1, min(score, 10))
        except ValueError:
            return 5