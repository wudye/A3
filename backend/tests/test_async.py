import pytest
from main import say_hello

@pytest.mark.asyncio
async def test_say_hello():
    result = await say_hello("John")
    assert result == {"message": "Hello John"}