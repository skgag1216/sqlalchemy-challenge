from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"