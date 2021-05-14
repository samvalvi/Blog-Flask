from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Meli8462@127.0.0.1/blog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now, nullable=False)
    texto = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"Post('{self.titulo}', '{self.fecha}', '{self.texto}')"


@app.route('/')
def inicio():
    posts = Post.query.order_by(Post.fecha.desc()).all()
    return render_template('index.html', values=posts)


@app.route("/crear")
def crear_post():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def add_post():
    titulo = request.form.get("titulo")
    texto = request.form.get("texto")

    if titulo and texto:
        post = Post(titulo=titulo, texto=texto)
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("add.html", error="Todos los campos son requeridos")


@app.route('/eliminar', methods=['POST'])
def eliminar_post():
    post_id = request.form.get("eliminar")
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
