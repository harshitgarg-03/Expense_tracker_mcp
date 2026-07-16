# tools/transactions.py

from datetime import date as Date
from typing import Literal

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from fastmcp.exceptions import ToolError

from db import get_pool


TransactionType = Literal[
    "INCOME",
    "EXPENSE",
]

TransactionCategory = Literal[
    "Food",
    "Travel",
    "Bills",
    "Entertainment",
    "Shopping",
    "Health",
    "Salary",
    "Freelance",
    "Other",
]


def _current_user_id() -> str:
    """The JWT's `sub` claim is the SAME user.id Better Auth uses everywhere
    else in the app — this is the whole trick. No lookup table, no mapping."""
    

    token = get_access_token()

    if token is None:
        raise ToolError("Not authenticated")

    user_id = token.claims.get("sub")

    if not user_id:
        raise ToolError("Invalid authentication token")

    return user_id


def register_transaction_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_recent_expenses() -> list[dict]:
        """List the authenticated user's most recent expenses."""
        user_id = _current_user_id()
        pool = await get_pool()
        rows = await pool.fetch(
            """
            SELECT id, amount, category, description, created_at
            FROM expenses
            WHERE user_id = $1
            ORDER BY created_at DESC
            """,
            user_id,
        )
        return [dict(r) for r in rows]

    @mcp.tool()
    async def add_transaction(
        title: str,
        amount: float,
        type: TransactionType = "EXPENSE",
        category: TransactionCategory = "Other",
        note: str | None = None,
        date: Date | None = None,
    ) -> dict:
        """
        Add a new income or expense transaction
        for the authenticated user.
        """

        user_id = _current_user_id()

        if not title.strip():
            raise ToolError("Title cannot be empty")

        if amount <= 0:
            raise ToolError("Amount must be greater than zero")

        transaction_date = date or Date.today()

        pool = await get_pool()

        row = await pool.fetchrow(
            """
            INSERT INTO "Expense"
            (title, amount, type, category, note, "userId", date)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *
            """,
            title.strip(),
            amount,
            type,
            category,
            note,
            user_id,
            transaction_date,
        )

        return dict(row)


    @mcp.tool()
    async def update_transaction(
        transaction_id: str,
        title: str | None = None,
        amount: float | None = None,
        type: TransactionType | None = None,
        category: TransactionCategory | None = None,
        note: str | None = None,
        date: Date | None = None,
    ) -> dict:
            """
            Update an existing transaction.

            Only provided fields are updated.
            """

            user_id = _current_user_id()

            if title is not None and not title.strip():
                raise ToolError("Title cannot be empty")

            if amount is not None and amount <= 0:
                raise ToolError("Amount must be greater than zero")

            updates = []
            values = []

            if title is not None:
                values.append(title.strip())
                updates.append(f"title = ${len(values)}")

            if amount is not None:
                values.append(amount)
                updates.append(f"amount = ${len(values)}")

            if type is not None:
                values.append(type)
                updates.append(f"type = ${len(values)}")

            if category is not None:
                values.append(category)
                updates.append(f"category = ${len(values)}")

            if note is not None:
                values.append(note)
                updates.append(f"note = ${len(values)}")

            if date is not None:
                values.append(date)
                updates.append(f"date = ${len(values)}")

            if not updates:
                raise ToolError("No fields provided to update")

            updates.append('"updatedAt" = NOW()')

            values.append(transaction_id)
            transaction_index = len(values)

            values.append(user_id)
            user_index = len(values)

            query = f"""
                UPDATE "Expense"
                SET {", ".join(updates)}
                WHERE id = ${transaction_index}
                AND "userId" = ${user_index}
                RETURNING *
            """

            pool = await get_pool()

            row = await pool.fetchrow(
                query,
                *values,
            )

            if row is None:
                raise ToolError("Transaction not found")

            return dict(row)

    
    @mcp.tool()
    async def delete_transaction(
    transaction_id: str,
) -> dict:
        """
        Delete a transaction of the authenticated user.
        """

        user_id = _current_user_id()

        pool = await get_pool()

        row = await pool.fetchrow(
            """
            DELETE FROM "Expense"
            WHERE id = $1
            AND "userId" = $2
            RETURNING *
            """,
            transaction_id,
            user_id,
        )

        if row is None:
            raise ToolError("Transaction not found")

        return {
            "message": "Transaction deleted successfully",
            "transaction": dict(row),
        }