from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from .config import settings

COLLECTION = "memories"
_q = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None, timeout=30)


def ensure_collection():
    if not _q.collection_exists(COLLECTION):
        _q.create_collection(COLLECTION, vectors_config=VectorParams(size=settings.embed_dim, distance=Distance.COSINE))


def upsert(mem_id: str, vec: list[float], payload: dict):
    _q.upsert(COLLECTION, [PointStruct(id=mem_id, vector=vec, payload=payload)])


def search(vec: list[float], user_id: str, limit: int = 20):
    flt = Filter(must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))])
    return _q.query_points(COLLECTION, query=vec, query_filter=flt, limit=limit).points


def delete(ids: list[str]):
    if ids:
        _q.delete(COLLECTION, points_selector=ids)


def ping() -> int:
    """Qdrant ko active rakhta hai (free cluster inactivity pe suspend hota hai)."""
    return _q.count(COLLECTION).count
