from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.universities import router as universities_router

app = FastAPI(
    title="Premium Admissions API",
    description="University Admissions Platform",
    version="0.1.0",
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(universities_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "healthy"}