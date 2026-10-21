from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str
    openai_embedding_model: str
    embedding_dimensions: int
    database_url: str
    rag_min_similarity: float = 0.3
    rag_min_relevance: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()