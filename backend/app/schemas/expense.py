from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    description: str | None = None
    expense_date: date


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    amount: float | None = Field(default=None, gt=0)
    description: str | None = None
    expense_date: date | None = None


class ExpenseResponse(ExpenseBase):
    id: int
    category: str

    model_config = ConfigDict(
        from_attributes=True
    )