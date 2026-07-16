from pydantic import BaseModel
from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
)


class EpisodeExtractionResult(BaseModel):
    action: str
    title: str
    description: str
    event_type: str


class EpisodeExtractor:

    @staticmethod
    def extract(
        message: str,
    ) -> EpisodeExtractionResult:

        prompt = f"""
You are an episodic memory extraction system.

Determine whether the user's message describes a meaningful event
that should be remembered as an episode.

Remember ONLY events such as:

- achievements
- milestones
- travel
- meetings
- competitions
- interviews
- exams
- conferences
- project completion
- important incidents
- memorable experiences

Ignore:

- preferences
- identity
- facts
- skills
- casual chat

Return JSON.

Example:

{{
  "action":"SAVE",
  "title":"Completed AI Personal OS",
  "description":"User completed the AI Personal OS project.",
  "event_type":"achievement"
}}

OR

{{
  "action":"NONE",
  "title":"",
  "description":"",
  "event_type":""
}}

User message:

{message}
"""

        response = client.responses.parse(
            model="gpt-5-nano",
            input=prompt,
            text_format=EpisodeExtractionResult,
        )

        return response.output_parsed