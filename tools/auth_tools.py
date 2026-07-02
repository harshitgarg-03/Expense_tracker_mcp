from mcp_server import mcp
from api_client import ExpenseApi

@mcp.tool(
    name="sign_up",
    description="Create a new user account with a name, email, and password, and automatically log in."
)
async def sign_up(
    name: str,
    email: str,
    password: str
):
    api = ExpenseApi()
    return await api.sign_up_user(name, email, password)

@mcp.tool(
    name="login",
    description="Log in an existing user using their email and password."
)
async def login(email: str, password: str):
    api = ExpenseApi()
    return await api.signin_user(email, password)

@mcp.tool(
    name="whoami",
    description="Get details of the currently logged-in user session."
)
async def whoami():
    api = ExpenseApi()
    return await api.whoami()

@mcp.tool(
    name="logout",
    description="Log out the currently authenticated user and clear the session."
)
async def logout(): 
    api = ExpenseApi()
    return await api.logout()
