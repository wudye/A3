from os import device_encoding
from pydoc import describe
from tokenize import TokenError

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.postgres_manager import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.token import Token, TokenRefresh, TokenResponse
from app.services import auth_service
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

"""
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "username": "alice",
                        "email": "alice@example.com",
                        "password": "secret123"
                    }
                }
            }
        }
    },
)
async def register(...):
    ...

"""

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="new user register", description="create a new user")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db),):
    """用户注册"""
    auth_service = AuthService(db)
    try:
        user = await auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            passwrod=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token, summary="user login", description="user login")
async def login(
    login_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    client_host = request.client.host if request.client else "unknown"
    device_info = login_data.device_info or f"{client_host} - {request.headers.get('user-agent', 'Unknown')}"



    access_token, refresh_token_str, refresh_token = await auth_service.create_token_pair(
        user=user,
        device_info=device_info
    
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    
    """刷新访问令牌"""
    auth_service = AuthService(db)
    result = await auth_service.refresh_access_token(token_data.refresh_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token, refresh_token = result
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token if refresh_token != token_data.refresh_token else None
    )

@router.post("/logout")
async def logout(
    token_data: TokenRefresh,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    success = await auth_service.revoke_refresh_token(token_data.refresh_token)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的刷新令牌"
        )
    
    return {"message": "登出成功"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user


@router.post("/logout-all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """撤销用户的所有令牌"""
    auth_service = AuthService(db)
    count = await auth_service.revoke_all_user_tokens(current_user.id)
    
    return {"message": f"已撤销 {count} 个令牌"}


@router.get("/authtest")
async def get_current_user_info():
    return "auth test"
