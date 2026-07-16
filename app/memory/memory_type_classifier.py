from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)


class MemoryTypeClassifier:

    @staticmethod
    def classify(memory: str) -> str:

        text = memory.strip().lower()

        # -------------------------------
        # Identity
        # -------------------------------

        if text.startswith("my name is"):
            return "identity"

        if text.startswith("i am "):
            return "identity"

        if text.startswith("i'm "):
            return "identity"

        if text.startswith("my age is"):
            return "identity"

        if text.startswith("i was born"):
            return "identity"

        if text.startswith("my birthday is"):
            return "identity"

        if text.startswith("i live in"):
            return "identity"

        if text.startswith("i am from"):
            return "identity"

        if text.startswith("my nationality is"):
            return "identity"

        if text.startswith("i work as"):
            return "identity"

        # -------------------------------
        # Preference
        # -------------------------------

        preference_patterns = [
            "favorite",
            "favourite",
            "i love",
            "i like",
            "i enjoy",
            "i prefer",
        ]

        if any(p in text for p in preference_patterns):
            return "preference"

        # -------------------------------
        # Goal
        # -------------------------------

        goal_patterns = [
            "i want to",
            "my goal is",
            "i plan to",
            "i hope to",
            "i will become",
            "my dream is",
        ]

        if any(p in text for p in goal_patterns):
            return "goal"

        # -------------------------------
        # Project
        # -------------------------------

        project_patterns = [
            "i am building",
            "i'm building",
            "i am developing",
            "i'm developing",
            "my project",
            "working on",
            "currently building",
        ]

        if any(p in text for p in project_patterns):
            return "project"

        # -------------------------------
        # Skill
        # -------------------------------

        skill_patterns = [
            "i know",
            "i can",
            "i'm good at",
            "i am good at",
            "i have experience with",
        ]

        if any(p in text for p in skill_patterns):
            return "skill"

        # -------------------------------
        # GPT Fallback
        # -------------------------------

        prompt = f"""
Classify the memory into exactly one category.

Categories:
identity
preference
goal
skill
project
fact

Memory:
{memory}

Return ONLY one word.
"""

        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
        )

        memory_type = response.output_text.strip().lower()

        allowed = {
            "identity",
            "preference",
            "goal",
            "skill",
            "project",
            "fact",
        }

        if memory_type not in allowed:
            return "fact"

        return memory_type