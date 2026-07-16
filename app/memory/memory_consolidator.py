import json

from app.core.config import settings
from app.core.openai_client import client
from app.schemas.memory_consolidation import MemoryDecision


class MemoryConsolidator:

    @staticmethod
    def consolidate(
        existing_memories: str,
        new_memory: str,
    ) -> MemoryDecision:

        prompt = f"""
You are an AI memory management system.

Existing memories:

{existing_memories}

New memory:

{new_memory}

Decide whether the new memory should be:

1. KEEP
- if it is a completely new fact.

2. IGNORE
- if the same fact already exists.

3. UPDATE
- if the new memory replaces an old fact.

Return ONLY valid JSON.

Examples:

KEEP

{{
    "action": "KEEP"
}}

IGNORE

{{
    "action": "IGNORE"
}}

UPDATE

{{
    "action": "UPDATE",
    "memory_id": 3,
    "new_memory": "My favorite language is Rust."
}}

Rules:

- Return ONLY JSON.
- No markdown.
- No explanation.
- memory_id must refer to the memory being updated.
- new_memory is required only for UPDATE.
"""

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        content = response.output_text.strip()

        data = json.loads(content)

        return MemoryDecision(**data)