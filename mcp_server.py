from fastmcp import FastMCP
from fastmcp.server.auth import RemoteAuthProvider
from pydantic import AnyHttpUrl
from config import API_BASE_URL, MCP_RESOURCE_URI
from fastmcp.server.auth.providers.jwt import JWTVerifier

issuer_url = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"

jwks_uri = f"{issuer_url}/api/auth/mcp/jwks"

token_verifier = JWTVerifier(
    jwks_uri=jwks_uri,
    issuer=issuer_url,
    audience=MCP_RESOURCE_URI,
)

print("OAuth issuer:", issuer_url)
print("JWKS URI:", jwks_uri)
print("Expected audience:", MCP_RESOURCE_URI)



print("JWKS UIS ::: " , jwks_uri)
auth = RemoteAuthProvider(
    token_verifier=token_verifier,
    authorization_servers=[AnyHttpUrl(issuer_url)],
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

