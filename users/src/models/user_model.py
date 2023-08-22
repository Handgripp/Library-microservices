import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180))
    created_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    role = db.Column(Enum('guest', 'admin', name='users_role'))

