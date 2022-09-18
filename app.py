from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world(): # what
    return 'Hello, World!' #ag