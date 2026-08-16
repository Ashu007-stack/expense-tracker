from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.agents.manager.agent_manager import AgentManager
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

# Create one manager instance
agent_manager = AgentManager()


def create_expense(
    db: Session,
    expense: ExpenseCreate,
    current_user: User,
) -> Expense:

    # AI categorization
    result = agent_manager.categorize(
        title=expense.title,
        description=expense.description or "",
    )

    db_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=result.category,
        category_confidence=result.confidence,
        category_source=result.provider.lower(),
        description=expense.description,
        expense_date=expense.expense_date,
        owner_id=current_user.id,
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def get_user_expenses(
    db: Session,
    current_user: User,
    category: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10,
):
    query = (
        db.query(Expense)
        .filter(
            Expense.owner_id == current_user.id
        )
    )

    # Category filter — case-insensitive
    if category:
        query = query.filter(
            Expense.category.ilike(category)
        )

    # Search title or description — case-insensitive
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            Expense.title.ilike(search_term)
            | Expense.description.ilike(search_term)
        )

    # Pagination calculation
    offset = (page - 1) * limit

    return (
        query
        .order_by(
            Expense.created_at.desc()
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_expense_by_id(
    db: Session,
    expense_id: int,
    current_user: User,
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.owner_id == current_user.id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )

    return expense


def update_expense(
    db: Session,
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User,
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.owner_id == current_user.id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )

    update_data = expense_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(
    db: Session,
    expense_id: int,
    current_user: User,
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.owner_id == current_user.id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )

    db.delete(expense)
    db.commit()