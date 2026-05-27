from annotated_types import T
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client() :
    """创建测试客户端夹具"""
    with TestClient(app) as test_client:
        yield test_client