# JWT Authentication Service with FastAPI

This project is a **FastAPI backend** for user authentication using **JWT tokens** with **real-time session management**.

---

## Features

- **JWT Authentication** – Generate and validate JWT tokens for users.
- **Real-time Session Management** –  
  - **Hash map** (`dict`) for O(1) active session lookups  
  - **Priority queue** (`heapq`) to efficiently expire/revoke tokens
- **Logout / Token Revocation** – Tokens are removed from active sessions immediately.
- **Protected Routes** – Only accessible with a valid token.
- **Unit Tests** – Test login, logout, and invalid token handling.

---

## Tech Stack

- Python 3.10  
- FastAPI  
- Uvicorn  
- python-jose (JWT)  
- pytest  