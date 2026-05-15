"""
Temporary configuration for testing purposes.

These routes verify that required environment variables are avaible during local
development and testing. They should not expose secret values.
"""

from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/test-config")
def test_config():
    """
    Test route to verify that required environment variables are available.

    This route checks for the presence of critical configuration values and returns a success message if they are set.
    It does not return the actual values to avoid exposing secrets.
    """
    required_vars = {
        "DATABASE_URL": settings.DATABASE_URL,
        "SPOTIFY_CLIENT_ID": settings.SPOTIFY_CLIENT_ID,
        "SPOTIFY_CLIENT_SECRET": settings.SPOTIFY_CLIENT_SECRET,
    }

    missing_vars = [var for var, value in required_vars.items() if not value]

    if missing_vars:
        return {"status": "error", "message": f"Missing environment variables: {', '.join(missing_vars)}"}

    return {"status": "success", "message": "All required environment variables are set."}


