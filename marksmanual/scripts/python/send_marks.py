from flask import Flask, request
from flask_cors import CORS

from markserver import MarkServer

mark_server = MarkServer()

# to run in terminal:
# FLASK_APP=send_marks.py flask run

app = Flask(__name__)
CORS(app)

@app.route("/mark", methods=["GET", "POST"])
def mark():
    data = request.form["mark"]
    print(data)
    if data:
        mark_server.data_transfer(data)
    else:
        print("No data")
    return data
