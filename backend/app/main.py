from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import standards, analysis, recommendations, gaps, specifications, history

app = FastAPI(title="ManakSetu API")

# Allow requests from the frontend Vite dev server
origins = [
    "http://localhost:5174",
    "https://manak-setu-liard.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

app.include_router(standards.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(recommendations.router)
app.include_router(gaps.router)
app.include_router(specifications.router)
app.include_router(history.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "ManakSetu"}
