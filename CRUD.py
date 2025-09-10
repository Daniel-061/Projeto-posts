from flask import request, redirect, url_for, jsonify, Blueprint
from app import app
from extensions import db
from models.post import Posts
from models.comment import Comment

crud = Blueprint('crud', __name__, url_prefix='')

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
@app.route('/posts/<int:_id>')
def detalhes(_id):
    post = Posts.query.get(id)
    comments = Comment.query.filter_by(post_id=id).all()
    return jsonify({
        "post": post.to_dict(),
        "comments": [{"id": c.id, "text": c.text} for c in comments]
    })


# Deletar um post
@app.route('/delete/posts/<int:_id>')
def deletar(_id):
    decision = input(bool(f'Você tem certeza que deseja deletar {Posts.query.get(id)}'))
    if decision:
        db.session.delete(Posts.query.filter_by(id=id).first())
        db.session.delete(Comment.query.filter_by(Post_id=id).all())
        db.session.commit()
        return '<p> deletado com sucesso! </p>'
    else:
        return '<p> ação cancelada com sucesso!</p>', redirect(url_for('/posts'))
