import httpx

from config import API_BASE_URL

from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
async def login(email:str, password: str):
    async with httpx.AsyncClient() as client:

        res = await client.post(
            f"{API_BASE_URL}/api/auth/sign-in/email",
            json={
                "email": email,
                "password": password
            }
        )

        if res.status_code != 200:
            return {
                "error": "Invalid credentials"
            }
        
        data = res.json()

        token = data.get("token")

        if not token:
            return {
                "error": "No token returned by server"
            }
        
        return {
            "message": "Successfully logged in"
        }
    

@mcp.tool()
async def sign_up(
    name: str,
    email: str,
    password: str
):

    async with httpx.AsyncClient() as client:

        res = await client.post(
            f"{API_BASE_URL}/api/auth/sign-up/email",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        return res.json()


# @mcp.tool()
# async def sign_out(){
#     async with httpx.AsyncClient() as client:
    
#     res = await client.post()
# }