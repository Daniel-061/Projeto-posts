from flask import Blueprint, request
from extensions import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

login = Blueprint('login', __name__, url_prefix='/login')
db.init_app(login)


@login.route('/login', methods=['POST'])
def login():
    username = request.json.get['username']
    password = request.json.get['password']
    if username == 'admin' and password == '':
        create_access_token(identity=username)

