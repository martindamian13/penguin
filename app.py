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
    cur = db.execute('SELECT * FROM artesanos')
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
            apellido = request.form['apellido']
            ciudad = request.form['ciudad']
            nacimiento = request.form['nacimiento']
            #sexo = request.form['sexo']
            t_artesanal = request.form.getlist('t_artesanal')
            t_artesanal = ', '.join(t_artesanal)
            modalidad = request.form.getlist('modalidad')
            modalidad = ', '.join(modalidad)
            print (modalidad)
            mat_prima = request.form.getlist('mat_prima')
            mat_prima = ', '.join(mat_prima)
            oficio = request.form['oficio']
            antiguedad =request.form['antiguedad']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO artesanos (nombre, apellido, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) VALUES (?,?,?,?,?,?,?,?,?)",(nombre, apellido, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return render_template("result.html",msg = msg)

# @app.route('/editar', methods=['POST', 'GET'])
# def editar():   
#     if request.method == 'POST':
#         try:
#             nombre = request.args.get['nombre']
#             apellido = data['apellido']
#             ciudad = data['ciudad']
#             nacimiento = data['nacimiento']
#             #sexo = request.form['sexo']
#             t_artesanal = request.form.getlist('t_artesanal')
#             t_artesanal = ', '.join(t_artesanal)
#             modalidad = request.form.getlist('modalidad')
#             modalidad = ', '.join(modalidad)
#             print (modalidad)
#             mat_prima = request.form.getlist('mat_prima')
#             mat_prima = ', '.join(mat_prima)
#             oficio = data['oficio']
#             antiguedad =request.form['antiguedad']
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO artesanos (nombre, apellido, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) VALUES (?,?,?,?,?,?,?,?,?)",(nombre, apellido, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) )
#                 con.commit()
#                 msg = "Record successfully added"
#         except:
#             con.rollback()
#             msg = "error in insert operation"
#         finally:
#             con.close()
#             return render_template("result.html",msg = msg)

if __name__ == "__main__":
    app.run(debug=True)
