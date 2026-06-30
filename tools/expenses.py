from fastmcp import FastMCP

from api_client import ExpenseApi

mcp = FastMCP()

@mcp.tool()
async def list_expenses(token: str):
    api = ExpenseApi(token)
    return await api.get_expense()

@mcp.tool()
async def add_expenses(token: str):
    api = ExpenseApi(token)
    return await api.add_expense()

@mcp.tool()
async def edit_expenses(token: str):
    api = ExpenseApi(token)
    return await api.edit_expense()

@mcp.tool()
async def delete_expenses(token: str):
    api = ExpenseApi(token)
    return await api.delete_expense()
