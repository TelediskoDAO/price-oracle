from time import time
from flask import Flask
import os

INFO_LOG = os.environ["INFO_LOG"]

app = Flask(__name__)

@app.route("/")
def check():
    with open(INFO_LOG, "r") as logs:
        last_update = int(logs.read().split("\n")[-1].split("\t")[0])
        if time() > last_update + 60 * 12:
            return "error", 500
        else:
            return "ok"