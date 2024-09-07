from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/"
    database_name: str = "service_registry"
    telegram_bot_token: str
    telegram_chat_id: str
    service_inactive_threshold_minutes: int = 5
    check_interval_seconds: int = 60
    daily_summary_interval_seconds: int = 86400
    api_host: str = "0.0.0.0"
    api_port: int = 8002
    timezone: str = "UTC"
    daily_summary_time: str = "00:00"  # 24-hour format
    debug_mode: bool = False
    debug_summary_interval_seconds: int = 300  # 5 minutes in debug mode

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
