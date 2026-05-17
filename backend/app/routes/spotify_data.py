"""
Spotify data routes.

These routes expose Spotify listening data through our backend.

The routes coordinate HTTP behavior, database access, and service calls
while keeping Spotify API request details inside the service layer.
"""

from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.models.user import User
from app.models.track import Track
from app.services.spotify_api_service import get_user_top_artists, get_user_top_tracks
from app.services.spotify_auth_service import refresh_access_token
from app.services.spotify_ingestion_service import save_user_top_artists, save_user_top_tracks
from app.services.spotify_token_service import get_decrypted_access_token, update_access_token, get_decrypted_refresh_token
from app.services.recommendation_service import generate_recommendations_for_user


router = APIRouter(prefix="/spotify", tags=["spotify"])

def call_spotify_with_refresh(
        db,
        spotify_user_id: str,
        spotify_call,
) -> dict:
    """
    Call Spotify with the stored access token, refreshing it if the call fails due to an expired token.

    Route handles use this helper so each endpoint does not duplicate token refresh and retry logic.
    """

    access_token = get_decrypted_access_token(db, spotify_user_id)

    try:
        return spotify_call(access_token)
    
    except HTTPException as exc:
        if exc.status_code != 401:
            raise

        refresh_token = get_decrypted_refresh_token(db, spotify_user_id)
        refreshed_token_response = refresh_access_token(refresh_token)

        new_access_token = refreshed_token_response["access_token"]
        expires_in = refreshed_token_response["expires_in"]

        update_access_token(
            db=db,
            spotify_user_id=spotify_user_id,
            new_access_token=new_access_token,
            expires_in=expires_in,
        )

        return spotify_call(new_access_token)


@router.get("/{spotify_user}/top-tracks")
def get_top_tracks(spotify_user: str) -> dict:
    """
    Fetch the user's top tracks from Spotify from an authorized Spotify user.
    """

    spotify_user_id = spotify_user
    db = SessionLocal()

    try:
        return call_spotify_with_refresh(
            db=db,
            spotify_user_id=spotify_user_id,
            spotify_call=get_user_top_tracks,
        )
    
    # Exc is raised when the user doesn't exist or doesn't have a Spotify token
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    finally:
        db.close()

@router.get("/{spotify_user}/top-artists")
def get_top_artists(spotify_user: str) -> dict:
    """
    Fetch the user's top artists from Spotify from an authorized Spotify user.
    """

    spotify_user_id = spotify_user
    db = SessionLocal()

    try:
        return call_spotify_with_refresh(
            db=db,
            spotify_user_id=spotify_user_id,
            spotify_call=get_user_top_artists,
        )
    
    # Exc is raised when the user doesn't exist or doesn't have a Spotify token
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    finally:
        db.close()

@router.post("/{spotify_user_id}/sync")
def sync_spotify_data(spotify_user_id: str) -> dict:
    """
    Fetch and persist a user's top Spotify tracks and artists.
    """

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.spotify_user_id == spotify_user_id).first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        access_token = get_decrypted_access_token(db, spotify_user_id)

        top_tracks_response = get_user_top_tracks(access_token)
        top_artists_response = get_user_top_artists(access_token)

        save_user_top_artists(
            db,
            user,
            top_artists_response.get("items", []),
        )
        save_user_top_tracks(
            db,
            user, 
            top_tracks_response.get("items", []),
        )
        
        """
        This feature is commented out due to Spotify revoking access to audio features for tracks

        for spotify_track in top_tracks_response.get("items", []):
            track = db.query(Track).filter(
                Track.spotify_track_id == spotify_track["id"]
            ).first()

            if track is None:
                continue

            audio_features = get_track_audio_features(
                access_token,
                spotify_track["id"]
            )

            update_track_audio_features(db, track, audio_features)
        """
        return {
            "message": "Spotify data synced successfully",
            "top_tracks_saved": len(top_tracks_response.get("items", [])),
            "top_artists_saved": len(top_artists_response.get("items", [])),
        }

    finally:
        db.close()

@router.get("/{spotify_user_id}/recommendations")
def get_recommendations(spotify_user_id: str) -> dict:
    """Generate recommendations for a Spotify user from stored listening data."""
    db = SessionLocal()

    try:
        recommendations = generate_recommendations_for_user(
            db=db,
            spotify_user_id=spotify_user_id
        )

        return recommendations
    
    finally:
        db.close()


