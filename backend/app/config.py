"""
Application configuration.

This module owns environment-based settings for the backend.

Keeping this in a separate file allows us to easily manage and override settings for different environments (development, testing, production).
"""


import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  # Load environment variables from .env file

class Settings(BaseSettings):
    """
    Centralized application settings loaded from environment variables.

    Each attribute corresponds to a specific configuration parameter that can be set via environment variables.
    """

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    SPOTIFY_CLIENT_ID: str = os.getenv("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET: str = os.getenv("SPOTIFY_CLIENT_SECRET", "")
    SPOTIFY_AUTH_URL: str = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL: str = "https://accounts.spotify.com/api/token"
    SPOTIFY_SCOPES: str = "user-top-read playlist-modify-private playlist-modify-public"
    SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI", "") # Redirect URI for Spotify OAuth, should be set in environment variables
    TOKEN_ENCRYPTION_KEY: str = os.getenv("TOKEN_ENCRYPTION_KEY") # Encryption key for securing sensitive tokens, should be set in environment variables

    FRONTEND_URL: str | None = os.getenv("FRONTEND_URL") # URL of the frontend application, used for CORS and redirect URIs

settings = Settings() # Create an instance of the Settings class to access configuration values throughout the application