from mcp_server import mcp
from tools.utils import get_api
from schemas.expense import ExpenseCreate
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_access_token
from fastmcp.exceptions import ToolError

from db import get_pool
import json


def _current_user_id() -> str:
    """The JWT's `sub` claim is the SAME user.id Better Auth uses everywhere
    else in the app — this is the whole trick. No lookup table, no mapping."""
    token = get_access_token()
    if token is None:
        raise ToolError("Not authenticated")
    return token.claims["sub"]

def register_expense_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_expenses",
        description="Retrieve a list of all transactions/expenses for the logged-in user."
    )
    async def list_expenses():
        api = get_api()
        result = await api.get_expense()
        return json.dumps(result)

    @mcp.tool(
        name="add_expense",
        description="Add a new transaction (income or expense) for the logged-in user."
    )
    async def add_expense(expense: ExpenseCreate):
        api = get_api()
        result = await api.add_expense(expense)
        return json.dumps( result );

    @mcp.tool(
        name="edit_expense",
        description="Update an existing transaction/expense by ID."
    )
    async def edit_expense(id: str, expense: ExpenseCreate):
        api = get_api()
        res = await api.edit_expense(id, expense)
        return json.dumps(res)

    @mcp.tool(
        name="delete_expense",
        description="Delete a transaction/expense by ID."
    )
    async def delete_expense(id: str):
        api = get_api()
        res = await api.delete_expense(id)
        return json.dumps(res)
