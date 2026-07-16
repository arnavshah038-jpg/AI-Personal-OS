from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)


class ReflectionGenerator:

    @staticmethod
    def generate(
        memories: str,
    ) -> str:

        if not memories.strip():
            return ""

        prompt = f"""
You are an AI that creates long-term reflections.

Below are memories collected about a user.

Your task:

- Find higher-level patterns.
- Infer habits.
- Infer long-term interests.
- Infer learning trends.
- Infer consistent behavior.

Do NOT repeat memories.

Create ONE concise reflection.

Examples:

Memories:
User knows LangChain.
User uses Docker.
User completed AI Personal OS.

Reflection:
User consistently builds production-grade AI systems and enjoys learning modern AI infrastructure.

------------------------

Memories:

{memories}

Return ONLY the reflection.
"""

        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
        )

        return response.output_text.strip()