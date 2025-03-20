from fastapi import APIRouter, Depends
from thoughtgrove.core.deps import get_current_user
from thoughtgrove.models.user import User

router = APIRouter(prefix="/users", tags=["用户"])

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user 