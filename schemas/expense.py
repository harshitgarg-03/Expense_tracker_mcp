from datetime import datetime, date as Date

from typing import Literal

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    id: str | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    amount: float | None = Field(
        default=None,
        gt=0,
        description="Transaction amount",
    )

    type: Literal[
        "INCOME",
        "EXPENSE"
    ] = "EXPENSE"

    category: Literal[
        "Food",
        "Travel",
        "Bills",
        "Entertainment",
        "Shopping",
        "Health",
        "Salary",
        "Freelance",
        "Other"
    ] = "Other"

    note: str | None = Field(
        default=None,
        max_length=500,
    )

    userId: str | None = None

    date: Date | None = Field(default_factory=Date.today)

    createdAt: datetime | None = None

    updatedAt: datetime | None = None