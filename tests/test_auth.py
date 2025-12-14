import pytest
from fastapi.testclient import TestClient

def test_login_and_protected(client: TestClient):
    """Test login and access to protected endpoint."""
    # Login
    response = client.post("/auth/login")
    print(f"Login response: {response.status_code}, {response.json()}")  # Debug
    
    assert response.status_code == 200
    data = response.json()
    
    # Check the actual response structure
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    
    access_token = data["access_token"]
    
    # Access protected endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/protected", headers=headers)
    
    print(f"Protected response: {response.status_code}, {response.json()}")  # Debug
    assert response.status_code == 200
    assert "message" in response.json()

def test_invalid_token(client: TestClient):
    """Test accessing protected endpoint with invalid token."""
    # Test with invalid token
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/auth/protected", headers=headers)
    
    print(f"Invalid token response: {response.status_code}, {response.json()}")  # Debug
    
    # FastAPI with HTTPException will return 401
    assert response.status_code == 401
    assert "detail" in response.json()

def test_logout_revokes_token(client: TestClient):
    """Test that logout revokes the token."""
    # First login
    response = client.post("/auth/login")
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]
    
    # Use the token to access protected endpoint (should work)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/protected", headers=headers)
    assert response.status_code == 200
    
    # Now logout
    response = client.post("/auth/logout", headers=headers)
    print(f"Logout response: {response.status_code}, {response.json()}")  # Debug
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"
    
    # Try to use the token again (should fail after logout)
    response = client.get("/auth/protected", headers=headers)
    print(f"After logout response: {response.status_code}, {response.json()}")  # Debug
    assert response.status_code == 401  # Token should be revoked

def test_protected_without_token(client: TestClient):
    """Test protected endpoint without token."""
    response = client.get("/auth/protected")
    assert response.status_code == 422  # FastAPI returns 422 for missing required header

def test_protected_with_malformed_header(client: TestClient):
    """Test protected endpoint with malformed Authorization header."""
    headers = {"Authorization": "InvalidFormat"}
    response = client.get("/auth/protected", headers=headers)
    assert response.status_code == 401
    assert "Invalid authorization header" in response.json()["detail"]