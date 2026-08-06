from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummary,
    ExpenseSummary,
)


def get_dashboard_summary(
    db: Session,
    current_user: User,
) -> DashboardSummary:

    # Total number of expenses
    total_expenses = (
        db.query(Expense)
        .filter(Expense.owner_id == current_user.id)
        .count()
    )

    # Total amount spent
    total_amount = (
        db.query(
            func.coalesce(func.sum(Expense.amount), 0)
        )
        .filter(Expense.owner_id == current_user.id)
        .scalar()
    )

    # Current date
    today = date.today()

    # Total amount spent this month
    this_month_total = (
        db.query(
            func.coalesce(func.sum(Expense.amount), 0)
        )
        .filter(
            Expense.owner_id == current_user.id,
            func.extract("year", Expense.expense_date) == today.year,
            func.extract("month", Expense.expense_date) == today.month,
        )
        .scalar()
    )

    # Average expense
    average_expense = (
        float(total_amount) / total_expenses
        if total_expenses > 0
        else 0.0
    )

    # Highest expense
    highest_expense = (
        db.query(Expense)
        .filter(Expense.owner_id == current_user.id)
        .order_by(Expense.amount.desc())
        .first()
    )

    # Latest expense
    latest_expense = (
        db.query(Expense)
        .filter(Expense.owner_id == current_user.id)
        .order_by(Expense.created_at.desc())
        .first()
    )

    return DashboardSummary(
        total_expenses=total_expenses,
        total_amount=float(total_amount),
        this_month_total=float(this_month_total),
        average_expense=average_expense,
        highest_expense=(
            ExpenseSummary(
                title=highest_expense.title,
                amount=highest_expense.amount,
            )
            if highest_expense
            else None
        ),
        latest_expense=(
            ExpenseSummary(
                title=latest_expense.title,
                amount=latest_expense.amount,
            )
            if latest_expense
            else None
        ),
    )