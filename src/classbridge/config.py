import os
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


SUPABASE_URL = _require("SUPABASE_URL")
SUPABASE_ANON_KEY = _require("SUPABASE_ANON_KEY")

# Only needed by backend code (notifications). Never import this in page files.
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")