/**
 * Spotify-related frontend API calls.
 * 
 * This module owns frontend communication with backend Spotify endpoints.
 * 
 * React components should not build API URLs directly because API interaction
 * belongs in a dedicated service layer.
 */

import api from "./api";

export async function fetchTopTracks(spotifyUserId: string) {
    const response = await api.get(
        `/spotify/${spotifyUserId}/top-tracks`
    );
    
    return response.data;
}

export async function fetchRecommendations(spotifyUserId: string) {
    const response = await api.get(
        `/spotify/${spotifyUserId}/recommendations`
    );

    return response.data;
}