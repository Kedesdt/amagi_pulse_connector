import os
from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)


def _env(name: str, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value


BASE_URL = _env("BASE_URL", "https://bandnews.cloudport.amagi.tv")
TOKEN = _env("TOKEN", "")
FEED_CODE = _env("FEED_CODE", "")
HEADEND = int(_env("HEADEND", "1"))
TAKE_NEXT_ACTION_NAME = _env("ACTION_NAME", "take_next")
DELAY = float(_env("DELAY", "0"))  # Delay em segundos
