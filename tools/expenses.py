from fastmcp import FastMCP

from utils import get_api

mcp = FastMCP()

api = get_api()

@mcp.tool()
async def list_expenses():
    return await api.get_expense()

@mcp.tool()
async def add_expenses():
    return await api.add_expense()

@mcp.tool()
async def edit_expenses():
    return await api.edit_expense()

@mcp.tool()
async def delete_expenses():
    return await api.delete_expense()
