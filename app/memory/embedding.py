from app.core.config import settings
from app.core.openai_client import client


class EmbeddingGenerator:

    @staticmethod
    def generate(text: str) -> list[float]:

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding