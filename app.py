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
    cur = db.execute('SELECT * FROM database')
    datas = cur.fetchall()
    return render_template('index.html', datas=datas)    

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/agregar', methods=['POST', 'GET'])
def agregar():   
    if request.method == 'POST':
        try:
            nombre = request.formartesanos['nombre']
            apellido = request.formartesanos['apellido']
            cuidad = request.formartesanos['cuidad']
            nacimiento = request.formartesanos['nacimiento']
            sexo = request.formartesanos['sexo']
            t_artesanal = request.formartesanos['t_artesanal']
            modalidad = request.formartesanos['modalidad']
            mat_prima = request.formartesanos['mat_prima']
            oficio = request.formartesanos['oficio']
            antiguedad =request.formartesanos['antiguedad']


            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ejemplo (nombre, apellido, cuidad, nacimiento, sexo, t_artesanal, modalidad, mat_prima, oficio, antiguedad ) VALUES (?,?,?,?,?,?,?,?,?,?)",(nombre, apellido, cuidad, nacimiento, sexo, t_artesanal, modalidad, mat_prima, oficio, antiguedad) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html",msg = msg)