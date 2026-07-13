import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp_server import mcp
from config import API_BASE_URL
from tools.expenses2 import register_transaction_tools

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

# HTTP Client for proxying requests to Better Auth
http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

@app.get("/")
def home():
    return {"message": "Server running"}

# Expose MCP at /mcp by mounting
app.mount("/mcp", mcp_app)

# 1. Protected Resource Discovery Endpoint (RFC 9728)
# Replaced /.well-known/oauth-protected-resource/mcp at root level
@app.get("/.well-known/oauth-protected-resource/mcp")
async def get_protected_resource_metadata(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "resource": f"{base_url}/mcp",
        "authorization_servers": [
            f"{base_url}/api/auth"
        ],
        "scopes_supported": ["openid", "profile", "email", "offline_access"]
    }

# Helper to fetch remote metadata and rewrite endpoints
async def fetch_and_rewrite_auth_metadata(request: Request):
    base_url = str(request.base_url).rstrip("/")
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    remote_metadata_url = f"{vercel_issuer}/api/auth/.well-known/oauth-authorization-server"
    
    try:
        res = await http_client.get(remote_metadata_url, timeout=10.0)
        res.raise_for_status()
        metadata = res.json()
    except Exception as e:
        return {"error": f"Failed to fetch remote metadata: {str(e)}"}
        
    # Rewrite fields to use our local proxy paths
    metadata["issuer"] = f"{base_url}/api/auth"
    metadata["authorization_endpoint"] = f"{base_url}/api/auth/oauth2/authorize"
    metadata["token_endpoint"] = f"{base_url}/api/auth/oauth2/token"
    metadata["userinfo_endpoint"] = f"{base_url}/api/auth/oauth2/userinfo"
    metadata["jwks_uri"] = f"{base_url}/api/auth/oauth2/jwks"
    metadata["registration_endpoint"] = f"{base_url}/api/auth/oauth2/register"
    
    return metadata

# 2. Authorization Server Discovery Endpoint (RFC 8414 Path-aware)
@app.get("/.well-known/oauth-authorization-server/api/auth")
@app.get("/.well-known/openid-configuration/api/auth")
async def get_auth_metadata(request: Request):
    return await fetch_and_rewrite_auth_metadata(request)

# 3. Proxy Routes to Remote Better Auth
@app.api_route("/api/auth/oauth2/authorize", methods=["GET", "POST"])
async def proxy_authorize(request: Request):
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    target_url = f"{vercel_issuer}/api/auth/mcp/authorize"
    query_string = request.url.query
    redirect_url = f"{target_url}?{query_string}" if query_string else target_url
    return RedirectResponse(url=redirect_url, status_code=307)

@app.post("/api/auth/oauth2/token")
async def proxy_token(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    target_url = f"{vercel_issuer}/api/auth/mcp/token"
    
    res = await http_client.post(
        target_url,
        content=body,
        headers=headers,
        params=dict(request.query_params),
        timeout=30.0
    )
    
    response_headers = {
        k: v for k, v in res.headers.items()
        if k.lower() not in ("content-encoding", "content-length", "transfer-encoding", "connection", "keep-alive")
    }
    return Response(
        content=res.content,
        status_code=res.status_code,
        headers=response_headers
    )

@app.post("/api/auth/oauth2/register")
async def proxy_register(request: Request):
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    target_url = f"{vercel_issuer}/api/auth/mcp/register"
    
    res = await http_client.post(
        target_url,
        content=body,
        headers=headers,
        params=dict(request.query_params),
        timeout=30.0
    )
    
    response_headers = {
        k: v for k, v in res.headers.items()
        if k.lower() not in ("content-encoding", "content-length", "transfer-encoding", "connection", "keep-alive")
    }
    return Response(
        content=res.content,
        status_code=res.status_code,
        headers=response_headers
    )

@app.get("/api/auth/oauth2/jwks")
async def proxy_jwks(request: Request):
    headers = dict(request.headers)
    headers.pop("host", None)
    
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    target_url = f"{vercel_issuer}/api/auth/jwks"
    
    res = await http_client.get(
        target_url,
        headers=headers,
        params=dict(request.query_params),
        timeout=30.0
    )
    
    response_headers = {
        k: v for k, v in res.headers.items()
        if k.lower() not in ("content-encoding", "content-length", "transfer-encoding", "connection", "keep-alive")
    }
    return Response(
        content=res.content,
        status_code=res.status_code,
        headers=response_headers
    )

@app.get("/api/auth/oauth2/userinfo")
async def proxy_userinfo(request: Request):
    headers = dict(request.headers)
    headers.pop("host", None)
    
    vercel_issuer = API_BASE_URL.replace("/api", "") if API_BASE_URL else "https://expense-tracker-orpin-nu-68.vercel.app"
    target_url = f"{vercel_issuer}/api/auth/mcp/userinfo"
    
    res = await http_client.get(
        target_url,
        headers=headers,
        params=dict(request.query_params),
        timeout=30.0
    )
    
    response_headers = {
        k: v for k, v in res.headers.items()
        if k.lower() not in ("content-encoding", "content-length", "transfer-encoding", "connection", "keep-alive")
    }
    return Response(
        content=res.content,
        status_code=res.status_code,
        headers=response_headers
    )
