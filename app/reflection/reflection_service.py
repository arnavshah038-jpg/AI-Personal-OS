from openai import OpenAI

from app.core.config import settings
from app.database.models.memory import Memory
from app.database.session import SessionLocal
from app.repositories.reflection_repository import ReflectionRepository


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)


class ReflectionService:

    @staticmethod
    def generate_reflection(
        session_id: str = "arnav",
    ):

        db = SessionLocal()

        try:

            memories = (
                db.query(Memory)
                .filter(
                    Memory.session_id == session_id,
                )
                .order_by(
                    Memory.importance.desc(),
                )
                .limit(20)
                .all()
            )

            if not memories:

                return "No memories found."

            memory_text = "\n".join(
                f"- {memory.memory}"
                for memory in memories
            )

            prompt = f"""
You are the reasoning engine of an AI Personal OS.

Analyze the user's memories.

Your tasks:

1. Find patterns.
2. Detect contradictions.
3. Identify long-term goals.
4. Identify preferences.
5. Suggest one improvement.

Return exactly 5 concise bullet points.

Memories:

{memory_text}
"""

            response = client.responses.create(
                model="gpt-5-mini",
                input=prompt,
            )

            reflection = response.output_text

            ReflectionRepository.save_reflection(
                db=db,
                session_id=session_id,
                reflection=reflection,
                importance=8,
            )

            return reflection

        finally:

            db.close()