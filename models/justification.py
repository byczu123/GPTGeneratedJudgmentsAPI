import uuid
from app import db


class Justification(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    text = db.Column(db.Text)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
