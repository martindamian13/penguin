from flask import Flask, render_template, request, redirect, url_for,g
import sqlite3


app = Flask(__name__)
# Coneccion a la base de datos
def connect_db():
    sql = sqlite3.connect('database.db')
    sql.row_factory = sqlite3.Row
    return sql

# Funcion para obtener la base de datos
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Funcion para cerrar la base de datos
@app.teardown_appcontext
def close_db(error): 
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Ruta principal
@app.route('/home')
def home():
    return render_template('index.html')

# Ruta de login
@app.route('/')
def login():
    return render_template('login.html') 

# Ruta de estadisticas
@app.route('/estadisticas')
def estadisticas():
    return render_template('stadistics1.html')

# Ruta para ver los datos de la base de datos
@app.route('/view')
def view():
    db = get_db()
    cur = db.execute('SELECT * from artesanos')
    artesanos = cur.fetchall()
    return render_template('view.html', artesanos=artesanos)

# Ruta para agregar datos a la base de datos
@app.route('/form')
def form():
    return render_template('form.html')

# Funcion que agrega los datos a la base de datos
@app.route('/agregar', methods=['POST', 'GET'])
def agregar():   
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            ciudad = request.form['ciudad']
            nacimiento = request.form['nacimiento']
            sexo = request.form['sexo']
            t_artesanal = request.form.getlist('t_artesanal')
            t_artesanal = ', '.join(t_artesanal)
            modalidad = request.form.getlist('modalidad')
            modalidad = ', '.join(modalidad)    
            mat_prima = request.form.getlist('mat_prima')
            mat_prima = ', '.join(mat_prima)
            oficio = request.form['oficio']
            antiguedad =request.form['antiguedad']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO artesanos (nombre, apellido, sexo, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) VALUES (?,?,?,?,?,?,?,?,?,?)",(nombre, apellido,sexo, ciudad, nacimiento, t_artesanal, modalidad, mat_prima, oficio, antiguedad) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            con.close()
            return redirect("home")

# Debug mode on
if __name__ == "__main__":
    app.run(debug=True)