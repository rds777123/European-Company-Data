from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Score, User
from backend.schemas import ScoreCreate, ScoreOut, LeaderboardEntry, APIResponse

router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("/{user_id}", response_model=APIResponse[ScoreOut])
def submit_score(user_id: int, payload: ScoreCreate, db: Session = Depends(get_db)):
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    score = Score(user_id=user_id, value=payload.value)
    db.add(score)
    db.commit()
    db.refresh(score)
    return APIResponse(data=ScoreOut.model_validate(score))


@router.get("/leaderboard", response_model=APIResponse[list[LeaderboardEntry]])
def leaderboard(db: Session = Depends(get_db)):
    rows = (
        db.query(User.username, func.max(Score.value).label("best_score"))
        .join(Score, Score.user_id == User.id)
        .group_by(User.id)
        .order_by(func.max(Score.value).desc())
        .limit(10)
        .all()
    )
    entries = [
        LeaderboardEntry(rank=i + 1, username=row.username, best_score=row.best_score)
        for i, row in enumerate(rows)
    ]
    return APIResponse(data=entries)


@router.get("/{user_id}", response_model=APIResponse[list[ScoreOut]])
def get_user_scores(user_id: int, db: Session = Depends(get_db)):
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    scores = db.query(Score).filter(Score.user_id == user_id).order_by(Score.recorded_at.desc()).all()
    return APIResponse(data=[ScoreOut.model_validate(s) for s in scores])
