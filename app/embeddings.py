import hashlib
import json
from . import cache
from .config import settings
from .llm import client


def embed(text: str) -> list[float]:
    key = "emb:" + hashlib.sha256(text.encode()).hexdigest()
    if (hit := cache.get(key)):
        return json.loads(hit)
    vec = client().embeddings.create(model=settings.embed_model, input=text).data[0].embedding
    cache.set(key, json.dumps(vec))
    return vec
