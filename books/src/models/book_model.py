import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Books(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_name = db.Column(db.String(120), unique=True)
    added_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    number_of_books = db.Column(db.Integer)

