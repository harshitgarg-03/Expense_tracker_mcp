from fastmcp import FastMCP

from utils import get_api

from schemas.expense import Expense_Create

mcp = FastMCP()

@mcp.tool()
async def list_expenses():
    api = get_api()
    return await api.get_expense()

@mcp.tool()
async def add_expenses(expense: Expense_Create):
    api = get_api()
    return await api.add_expense(expense)

@mcp.tool()
async def edit_expenses(id: str, expense: Expense_Create):
    api = get_api()
    return await api.edit_expense(id, expense)

@mcp.tool()
async def delete_expenses(id: str):
    api = get_api()
    return await api.delete_expense(id)
