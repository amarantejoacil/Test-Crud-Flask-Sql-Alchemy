import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        book = Book(titulo=request.form.get('titulo'))
        db.session.add(book)
        db.session.commit()
    books = Book.query.all()
    return render_template('home.html', books=books)


class Book(db.Model):
    titulo = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Titulo: {}>".format(self.titulo)

if __name__ =="__main__":
    app.run(debug=True)