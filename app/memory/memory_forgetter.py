from app.core.config import settings
from app.core.openai_client import client
from app.schemas.memory_forget import MemoryForgetDecision


class MemoryForgetter:

    @staticmethod
    def should_forget(
        message: str,
    ) -> MemoryForgetDecision:

        prompt = f"""
You are an AI memory management system.

User message:

{message}

Determine whether the user wants to delete or forget a memory.

If the user wants to forget/delete/remove some memory, respond EXACTLY like this:

YES: <memory>

Examples:

YES: My favorite language is Rust.

If the user is NOT asking to forget anything, respond:

NO

Rules:
- Respond ONLY with YES: ... or NO.
- Do not explain.
"""

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        return MemoryForgetDecision.parse(
            response.output_text.strip()
        )