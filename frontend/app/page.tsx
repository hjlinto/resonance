"use client";
/**
 * Application landing page.
 * 
 * This page owns the responsibility of presenting the initial login entry
 * point for the Resonance frontend.
 */
import Image from "next/image";

export default function Home() {
  /**
   * Redirect the browser to the backend Spotify login route.
   * 
   * The frontend does not handle OAuth directly. The backend owns
   * Spotify authorization responsibilites.
   */
  function handleSpotifyLogin(): void {
    window.location.href = 
    "http://127.0.0.1:8000/auth/spotify/login";
  }
  
  return (
    <main className="flex min-h-screen items-center justify-center">
      <button
        onClick={handleSpotifyLogin}
        className="rounded bg-green-500 px-6 py-3 text-white"
        >
          Login with Spotify
        </button>
    </main>
  );
}