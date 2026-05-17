/**
 * Shared API client configuration.
 * 
 * This module owns the responsibility of configuring outbound requests to the
 * backend API so the rest of the frontend does not repeatedly define base URLs.
 */

import axios from "axios";

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

export default api;