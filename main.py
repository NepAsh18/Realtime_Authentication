# main.py
from fastapi import FastAPI
from routes.auth import auth_router

app = FastAPI(title="JWT Auth Service")
app.include_router(auth_router, prefix="/auth")  # important
