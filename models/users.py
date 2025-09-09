from flask_sqlalchemy import SQLAlchemy
from extensions import db

class Posts(db.Model):
    id = db.Column('Id', db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = password
