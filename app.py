from flask import Flask, request, jsonify, redirect, url_for, Blueprint
#from CRUD import crud
from models.post import Posts
from models.comment import Comment
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.register_blueprint(crud)

db.init_app(app)


# Postar
@app.route('/postar', methods=['POST'])
def postar():
    title = request.json.get('title')
    subtitle = request.json.get('subtitle')
    photo = request.json.get('photo')
    db.session.add(Posts(title, subtitle, photo))
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
@app.route('/delete/posts/<int:_id>', methods=['DELETE'])
def deletar_post(_id):
    post = Posts.query.filter_by(id=_id).first()
    if not post:
        return {"message": "Post não encontrado"}, 404  # Evita erro

    # Deleta comentários relacionados
    Comment.query.filter_by(post_id=_id).delete()

    db.session.delete(post)
    db.session.commit()
    return {"message": "Deletado com sucesso!"}, 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
