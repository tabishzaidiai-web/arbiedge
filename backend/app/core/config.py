"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ArbiEdge"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://arbiedge:arbiedge_secret@localhost:5432/arbiedge"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # Clerk
    CLERK_SECRET_KEY: str = ""
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_STARTER_PRICE_ID: str = ""
    STRIPE_PRO_PRICE_ID: str = ""
    STRIPE_ENTERPRISE_PRICE_ID: str = ""

    # Amazon SP-API
    SP_API_CLIENT_ID: str = ""
    SP_API_CLIENT_SECRET: str = ""
    SP_API_REFRESH_TOKEN: str = ""
    SP_API_MARKETPLACE_ID: str = "ATVPDKIKX0DER"

    # Amazon PA-API
    PA_API_ACCESS_KEY: str = ""
    PA_API_SECRET_KEY: str = ""
    PA_API_PARTNER_TAG: str = ""

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://arbiedge.vercel.app"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
