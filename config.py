import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

API_BASE_URL = os.getenv("API_BASE_URL")