from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router

from backend.auth.routes import router as auth_router
from backend.auth.dependencies import get_current_user

app = FastAPI(
    title="Kairova API",
    swagger_ui_parameters={"persistAuthorization": True}
)

# ---------------------------
# CORS CONFIG (SAFE FOR DEV + FUTURE DEPLOYMENT)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🔥 DATABASE CONTROLLED BY ALEMBIC (NO AUTO INIT)")

# ---------------------------
# ROUTES
# ---------------------------
app.include_router(auth_router)

app.include_router(
    api_router,
    prefix="/api",
)

# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/")
def home():
    return {"status": "kairova backend running"}

# ---------------------------
# USER INFO
# ---------------------------
@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email
    }

# ---------------------------
# PROTECTED TEST ROUTE
# ---------------------------
@app.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {
        "message": "Protected route working",
        "user_id": current_user.id,
        "email": current_user.email
    }