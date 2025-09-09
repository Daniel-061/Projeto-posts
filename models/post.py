from flask_sqlalchemy import SQLAlchemy
from extensions import db

class Posts(db.Model):
    id = db.Column('Id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    photo = db.Column(db.String(255))

    def __init__(self, title, subtitle, photo):
        self.title = title
        self.subtitle = subtitle
        self.photo = photo

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "photo": self.photo
        }
