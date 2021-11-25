from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produto_banco.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Parent(Base):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = db.Column(Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parent = db.relationship("Parent", back_populates="children")




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)