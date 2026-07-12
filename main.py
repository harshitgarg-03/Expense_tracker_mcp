from fastapi import FastAPI
from mcp_server import mcp
from session import session

# print( "https are :: " ,type(mcp.http_app()))

# print("mcp methods : ", dir(mcp))
# session.load()
# Import tools to trigger registration decorators on the shared mcp instance
# import tools.expenses
# import tools.auth_tools

from tools.expenses2 import register_transaction_tools
register_transaction_tools(mcp)

from fastapi.middleware.cors import CORSMiddleware

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

# Expose MCP at /mcp by mounting at / to avoid trailing slash redirects
app.mount("/", mcp_app)


