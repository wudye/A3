from re import A

import pytest
from fastapi import status
from app.services import auth_service
from app.services.auth_service import AuthService

@pytest.mark.asyncio
async def test_register_user(test_session):
    auth_service = AuthService(test_session)
    user = await auth_service.register_user(
        username="testuser",
        email="test@example.com",
        passwrod="password123"

    )
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.verify_password("password123") is True

    with pytest.raises(ValueError, match="Username already exists"):
        await auth_service.register_user(
            username="testuser",
            email="test@example1.com",
            passwrod="password123"
        )

    with pytest.raises(ValueError, match="Email already exists"):
        await auth_service.register_user(
            username="testuser1",
            email="test@example.com",
            passwrod="password123"
        )

@pytest.mark.asyncio
async def test_authenticate_user(test_session):
    auth_service = AuthService(test_session)
    
    await auth_service.register_user(
        username="testuser",
        email="test@example.com",
        passwrod="password123"
    )
    user = await auth_service.authenticate_user(
        username="testuser",
        password="password123"
    )

    assert user is not None
    assert user.username == "testuser"
    assert user.verify_password("password123") is True

    user =await auth_service.authenticate_user(
        username="testuser",
        password="wrongpassword"
    )
    assert user is None

    user = await auth_service.authenticate_user(
        username="wronguser",
        password="password123"
    )
    assert user is None

@pytest.mark.asyncio
async def test_create_token_pair(test_session):
    """测试创建令牌对"""
    auth_service = AuthService(test_session)
    
    # 先注册用户

    user = await auth_service.register_user(
        username="testuser",
        email="test@example.com",
        passwrod="password123"
    )
    
    # 创建令牌对
    access_token, refresh_token, db_token = await auth_service.create_token_pair(
        user=user,
        device_info="Test Device"
    )
    
    assert access_token is not None
    assert refresh_token is not None
    assert db_token is not None
    assert db_token.user_id == user.id
    assert db_token.device_info == "Test Device"
    assert db_token.is_revoked is False

@pytest.mark.asyncio
async def test_refresh_access_token(test_session):
    """测试刷新访问令牌"""
    auth_service = AuthService(test_session)
    
    # 先注册用户并创建令牌对
    user = await auth_service.register_user(
        username="refreshuser",
        email="refresh@example.com",
        passwrod="password123"
    )

    
    _, refresh_token, _ = await auth_service.create_token_pair(user)
    
    # 刷新令牌
    result = await auth_service.refresh_access_token(refresh_token)
    assert result is not None
    
    new_access_token, new_refresh_token = result
    assert new_access_token is not None
    assert new_refresh_token is not None
    
    # 测试无效令牌
    result = await auth_service.refresh_access_token("invalid_token")
    assert result is None


@pytest.mark.asyncio
async def test_revoke_tokens(test_session):
    """测试撤销令牌"""
    auth_service = AuthService(test_session)
    
    # 先注册用户并创建令牌对
    user = await auth_service.register_user(
        username="refreshuser",
        email="refresh@example.com",
        passwrod="password123"
    )
    
    _, refresh_token, _ = await auth_service.create_token_pair(user)
    
    # 撤销单个令牌
    success = await auth_service.revoke_refresh_token(refresh_token)
    assert success is True
    
    # 再次撤销应该失败
    success = await auth_service.revoke_refresh_token(refresh_token)
    assert success is False
    
    # 创建多个令牌并全部撤销
    _, token1, _ = await auth_service.create_token_pair(user)
    _, token2, _ = await auth_service.create_token_pair(user)
    
    count = await auth_service.revoke_all_user_tokens(user.id)