"use client";

/**
 * Dashboard page.
 * 
 * This page owns the responsibility of displaying Spotify listening data after successful authentication.
 */

import { useEffect, useState } from "react";
import { fetchTopTracks } from "@/services/spotify";

interface SpotifyTrack {
    id: string;
    name: string;
}

export default function DashboardPage() {
    const [tracks, setTracks] = useState<SpotifyTrack[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        /**
         * Fetch Spotify top tracks from the backend.
         * 
         * The frontend only requests already-processed backened data and does not communicate directly with
         * Spotify APIs.
         */
        async function loadTracks(): Promise<void> {
            const params = new URLSearchParams(window.location.search);

            const spotifyUserId = params.get("spotify_user_id");

            if (!spotifyUserId) {
                setLoading(false);
                return;
            }

            try {
                const data = await fetchTopTracks(spotifyUserId);

                setTracks(data.items);

            } catch (error) {
                console.error("Failed to fetch Spotify tracks.", error)
        
            } finally {
                setLoading(false);
            }
        }

        loadTracks();
    }, []);

    if (loading) {
        return (
            <main className="p-8">
                <p>Loading tracks...</p>
            </main>
        );
    }

    return (
        <main className="p-8">
            <h1 className="mb-6 text-3x1 font-bold">
                Your Top Tracks
            </h1>

            <ul className="space-y-3">
                {tracks.map((track) => (
                    <li
                    key={track.id}
                    className="rounded border p-4"
                    >
                        {track.name}
                    </li>
                ))}
            </ul>
        </main>
    );
}