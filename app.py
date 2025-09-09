from flask import Flask, request, jsonify, redirect, url_for, Blueprint
from models.post import Posts
from models.comment import Comment
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bp = Blueprint('posts', __name__, url_prefix='/posts')

db.init_app(app)


# Postar
@app.route('/postar', methods=['POST'])
def postar():
    titulo = request.json.get('titulo')
    subtitulo = request.json.get('subtitulo')
    foto = request.json.get('foto')
    db.session.add(Posts(titulo, subtitulo, foto))
    db.session.commit()
    return {"message": "Post criado com sucesso!"}, 201

# Comentar
@app.route('/comment', methods=['POST', 'GET'])
def comment():
    post_id = request.json.get('post_id')
    text = request.json.get('text')
    db.session.add(Comment(text, post_id))
    db.session.commit()
    return {"message": "Comment criado com sucesso!"}, 201

# Ver todos os posts
@app.route('/posts')
def listar():
    posts = Posts.query.all()
    return jsonify([p.to_dict() for p in posts])

# Ver um post e seus comentários
@app.route('/posts/<int:id>')
def detalhe(id):
    post = Posts.query.get(id)
    comments = Comment.query.filter_by(post_id=id).all()
    return jsonify({
        "post": post.to_dict(),
        "comments": [{"id": c.id, "text": c.text} for c in comments]
    })

# Deletar um post
@app.route('/delete/posts/<int:id>')
def deletar(id):
    Decision = input(bool(f'Você tem certeza que deseja deletar {Posts.query.get(id)}'))
    if Decision:
        db.session.delete(Posts.query.filter_by(id=id).first())
        db.session.delete(Comment.query.filter_by(Post_id=id).all())
        db.session.commit()
    else:
        return '<p> ação cancelada com sucesso!</p>', redirect(url_for('/posts'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
