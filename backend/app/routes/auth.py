"""
Authentication routes for the application.

This module defines the routes related to user authentication, including login, logout, and registration. 
It uses FastAPI for handling HTTP requests and responses, and integrates with the authentication 
service to manage user sessions and credentials.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from requests import HTTPError

from app.db.database import SessionLocal
from app.config import settings
from app.services.spotify_api_service import get_current_spotify_user
from app.services.spotify_token_service import upsert_spotify_token
from app.services.spotify_auth_service import build_spotify_login_url
from app.services.spotify_auth_service import exchange_code_for_token
from app.services.spotify_ingestion_service import upsert_user

from urllib.parse import urlencode

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/spotify/login")
def spotify_login() -> RedirectResponse:
    """
    Redirects the user to the Spotify login page.

    The route only handles HTTP behavior. The URL-building logic lives in the Spotify 
    auth service so it can be tested and reused in other contexts.
    """
    
    login_url = build_spotify_login_url()

    return RedirectResponse(url=login_url)

@router.get("/spotify/callback")
def spotify_callback(
    code: str | None = Query(default=None),
    error: str | None = Query(default=None),
) -> dict:
    """
    Handle Spotify's OAuth callback.
    
    Spotify redirects to this endpoint with either an authorization code
    or an error message. If a code is provided, we exchange it for an access 
    token. If an error is provided, we raise an HTTPException with the error details.
    """

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify authentication failed: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Spotify authentication failed: No code provided")
    
    try:
        token_response = exchange_code_for_token(code)

    except HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to exchange Spotify authorization code for access token.",
        ) from exc
    
    spotify_user = get_current_spotify_user(token_response["access_token"])

    db = SessionLocal()

    try:
        user = upsert_user(db=db, spotify_profile=spotify_user)

        upsert_spotify_token(
            db=db,
            spotify_user_id=spotify_user["id"],
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
            expires_in=token_response["expires_in"],
        )

        user_id = user.id

    finally:
        db.close()

    # Redirects an authenticated Spotify user to the frontend application
    frontend_redirect_url = (
        f"{settings.FRONTEND_URL}/dashboard?"
        + urlencode(
            {
                "spotify_user_id": spotify_user["id"],
            }
        )
    )

    print("Redirecting to frontend:", frontend_redirect_url)
    return RedirectResponse(frontend_redirect_url)

