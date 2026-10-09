from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .database import Base
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(20), default="student")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
class Exam(Base):
    __tablename__="exams"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    title: Mapped[str]=mapped_column(String(180))
    subject: Mapped[str]=mapped_column(String(100))
    description: Mapped[str]=mapped_column(Text, default="")
    duration_minutes: Mapped[int]=mapped_column(Integer, default=15)
    is_published: Mapped[bool]=mapped_column(Boolean, default=True)
    questions: Mapped[list["Question"]]=relationship(back_populates="exam", cascade="all, delete-orphan")
class Question(Base):
    __tablename__="questions"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    exam_id: Mapped[int]=mapped_column(ForeignKey("exams.id"))
    prompt: Mapped[str]=mapped_column(Text)
    option_a: Mapped[str]=mapped_column(Text)
    option_b: Mapped[str]=mapped_column(Text)
    option_c: Mapped[str]=mapped_column(Text)
    option_d: Mapped[str]=mapped_column(Text)
    correct_option: Mapped[str]=mapped_column(String(1))
    points: Mapped[int]=mapped_column(Integer, default=1)
    exam: Mapped["Exam"]=relationship(back_populates="questions")
class Attempt(Base):
    __tablename__="attempts"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    exam_id: Mapped[int]=mapped_column(ForeignKey("exams.id"))
    started_at: Mapped[datetime]=mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    submitted_at: Mapped[datetime|None]=mapped_column(DateTime, nullable=True)
    status: Mapped[str]=mapped_column(String(20), default="in_progress")
    score: Mapped[int]=mapped_column(Integer, default=0)
    total_points: Mapped[int]=mapped_column(Integer, default=0)
    answers_json: Mapped[str]=mapped_column(Text, default="{}")
    exam: Mapped["Exam"]=relationship()
    user: Mapped["User"]=relationship()
