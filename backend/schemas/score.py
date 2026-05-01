from pydantic import BaseModel
from datetime import datetime


class ScoreCreate(BaseModel):
    value: int


class ScoreOut(BaseModel):
    id: int
    user_id: int
    value: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    best_score: int
