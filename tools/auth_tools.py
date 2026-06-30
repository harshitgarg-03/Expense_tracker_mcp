import httpx

from config import API_BASE_URL

from fastmcp import FastMCP

from session import session

mcp = FastMCP()

@mcp.tool()
async def login(email:str, password: str):
    async with httpx.AsyncClient() as client:

        res = await client.post(
            f"{API_BASE_URL}/auth/sign-in/email",
            json={
                "email": email,
                "password": password
            }
        )

        if res.status_code != 200:
            return {
                "error": "Invalid credentials"
            }
        res.raise_for_status

        data = res.json()

        session.token = data["token"]
        session.user = data["user"]
        
        return {
            "message": "Successfully logged in",
            "user": data["user"]
        }
    

@mcp.tool()
async def sign_up(
    name: str,
    email: str,
    password: str
):

    async with httpx.AsyncClient() as client:

        res = await client.post(
            f"{API_BASE_URL}/auth/sign-up/email",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        res.raise_for_status

        data = res.json()
        session.token = data["token"]
        session.user = data["user"]

        return {
            "message": "use signup success..",
            "user": data["user"]
        }


@mcp.tool()
async def whoami():
    if not session.token :
        return {
            "message" : "not authenticated "
        }
    
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{API_BASE_URL}/auth/get-session",
            headers={
                "Authorization":
                f"Bearer {session.token}"
            }
        )

        res.raise_for_status
        return res.json()

@mcp.tool()
async def logout(): 
    if not session.token:
        raise Exception(
            "no user logged in"
        )
    
    async with httpx.AsyncClient() as client:

        res = await client.post(
            f"{API_BASE_URL}/auth/sign-out",
            headers={
                "Authorization": f"Bearer {session.token}"
            }
        )

        session.token = null
        session.user = null

        return "Logged out successfully.."


# @mcp.tool()
# async def sign_out(){
#     async with httpx.AsyncClient() as client:
    
#     res = await client.post()
# }