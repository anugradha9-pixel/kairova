from sqlalchemy import Column, Integer, String, Float
from backend.db.models import Base


class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    platform = Column(String, nullable=False)

    followers = Column(Integer, nullable=False)

    engagement_rate = Column(Float, nullable=False)

    niche = Column(String, nullable=False)

    estimated_price = Column(Float, nullable=True)