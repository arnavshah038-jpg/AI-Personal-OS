from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    chat_model: str = "gpt-4o-mini"
    embed_model: str = "text-embedding-3-small"
    embed_dim: int = 1536
    database_url: str = "postgresql+psycopg://aipos:aipos@localhost:5433/aipos"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    app_api_key: str = ""
    summarize_every: int = 12      # itne messages ke baad conversation summary
    reflect_every: int = 8         # itne episodic memories ke baad reflection
    context_token_budget: int = 700
    rate_limit_per_min: int = 30


settings = Settings()
