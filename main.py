from fastapi.middleware.cors import CORSMiddleware
from mcp_server import mcp
from tools.expenses2 import register_transaction_tools
from fastapi import FastAPI

# Register transaction tools
register_transaction_tools(mcp)

mcp_app = mcp.http_app()
app = FastAPI(lifespan=mcp_app.lifespan)

# Add CORS middleware to allow MCP Inspector and other web applications to connect
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Server running"}

# Expose MCP at /mcp by mounting
app.mount("/", mcp_app)

