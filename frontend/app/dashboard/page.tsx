"use client";

/**
 * Dashboard page.
 * 
 * This page owns the responsibility of displaying Spotify listening data after successful authentication.
 */

import { useEffect, useState } from "react";
import { fetchTopTracks, fetchRecommendations } from "@/services/spotify";

interface SpotifyTrack {
    id: string;
    name: string;

    /**
     * Additional Spotify metadata used for dashboard rendering.
     */
    artists: { name: string }[];
    album: {
        name: string;
        images: { url: string }[];
    };
    popularity?: number;
}

interface RecommendationTrack {
    track_id: number;
    spotify_track_id: string;
    name: string;
    artist_name: string | null;
    album_name: string | null;
    album_image_url: string | null;
    preview_url: string | null;
    score: number;
    reasons: string[];
}

export default function DashboardPage() {
    const [tracks, setTracks] = useState<SpotifyTrack[]>([]);
    const [recommendations, setRecommendations] = useState<RecommendationTrack[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        /**
         * Fetch Spotify top tracks from the backend.
         * 
         * The frontend only requests already-processed backend data and does not communicate directly with
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
                const topTracksData = await fetchTopTracks(spotifyUserId);
                const recommendationData = await fetchRecommendations(spotifyUserId);

                setTracks(topTracksData.items.slice(0, 10));
                setRecommendations(recommendationData.recommendations.slice(0, 20));

            } catch (error) {
                console.error("Failed to fetch Spotify dashboard data.", error)
        
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
            <h1 className="mb-6 text-3xl font-bold">
                Resonance Music Dashboard
            </h1>

            <section className="mb-10">
                <h2 className="mb-4 text-2xl font-semibold">
                    Your Top 10 Spotify Tracks
                </h2>

                <ul className="space-y-4">
                    {tracks.map((track, index) => (
                        <li
                            key={track.id}
                            className="flex items-center gap-4 rounded border p-4"
                        >
                            {track.album?.images?.[0]?.url && (
                                <img
                                    src={track.album.images[0].url}
                                    alt={`${track.name} album cover`}
                                    className="h-16 w-16 rounded object-cover"
                                />
                            )}

                            <div>
                                <p className="font-semibold">
                                    #{index + 1} — {track.name}
                                </p>

                                <p className="text-sm text-gray-500">
                                    {track.artists?.map((artist) => artist.name).join(", ")}
                                </p>

                                <p className="text-sm text-gray-400">
                                    {track.album?.name}
                                </p>

                                {track.popularity !== undefined && (
                                    <p className="text-xs text-gray-500">
                                        Popularity: {track.popularity}
                                    </p>
                                )}
                            </div>
                        </li>
                    ))}
                </ul>
            </section>

            <section>
                <h2 className="mb-4 text-2xl font-semibold">
                    Your Resonance Playlist
                </h2>

                <ul className="space-y-4">
                    {recommendations.map((track) => (
                        <li
                            key={track.track_id}
                            className="flex items-center gap-4 rounded border p-4"
                        >
                            {track.album_image_url && (
                                <img
                                    src={track.album_image_url}
                                    alt={`${track.name} album cover`}
                                    className="h-16 w-16 rounded object-cover"
                                />
                            )}

                            <div>
                                <p className="font-semibold">
                                    {track.name}
                                </p>

                                <p className="text-sm text-gray-500">
                                    {track.artist_name}
                                </p>

                                <p className="text-sm text-gray-400">
                                    {track.album_name}
                                </p>

                                <p className="mt-2 text-xs text-gray-500">
                                    Score: {track.score}
                                </p>

                                {track.reasons.map((reason) => (
                                    <p
                                        key={reason}
                                        className="text-xs text-gray-500"
                                    >
                                        {reason}
                                    </p>
                                ))}
                            </div>
                        </li>
                    ))}
                </ul>
            </section>
        </main>
    );
}