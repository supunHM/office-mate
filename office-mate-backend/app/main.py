"""
# GitHub Copilot: create a basic FastAPI application with:
# - CORS enabled for my React frontend at http://localhost:5173
# - a root GET "/" that returns {"status": "ok"}
# - include_router calls for documents and tasks from app.routers
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents, tasks

app = FastAPI(title="Office Mate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
