# Phase 1: Project Setup + UI Shell

## Implementation Completed
- Established a modular project architecture separating frontend, backend, and documentation.
- Created the React frontend using Vite, TypeScript, and Tailwind CSS.
- Developed a professional UI shell with a sidebar, top navigation, and working theme toggler (Light/Dark/System).
- Designed placeholder pages for Dashboard, New Analysis, Standards, Analysis History, and Specification Builder.
- Implemented the Settings page which verifies the actual connection to the FastAPI backend.
- Created a minimal FastAPI backend with CORS enabled for the frontend.
- Added `/api/health` endpoint to verify the backend is running.

## Project Structure
```text
ManakSetu/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── .env
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── venv/
│   └── requirements.txt
└── docs/
```

## Tech Stack & Ports
- **Frontend**: React + Vite + Tailwind CSS + React Router
- **Frontend Port**: `5174` (URL: `http://localhost:5174`)
- **Backend**: FastAPI (Python)
- **Backend Port**: `8002` (URL: `http://127.0.0.1:8002`)
- **API Base**: `http://127.0.0.1:8002/api`
- **Health Endpoint**: `http://127.0.0.1:8002/api/health`

## Environment Variables
- `VITE_API_BASE_URL=http://127.0.0.1:8002/api` (Frontend)

## How to Start Frontend
1. Navigate to `frontend/` directory.
2. Run `npm install`.
3. Run `npm run dev`.

## How to Start Backend
1. Navigate to `backend/` directory.
2. Activate virtual environment (`venv\Scripts\activate`).
3. Run `python -m uvicorn app.main:app --host 127.0.0.1 --port 8002`.

## Not Implemented
- **Phase 2 has NOT been implemented.**
- No real AI integration.
- No database connection (PostgreSQL/pgvector).
- No actual standards data loaded.
