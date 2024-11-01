from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router)

app.title = "NFL API"

@app.get("/")
async def root():
    return {"Welcome to the NFL API"}
