from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world(): # what_ever
    return 'Hello, World!' #ag