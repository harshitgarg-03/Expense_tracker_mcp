from fastapi import FastAPI

from fastmcp import FastMCP

from tools.expenses import add_expenses, list_expenses, edit_expenses, delete_expenses

app = FastAPI()

mcp = FastMCP(
    name="expense-tracker mcp",
    instructions="""
    AI interface for the Expense Tracker application.

    Use authentication tools before accessing
    user resources.

    All operations respect the same validation,
    permissions, and business logic as the web app.
    """
)

mcp.tool(name=list_expenses, description="Get all expenses for the authenticated user")

mcp.tool(name=add_expenses, description="adding the expenses for the authenticated user ")

mcp.tool(name=edit_expenses, description="edit the expenses for the authenticated user ")

mcp.tool(name=delete_expenses, description="delete the expenses for the authenticated user ")


app.mount("/mcp", mcp.http_app())



























# import random
# from fastmcp import FastMCP


# mcp = FastMCP(name= "expense tracker mcp server ");

# @mcp.tool()
# def roll_dice(n_dice: int) -> list[int]:
#     """return no. between 1 to 6 for n dices """
#     return [random.randint(1, 6) for _ in range (n_dice)]


# @mcp.tool()
# def addition(a : float,  b : float) -> float:
#     """return the addition of two numbers """
#     return a+b;


# if __name__ == "__main__":
#     mcp.run

