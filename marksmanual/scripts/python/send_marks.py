import sys
from flask import Flask, request
from flask_cors import CORS

from markserver import MarkServer

try:
    mark_server = MarkServer()
except:
    print("Unable to make a connection to marking device.")
    print("Shutting the whole program down, you hear!")
    sys.exit()

app = Flask(__name__)
CORS(app)

@app.route("/mark", methods=["GET", "POST"])
def mark():
    data = request.form["mark"]
    print(data)
    if data:
        mark_server.data_transfer(data)
    else:
        print("No data found in POST")
    return data
