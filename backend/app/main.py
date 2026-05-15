"""
Application entry point for the Resonance backend API.

This file owns the responsibility of creating the FastAPI app instance, 
registering global settings, and exposing health-check routes used 
during local development and deployment.
"""

from fastapi import FastAPI
from app.routes.test_db import router as test_db_router
from app.routes.test_config import router as test_config_router

app = FastAPI(
    title="Resonance API",
    description="Backend API for the Resonance music recommendation system.",
    version="0.1.0")

app.include_router(test_config_router)
app.include_router(test_db_router)

@app.get("/health")
def health_check():
    """
    Confirm that the backend API is running.
    """
    return {"status": "ok"}
