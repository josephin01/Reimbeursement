from config import db
from datetime import datetime, timezone


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    deleted_at = db.Column(db.DateTime, default=None)

    def delete(self):
        self.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
