from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routers import users, scores

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flappy Bird Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(scores.router)


@app.get("/health")
def health():
    return {"data": "ok", "error": None}
