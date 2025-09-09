from flask_sqlalchemy import SQLAlchemy
from extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.Id'))  # Relaciona com o post

    def __init__(self, text, post_id):
        self.text = text
        self.post_id = post_id

