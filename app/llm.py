import json
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from .config import settings

log = logging.getLogger("aipos.llm")
_client = None


def client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), reraise=True)
def respond(instructions: str, messages: list[dict], json_mode: bool = False) -> str:
    kw = {"text": {"format": {"type": "json_object"}}} if json_mode else {}
    r = client().responses.create(
        model=settings.chat_model, instructions=instructions, input=messages, **kw
    )
    return r.output_text


def json_call(instructions: str, text: str) -> dict:
    """Structured output; fail hone par empty dict (chat kabhi nahi tootna chahiye)."""
    try:
        out = respond(instructions + "\nReply with a JSON object only.",
                      [{"role": "user", "content": text}], json_mode=True)
        return json.loads(out)
    except Exception as e:
        log.warning("json_call failed: %s", e)
        return {}
