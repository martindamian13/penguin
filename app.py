from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
# Database

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Debug mode activado
if __name__ == '__main__':
    app.run(debug=True)