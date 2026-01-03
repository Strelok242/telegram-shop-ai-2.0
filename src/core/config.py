from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    db_url: str


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Create .env in project root and set BOT_TOKEN=...")

    db_url = os.getenv("DB_URL", "sqlite+aiosqlite:///./data/app.db")
    return Settings(bot_token=token, db_url=db_url)
