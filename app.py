from http.client import REQUEST_ENTITY_TOO_LARGE
from wsgiref.handlers import read_environ
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250))
    done = db.Column(db.Boolean)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create-registro', methods=['POST'])
def create():
    task = Task(content=request.form['content'], done=False)
    db.session.add(task)
    db.session.commit()
    return 'saved'


if __name__ == '__main__':
    app.run(debug=True)
