from fastapi import FastAPI

app = FastAPI(
    title="Premium Admissions API",
    description="University Admissions Platform",
    version="0.1.0",
)

@app.get("/health")
async def health():
    return {"status": "healthy"}