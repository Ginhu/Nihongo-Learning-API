import pytest
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)

def test_hash_and_verify_password():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_and_decode_access_token():
    token = create_access_token("user-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "access"

def test_create_and_decode_refresh_token():
    token = create_refresh_token("user-123")
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["type"] == "refresh"

def test_decode_invalid_token_raises():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        decode_token("not.a.valid.token")
    assert exc.value.status_code == 401
