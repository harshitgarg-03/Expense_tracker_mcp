from fastmcp import FastMCP

from utils import get_api

mcp = FastMCP()

@mcp.tool()
async def list_expenses():
    api = get_api()
    return await api.get_expense()

@mcp.tool()
async def add_expenses():
    api = get_api()
    return await api.add_expense()

@mcp.tool()
async def edit_expenses():
    api = get_api()
    return await api.edit_expense()

@mcp.tool()
async def delete_expenses():
    api = get_api()
    return await api.delete_expense()
