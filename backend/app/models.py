from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
import datetime


def _utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True)
    email           = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role            = Column(String)
    orgName         = Column(String)


class Hazard(Base):
    __tablename__ = "hazards"

    id                 = Column(Integer, primary_key=True, index=True)
    road_name          = Column(String)
    lat                = Column(Float)
    lng                = Column(Float)
    cls                = Column(String)
    severity           = Column(String)
    status             = Column(String, default="open")
    sla_hours          = Column(Integer)
    reported           = Column(String, default=_utc_now_iso)
    contractor         = Column(String,  nullable=True)
    completion_percent = Column(Integer, default=0)
    description        = Column(String,  nullable=True)
    tx_hash            = Column(String,  nullable=True, default=None)   # blockchain PoR


# ── Chat session tracking (Stage 2) ───────────────────────────────────────────

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id             = Column(String,  primary_key=True)      # UUID string
    created_at     = Column(String,  default=_utc_now_iso)
    last_active    = Column(String,  default=_utc_now_iso)
    intent_summary = Column(String,  nullable=True)         # last detected intent


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(String,  index=True)                # → chat_sessions.id
    role       = Column(String)                             # "user" or "assistant"
    content    = Column(String)
    intent     = Column(String,  nullable=True)             # set on user turns only
    sources    = Column(String,  nullable=True)             # JSON-encoded list
    created_at = Column(String,  default=_utc_now_iso)


# ── Citizen feedback loop (Stage 3) ───────────────────────────────────────────

class ChatFeedback(Base):
    __tablename__ = "chat_feedback"

    id            = Column(Integer, primary_key=True, index=True)
    session_id    = Column(String,  index=True)
    message_index = Column(Integer, default=0)   # which turn in the session
    rating        = Column(String)               # "thumbs_up" or "thumbs_down"
    comment       = Column(String,  nullable=True)
    created_at    = Column(String,  default=_utc_now_iso)