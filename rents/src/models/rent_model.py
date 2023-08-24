import uuid
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.extensions import db


class Rents(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.String(120))
    book_id = db.Column(db.String(120))
    rent_from = db.Column(DateTime)
    rent_to = db.Column(DateTime)

