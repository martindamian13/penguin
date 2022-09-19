from flask import Flask, render_template, request, redirect, url_for,g
import sqlite3


app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('database.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.route('/')
def hello_world():
    db = get_db()
    cur = db.execute('SELECT * FROM ejemplo')
    datas = cur.fetchall()
    return render_template('index.html', datas=datas)    

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/agregar', methods=['POST', 'GET'])
def agregar():   
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            edad = request.form['edad']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ejemplo (nombre, edad) VALUES (?,?)",(nombre,edad) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html",msg = msg)