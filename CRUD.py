from flask import request, redirect, url_for, jsonify, Blueprint
from extensions import db
from models.post import Posts
from models.comment import Comment

crud = Blueprint('crud', __name__, url_prefix='')

# Postar
@crud.route('/post', methods=['POST'])
def postar():
    data = request.get_json()
    title = data['title']
    subtitle = data['subtitle']
    photo = data['photo']

    if not title or not subtitle:
        return jsonify({"erro": "Todos os campos (Título e Subtítulo) são obrigatórios"}), 400

    db.session.add(Posts(title, subtitle, photo))
    db.session.commit()
    return {"message": "Post criado com sucesso!"}, 201

# Comentar
@crud.route('/comment', methods=['POST'])
def comment():
    data = request.get_json()
    post_id = data.get('post_id')
    text = data.get('text')
    db.session.add(Comment(text, post_id))
    db.session.commit()
    return {"message": "Comment criado com sucesso!"}, 201


# Ver todos os posts
@crud.route('/posts')
def listar():
    posts = Posts.query.all()
    return jsonify([p.to_dict() for p in posts])


# Ver um post e seus comentários
@crud.route('/posts/<int:id>')
def detalhe(id):
    post = Posts.query.get(id)
    comments = Comment.query.filter_by(post_id=id).all()
    return jsonify({
        "post": post.to_dict(),
        "comments": [{"id": c.id, "text": c.text} for c in comments]
    })


# Deletar um post e comentários
@crud.route('/delete/posts/<int:_id>', methods=['DELETE'])
def deletar_post(_id):
    post = Posts.query.filter_by(id=_id).first()
    if not post:
        return {"message": "Post não encontrado"}, 404  # Evita erro

    # Deleta comentários relacionados
    Comment.query.filter_by(post_id=_id).delete()

    db.session.delete(post)
    db.session.commit()
    return {"message": "Deletado com sucesso!"}, 200


# Deletar um comentário
@crud.route('/delete/comments/<int:_id>', methods=['DELETE'])
def deletar_comentario(_id):
    comment = Comment.query.filter_by(post_id=_id).first()

    if not comment:
        return '<p> Nenhum comentário encontrado nesse post </p>', 400

    Comment.query.filter_by(post_id=_id).delete()
    db.session.delete(comment)
    db.session.commit()
    return {"message": "Deletado com sucesso!"}, 200


# ATUALIZAR POSTS
@crud.route('/editar/posts/<int:_id>', methods=['PUT'])
def editar_post(_id):
    post = Posts.query.filter_by(id=_id).first()  # corrigido: id
    if not post:
        return jsonify({"erro": "Nenhum post encontrado"}), 404

    data = request.get_json()

    # Pega os campos enviados no JSON (não são obrigatórios todos)
    title = data.get('title')
    subtitle = data.get('subtitle')
    photo = data.get('photo')

    # Atualiza apenas os campos enviados
    if title is not None:
        post.title = title
    if subtitle is not None:
        post.subtitle = subtitle
    if photo is not None:
        post.photo = photo

# ATUALIZAR COMENTÁRIO
@crud.route('/editar/comentarios/<int:_id>', methods=['PUT'])
def editar_comentario(_id):
    comentario = Comment.query.filter_by(id=_id).first()
    if not comentario:
        return jsonify({"erro": "Comentário não encontrado"}), 404

    data = request.get_json()
    novo_texto = data.get("text")

    if not novo_texto or novo_texto.strip() == "":
        return jsonify({"erro": "O campo 'text' não pode estar vazio"}), 400

    comentario.text = novo_texto.strip()
    db.session.commit()

    return jsonify({"msg": "Comentário atualizado com sucesso!"}), 200
