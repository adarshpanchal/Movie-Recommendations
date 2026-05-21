# Movie Recommender App

A full-stack movie recommendation app with:
- Flask backend API
- React (Vite) frontend UI

## Project Structure

```text
react/
├── backend/
│   ├── app.py
│   ├── recommendations.py
│   ├── extraction.py
│   └── data/
└── frontend/
    ├── src/
    ├── package.json
    └── index.html
```

## Features

- Movie title search suggestions
- Recommendation results based on selected movie
- Poster + rating display for recommended movies
- Dark cinematic UI

## Requirements

- Python 3.9+
- Node.js 18+
- npm

## Backend Setup (Flask)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install flask pandas scikit-learn python-dotenv requests
```

### Generate model files (first time only)

If `movies.pkl` and `similar.pkl` do not exist in `backend/`, run:

```bash
cd backend
python3 extraction.py
```

### Run backend

```bash
cd backend
python3 app.py
```

Backend runs on:
- `http://127.0.0.1:3000`

## Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:
- `http://localhost:5173`

## How to Use

1. Open `http://localhost:5173`.
2. Type a movie name.
3. Select a suggestion or click **Recommend**.
4. View recommendation cards with poster and rating.

## API Endpoints

- `GET /` : health text response
- `GET /search?query=<movie>` : returns up to 10 matching movie titles
- `GET /recommend?movie=<movie>` : returns recommended movie objects

Example recommendation response:

```json
[
  {
    "title": "Inception",
    "movie_id": 27205,
    "rating": 8.8,
    "poster": "https://image.tmdb.org/t/p/w500/..."
  }
]
```

## Environment Variables

Create `backend/.env`:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

Without a valid TMDB key, fallback placeholder posters may be shown.

## Troubleshooting

- Blank page / only background visible:
  - Ensure frontend dev server is running (`npm run dev`).
  - Hard refresh browser (`Cmd + Shift + R` on macOS).

- `React is not defined`:
  - Ensure latest frontend code is pulled (fixed in current version).

- No recommendations shown:
  - Ensure backend is running on port `3000`.
  - Verify exact movie title exists in dataset.

- CORS/network errors:
  - Check backend terminal logs.
  - Confirm frontend calls `http://127.0.0.1:3000`.

## Build Frontend for Production

```bash
cd frontend
npm run build
npm run preview
```

## Future Improvements

- Add loading skeletons
- Add pagination / more recommendations
- Add genre/year filters
- Add Docker setup for one-command run
