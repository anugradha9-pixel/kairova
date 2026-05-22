from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import settings

from backend.api.router import api_router
from backend.auth.routes import router as auth_router
from backend.auth.dependencies import get_current_user

from backend.core.exceptions import AppException
from backend.core.handlers import app_exception_handler


# =====================================
# APP INITIALIZATION
# =====================================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)


# =====================================
# EXCEPTION HANDLERS
# =====================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# =====================================
# CORS CONFIGURATION
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# ROUTERS
# =====================================

app.include_router(auth_router)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
)


# =====================================
# STARTUP LOG
# =====================================

@app.on_event("startup")
def startup_event():
    print(f"🔥 {settings.APP_NAME} backend started successfully")


# =====================================
# HEALTH CHECK
# =====================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# =====================================
# AUTH TEST ENDPOINT (/me)
# =====================================

@app.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "last_login_at": current_user.last_login_at,
    }


# =====================================
# PROTECTED TEST ROUTE
# =====================================

@app.get("/protected")
def protected_route(
    current_user=Depends(get_current_user),
):
    return {
        "message": "Protected route working",
        "user_id": current_user.id,
        "email": current_user.email,
    }