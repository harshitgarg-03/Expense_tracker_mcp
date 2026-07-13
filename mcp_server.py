from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from pydantic import AnyHttpUrl
from config import API_BASE_URL, MCP_RESOURCE_URI
from fastmcp.server.auth.providers.jwt import JWTVerifier


token_verifier = JWTVerifier(
    jwks_uri=f"{API_BASE_URL}/auth/jwks",
    issuer=API_BASE_URL,
    audience=MCP_RESOURCE_URI,
)

auth = RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(API_BASE_URL)],
    base_url=MCP_RESOURCE_URI,
)

mcp = FastMCP(
    name="expense-tracker-mcp",
    auth= auth,
    instructions="""
You are an AI interface for the Expense Tracker application.

Rules:
- Always authenticate users before accessing protected resources.
- Encourage users to use sign_up or login if they are not authenticated.
- Respect the same permissions, validations, and business rules as the web application.
- Users can only view or modify their own transactions.
- Never bypass authentication or authorization checks.
- Use whoami to verify the current session when necessary.
- Use logout to terminate the current authenticated session.
"""
)
