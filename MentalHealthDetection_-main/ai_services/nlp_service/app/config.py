import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sentiment_model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    toxicity_model_name: str = "unitary/toxic-bert"
    max_length: int = 512

    class Config:
        env_file = ".env"

settings = Settings()
