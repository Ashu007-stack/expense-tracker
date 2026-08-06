from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)
from app.services.expense_service import (
    create_expense,
    get_user_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return create_expense(
        db=db,
        expense=expense,
        current_user=current_user,
    )

@router.get(
    "",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_expenses(
        db=db,
        current_user=current_user,
    )

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_expense_by_id(
        db=db,
        expense_id=expense_id,
        current_user=current_user,
    )

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_existing_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_expense(
        db=db,
        expense_id=expense_id,
        expense_data=expense,
        current_user=current_user,
    )

@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_expense(
        db=db,
        expense_id=expense_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )