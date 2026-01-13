"""
Office Mate API - AI-Powered Document Organizer with Smart To-Do List
Main FastAPI application with authentication, document management, and task management
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents, tasks, auth, tags, stats
from app.config import CORS_ORIGINS
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Office Mate API",
    description="AI-Powered Document Organizer with Smart To-Do List for Office Administration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """API health check"""
    return {
        "status": "ok",
        "message": "Office Mate API is running",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
app.include_router(stats.router, prefix="/stats", tags=["Statistics"])
