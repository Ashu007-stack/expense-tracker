from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ExpenseBase(BaseModel):
    title: str
    amount: float
    description: str | None = None
    expense_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    description: str | None = None
    expense_date: date | None = None


class ExpenseResponse(ExpenseBase):
    id: int

    category: str
    category_confidence: float
    category_source: str

    owner_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )