import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
DEFAULT_COVER = os.getenv("DEFAULT_COVER", "")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN", "") 