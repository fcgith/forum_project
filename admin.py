from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from models import Users
from schemas import AdminResponse
from utils import get_current_user

router = APIRouter(
    tags=["admin"]
)

@router.get("/", response_model=AdminResponse)
def admin_access(current_user: Users = Depends(get_current_user)) -> AdminResponse:
    if not current_user.admin:
        not_admin = HTTPException\
            (
                status_code=403,
                detail="You do not have permission to access this page."
            )
        raise not_admin

    result = AdminResponse\
    (
        username=current_user.username,
        email=current_user.email,
        age=current_user.age,
        nickname=current_user.nickname,
        admin=current_user.admin
    )

    return result