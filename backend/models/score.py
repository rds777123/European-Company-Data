from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Integer, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="scores")
