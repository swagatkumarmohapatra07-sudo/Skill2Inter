"""SQLAlchemy ORM model for Skill taxonomy."""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    normalized_name = Column(String(200), index=True)   # lowercase, no spaces
    category = Column(String(100))      # programming / ml / web / cloud / database / devops / soft
    description = Column(Text)
    aliases = Column(Text)              # comma-separated alternate names: "ML, machine-learning"
    related_skills = Column(Text)       # comma-separated related skill names
