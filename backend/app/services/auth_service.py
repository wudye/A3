
from datetime import datetime
from re import U
from typing import Optional, Tuple
import zoneinfo
from alembic.op import execute
from certifi import where
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, update
import uuid

from app.models import refresh_token
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.jwt_utils import jwt_manager

class AuthService:
    """认证服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self,  username: str,  email: str,  passwrod: str) -> User:
        "register new user"
        # check username and email exits
        stmt = select(User).where((User.username == username) | (User.email == email))
        result: Result[Tuple[User]] = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            if existing_user.username == username:
                raise ValueError("Username already exists")
            else:
                raise ValueError("Email already exists")
            
        user = User(username=username, email=email)
        user.set_password(passwrod)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user or not user.verify_password(password):
            return None
        if not user.is_active:
            raise ValueError("User is banned and not active")
        return user
    
    async def create_token_pair(self, user: User, device_info: Optional[str] = None) -> Tuple[str, str, RefreshToken]:
        access_token = jwt_manager.create_access_token(
            data={
                "sub": str(user.id),
                "username": user.username,
                "email": user.email,
            }
        )
    
        refresh_token_str = jwt_manager.create_refresh_token(
            {
                "sub": access_token,
                "jti": str(uuid.uuid4()),
            })
        
        decoded = jwt_manager.decode_token(refresh_token_str)
        if not decoded:
            raise ValueError("Invalid refresh token")
        expires_at = datetime.fromtimestamp(decoded["exp"], zoneinfo.ZoneInfo("Europe/Vienna"))
        refresh_token = RefreshToken(
            user_id = user.id,
            token = refresh_token_str,
            device_info = device_info,
            expire_at = expires_at
        ) 

        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return access_token, refresh_token_str, refresh_token
    
    async def refresh_access_token(self, refresh_token_str: str) -> Optional[Tuple[str, str]]:
        payload = jwt_manager.verify_token(refresh_token_str, "refresh")
        if not payload:
            return None
        
        stmt = select(RefreshToken).where(RefreshToken.token == refresh_token_str,
                                          RefreshToken.is_revoked == False,
                                          RefreshToken.expire_at > datetime.now(zoneinfo.ZoneInfo("Europe/Vienna")))
        result = await self.db.execute(stmt)
        refresh_token = result.scalar_one_or_none()
        if not refresh_token:
            return None
        
        # get user
        stmt = select(User).where(User.id == refresh_token.user_id, User.is_active == True)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        
        # create new token pair
        access_token = jwt_manager.create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "email": user.email,
            }
        )
        new_refresh_token_str = None
        if payload.get("jti"):
            new_refresh_token_data = {
                "sub": str(user.id),
                "jti": str(uuid.uuid4())
            }
            new_refresh_token_str = jwt_manager.create_refresh_token(new_refresh_token_data)
            decoded = jwt_manager.decode_token(new_refresh_token_str)
            if not decoded:
                raise ValueError("Invalid refresh token")
            
            expires_at = datetime.fromtimestamp(decoded["exp"], zoneinfo.ZoneInfo("Europe/Vienna"))

            refresh_token.token = new_refresh_token_str
            refresh_token.expire_at = expires_at
            await self.db.commit()
        
        return access_token, new_refresh_token_str or refresh_token_str

    async def revoke_refresh_token(self, refresh_token_str: str) -> bool:
        stmt = select(RefreshToken).where(RefreshToken.token == refresh_token_str)
        result = await self.db.execute(stmt)
        refresh_token = result.scalar_one_or_none()
        if refresh_token and not refresh_token.is_revoked:
            refresh_token.is_revoked = True
            await self.db.commit()
            return True
        return False

    async def revoke_all_user_tokens(self, user_id: int) -> int:
        stmt = update(RefreshToken).where(RefreshToken.user_id == user_id,             RefreshToken.is_revoked == False
    ).values(is_revoked=True)
        result =  await self.db.execute(stmt)
        await self.db.commit()
        return getattr(result, "rowcount", 0)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()