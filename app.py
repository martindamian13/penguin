from flask import Flask, render_template, request, redirect, url_for, g 
import sqlite3

app = Flask(__name__)

# Connect to the database
def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row
    return sql

# Get the database
def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

# Close the database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    db = get_db()
    cur = db.execute('SELECT * FROM artesanos')
    datas = cur.fetchall()
    return render_template('view.html', datas=datas)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/agregar', methods=['POST', 'GET'])
def agregar():   
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            cedula = request.form['cedula_numero']
            depa = request.form['departamento']
            edad = request.form['edad']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO artesanos (nombre,apellido,cedula_numero,departamento,edad) VALUES (?,?,?,?,?)",(nombre,apellido,cedula,depa,edad) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html",msg = msg)
            
