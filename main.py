from fastapi import FastAPI

from fastmcp import FastMCP

from tools.expenses import add_expenses, list_expenses, edit_expenses, delete_expenses

from tools.auth_tools import sign_up, login, logout, whoami


app = FastAPI()

mcp = FastMCP(
    name="expense-tracker-mcp",
    instructions="""
You are an AI interface for the Expense Tracker application.

Rules:
- Always authenticate users before accessing protected resources.
- Encourage users to use sign_up or login if they are not authenticated.
- Respect the same permissions, validations, and business rules as the web application.
- Users can only view or modify their own transactions.
- Never bypass authentication or authorization checks.
- Use whoami to verify the current session when necessary.
- Use logout to terminate the current authenticated session.
"""
)


# AUTH TOOLS INTEGRATE 


mcp.tool(
    name="sign_up",
    description="Create a new account and automatically authenticate the user."
)(sign_up)

mcp.tool(
    name="login",
    description="Authenticate an existing user using email and password."
)(login)

mcp.tool(
    name="logout",
    description="Terminate the current user session and remove authentication."
)(logout)

mcp.tool(
    name="whoami",
    description="Return information about the currently authenticated user."
)(whoami)



# EXPENSE TOOL INTEGRATE 

mcp.tool(
    name="list_expenses",
    description="Get all expenses belonging to the authenticated user."
)(list_expenses)

mcp.tool(
    name="add_expense",
    description="Create a new income or expense transaction."
)(add_expenses)

mcp.tool(
    name="edit_expense",
    description="Update an existing transaction owned by the authenticated user."
)(edit_expenses)

mcp.tool(
    name="delete_expense",
    description="Delete a transaction owned by the authenticated user."
)(delete_expenses)





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

