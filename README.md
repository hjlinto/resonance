# Resonance Music Engine

Spotify-connected music analytics and smart DJ recommendation platform.

---

# Backend Setup

## Start Backend

From repo root:

```bash
cd backend
```

Activate virtual environment:

```bash
source .venv/Scripts/activate
```

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## Start Frontend

From repo root:

```bash
cd frontend
```

Start Next.js app:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

# Login Flow

1. Open frontend
2. Click "Login with Spotify"
3. Authenticate with Spotify
4. Redirect back to dashboard
5. Dashboard fetches Spotify listening data from backend

---

# Current MVP Features

- Spotify OAuth authentication
- Encrypted Spotify token storage
- PostgreSQL persistence
- Spotify top tracks ingestion
- Spotify top artists ingestion
- Frontend dashboard
- Backend API service layer

---

# Current Architecture

```text
frontend/
    Next.js frontend UI

backend/
    FastAPI backend
    PostgreSQL persistence
    Spotify integration
```