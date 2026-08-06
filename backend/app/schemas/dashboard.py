from pydantic import BaseModel


class ExpenseSummary(BaseModel):
    title: str
    amount: float


class DashboardSummary(BaseModel):
    total_expenses: int
    total_amount: float
    this_month_total: float
    average_expense: float
    highest_expense: ExpenseSummary | None = None
    latest_expense: ExpenseSummary | None = None