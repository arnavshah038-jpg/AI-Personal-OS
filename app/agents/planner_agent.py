from app.core.config import settings
from app.core.openai_client import client
from app.utils.logger import logger


class PlannerAgent:

    @staticmethod
    def plan(
        user_request: str,
    ) -> str:

        prompt = f"""
You are an AI Planner.

Your job is to convert a user's request into
clear executable steps.

Rules:

- Break the task into logical steps.
- Keep steps concise.
- Return only the plan.
- No explanations.

User Request:

{user_request}
"""

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=prompt,
        )

        plan = response.output_text.strip()

        logger.info(
            "Execution Plan:\n%s",
            plan,
        )

        return plan