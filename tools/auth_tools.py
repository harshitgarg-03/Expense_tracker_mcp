from fastmcp import FastMCP

from api_client import ExpenseApi

mcp = FastMCP()

@mcp.tool()
async def sign_up(
    name: str,
    email: str,
    password: str
):
    
    api = ExpenseApi()
    return await api.sign_up_user(name, email, password)

@mcp.tool()
async def login(email:str, password: str):
    api = ExpenseApi()
    return api.signin_user(email, password)

@mcp.tool()
async def whoami():
    api = ExpenseApi()
    return api.whoami()

@mcp.tool()
async def logout(): 
    api = ExpenseApi()
    return api.logout()
