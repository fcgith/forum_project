from fastapi import APIRouter, Depends

from models import Users
from schemas import AdminResponse
from utils import get_admin

router = APIRouter(
    tags=["admin"]
)

@router.get("/", response_model=AdminResponse)
def admin_access_test(admin: Users = Depends(get_admin)) -> AdminResponse:
    """
    Initial admin page (probably wrong because it's more FE-focused)
    """
    result = AdminResponse\
    (
        username=admin.username,
        email=admin.email,
        age=admin.age,
        nickname=admin.nickname,
        admin=admin.admin
    )
    return result