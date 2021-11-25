from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aluno_banco.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, index=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    # curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


class Curso(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, index=True)
    descricao = db.Column(db.String(150))
    # alunos = db.relationship('Aluno', backref='curso_id')

    def __init__(self, descricao):
        self.descricao = descricao


@app.route('/')
def consultar_aluno():
    alunos = Aluno.query.all()
    cursos = Curso.query.all()
    return render_template('listar-aluno.html',alunos=alunos, cursos=cursos )


@app.route('/adicionar_curso', methods=['GET', 'POST'])
def adicionar_curso():
    if request.method == 'POST':
        curso = Curso(request.form['descricao'])
        db.session.add(curso)
        db.session.commit()
        return redirect('/')
    return render_template('adicionar_curso.html')


@app.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        aluno = Aluno(request.form['nome'], request.form['idade'])
        db.session.add(aluno)
        db.session.commit()
        return redirect('/')
    return render_template('adicionar_aluno.html')


@app.route('/editar_aluno/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.query.get(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.idade = request.form['idade']
        db.session.commit()
        return redirect('/')
    return render_template('editar_aluno.html', aluno=aluno)


@app.route('/excluir_aluno/<int:id>')
def excluir_aluno(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)