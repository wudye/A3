from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from dotenv import load_dotenv
from .pydantic_settings_config import settings
from zoneinfo import ZoneInfo
class JWTManager:
    """JWT 管理器"""

    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.expire_minutes = settings.jwt_expire_minutes
        self.algorithm = settings.jwt_alogrithm
        self.refresh_token_expire = settings.refresh_token_expire_days

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(ZoneInfo("Europe/Vienna")) + expires_delta
        else:
            expire = datetime.now(ZoneInfo("Europe/Vienna")) + timedelta(minutes=self.expire_minutes)

        to_encode.update({
            "exp": expire,
            "type" : "access"
        })

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        expire = datetime.now(ZoneInfo("Europe/Vienna")) + timedelta(days=self.refresh_token_expire)
        to_encode.update({
            "exp": expire,
            "type" : "refresh"
        })

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        try:
            playload: Dict[str, Any] = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if playload.get("type") == token_type:
                return playload
            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
        except jwt.ExpiredSignatureError:
            return None
        




jwt_manager = JWTManager()
