from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1
    )

    amount: Decimal = Field(
        ...,
        gt=0,
        description="Transaction amount"
    )

    date: datetime = Field(
        default_factory=datetime.now
    )

    category: Literal[
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

    type: Literal[
        "INCOME",
        "EXPENSE",
    ]

    note: str | None = None