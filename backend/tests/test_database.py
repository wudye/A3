
from zoneinfo import ZoneInfo

import pytest
from app.models.user import User
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_user_model(test_session):
    user = User(
        username="testuser",
        email="test@example.com"
    )
    user.set_password("password123")
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.verify_password("password123") is True
    assert user.verify_password("wrongpassword") is False


@pytest.mark.asyncio
async def test_refresh_token_model(test_session):
    user = User(
        username="testuser",
        email="test@example.com")
    user.set_password("password123")
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    expires_at = datetime.now(ZoneInfo("Europe/Vienna")) + timedelta(days=7)
    # expires_at = datetime.now() + timedelta(days=7)
    refresh_token = RefreshToken(
        user_id=user.id,
        token="test_refresh_token",
        device_info="test_device",
        expire_at=expires_at
    )
    test_session.add(refresh_token)
    await test_session.commit()
    await test_session.refresh(refresh_token)

    assert refresh_token.id is not None
    assert refresh_token.user_id == user.id     
    assert refresh_token.token == "test_refresh_token"
    assert refresh_token.device_info == "test_device"
    assert refresh_token.expire_at == expires_at

