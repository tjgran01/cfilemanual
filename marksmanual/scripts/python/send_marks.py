import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/mark", methods=["GET"])
def mark():
    with open("./this.txt", "w") as out_file:
       out_file.write('Hello')

    return "Nothing to see here..."
