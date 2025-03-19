# /home/ubuntu/lms/backend/app/main.py
from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# Import components
from .database import engine
from .models import Base
from .routes import lessons, exercises, users
from .routes import exercise_routes, log_routes
from .routes import auth_routes, user_routes
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .schemas import SubmissionRequest, SubmissionResponse
from . import crud

# Import configuration
from .config import (
    get_logger, 
    API_TITLE, API_DESCRIPTION, API_VERSION, API_DEBUG,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
)
from .middleware import RequestLoggingMiddleware

# Get application logger
logger = get_logger("api.main")

# Create FastAPI app with more detailed information
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    debug=API_DEBUG
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware, log_headers=False)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(exercise_routes.router, prefix="/api/exercises", tags=["Exercises"])
app.include_router(log_routes.router, prefix="/api/logs", tags=["Logs"])

# Include legacy routers
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(exercises.router, prefix="/api/exercise-templates", tags=["Exercise Templates"])
app.include_router(users.router, prefix="/api/admin/users", tags=["Admin Users"])

@app.on_event("startup")
async def startup_event():
    """Actions to run on application startup."""
    logger.info("Starting up LMS API")
    # We'll keep the table creation in Alembic migrations

@app.on_event("shutdown")
async def shutdown_event():
    """Actions to run on application shutdown."""
    logger.info("Shutting down LMS API")

@app.get("/", tags=["root"])
async def read_root():
    """API Root - redirects to documentation."""
    return {"message": "Welcome to the LMS API. See /docs for documentation."}

# Add submission endpoint directly to main
@app.post("/api/submit/", tags=["Submissions"], response_model=SubmissionResponse)
async def submit_answer(data: SubmissionRequest = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Submit an answer to an exercise.
    
    This endpoint is for backward compatibility. New applications should use 
    the `/api/exercises/submit/` endpoint instead.
    
    Parameters:
        data: The submission data including exercise ID, user ID, and answer
        db: Database session dependency
        
    Returns:
        A response with submission confirmation and score
        
    Raises:
        HTTPException: If the exercise doesn't exist or the request is invalid
    """
    submission = await crud.create_submission(db, data)
    return {"message": "Answer submitted", "score": submission.score}


# Customize the OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme for JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Apply security to all routes except authentication routes
    for path in openapi_schema["paths"]:
        if not path.startswith("/api/auth/login") and not path.startswith("/api/auth/register"):
            if "security" not in openapi_schema["paths"][path]:
                openapi_schema["paths"][path]["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi