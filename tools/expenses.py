from mcp_server import mcp
from tools.utils import get_api
from schemas.expense import ExpenseCreate

@mcp.tool(
    name="list_expenses",
    description="Retrieve a list of all transactions/expenses for the logged-in user."
)
async def list_expenses():
    api = get_api()
    return await api.get_expense()

@mcp.tool(
    name="add_expense",
    description="Add a new transaction (income or expense) for the logged-in user."
)
async def add_expense(expense: ExpenseCreate):
    api = get_api()
    result = await api.add_expense(expense)
    return (
        f"Expense added successfully.\n"
        f"ID: {result['id']}\n"
        f"Title: {result['title']}\n"
        f"Amount: ₹{result['amount']}\n"
        f"Category: {result['category']}\n"
        f"Type: {result['type']}"
    )

@mcp.tool(
    name="edit_expense",
    description="Update an existing transaction/expense by ID."
)
async def edit_expense(id: str, expense: ExpenseCreate):
    api = get_api()
    return await api.edit_expense(id, expense)

@mcp.tool(
    name="delete_expense",
    description="Delete a transaction/expense by ID."
)
async def delete_expense(id: str):
    api = get_api()
    return await api.delete_expense(id)
