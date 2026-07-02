from fastapi import FastAPI
from mcp_server import mcp

# Import tools to trigger registration decorators on the shared mcp instance
import tools.expenses
import tools.auth_tools

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server running"}

# Expose MCP at /mcp
app.mount("/mcp", mcp.http_app())
