from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.utils.logger import logger


qdrant = QdrantClient(
    host="localhost",
    port=6333,
)

COLLECTION_NAME = "memories"

collections = qdrant.get_collections().collections

if not any(c.name == COLLECTION_NAME for c in collections):

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )

    logger.info("✅ Qdrant memories collection created.")

else:

    logger.info("✅ Qdrant memories collection already exists.")