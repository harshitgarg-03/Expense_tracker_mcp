from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from pydantic import AnyHttpUrl
from config import API_BASE_URL, MCP_RESOURCE_URI
from fastmcp.server.auth.providers.jwt import JWTVerifier


# Define the expected issuer claim from the remote Better Auth server
# In this workspace, API_BASE_URL is 'https://expense-tracker-orpin-nu-68.vercel.app/api'.
# The actual issuer claim in the Better Auth JWT is 'https://expense-tracker-orpin-nu-68.vercel.app'.
issuer_url = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"

# Better Auth JWKS URI for token validation
jwks_uri = f"{issuer_url}/api/auth/jwks"

token_verifier = JWTVerifier(
    jwks_uri=jwks_uri,
    issuer=issuer_url,
    audience=MCP_RESOURCE_URI, # Set to None to support dynamic client registration client IDs
)

# # We want the client to query our FastAPI server (acting as the proxy/gateway) for authorization metadata.
# auth_server_base = MCP_RESOURCE_URI/api/auth

auth = RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(API_BASE_URL)],
    base_url=MCP_RESOURCE_URI,
)

mcp = FastMCP(
    name="expense-tracker-mcp",
    auth=auth,
    instructions="""
You are an AI interface for the Expense Tracker application.

Rules:
- Always authenticate users before accessing protected resources.
- Respect the same permissions, validations, and business rules as the web application.
- Users can only view or modify their own transactions.
- Never bypass authentication or authorization checks.
"""
)

