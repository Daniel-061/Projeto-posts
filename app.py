from flask import Flask, request, jsonify, redirect, url_for, Blueprint
from CRUD import crud
#FAZER O JWT
from models.post import Posts
from models.comment import Comment
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(crud)
db.init_app(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
