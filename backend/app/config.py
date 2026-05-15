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

    SPOTIFY_CLIENT_ID: str | None = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET: str | None = os.getenv("SPOTIFY_CLIENT_SECRET")

settings = Settings() # Create an instance of the Settings class to access configuration values throughout the application