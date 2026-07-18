import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

MCP_RESOURCE_URI = os.environ["MCP_RESOURCE_URI"]  

API_BASE_URL = os.getenv("API_BASE_URL")

INTROSPECTION_CLIENT_ID = os.environ[
    "INTROSPECTION_CLIENT_ID"
]

INTROSPECTION_CLIENT_SECRET = os.environ[
    "INTROSPECTION_CLIENT_SECRET"
]