#! /usr/bin/env python

import logging
from flask import Flask, render_template, request, jsonify
from model import db


app = Flask(__name__)

words_db = db.TrieDb()

logger = logging.getLogger(__name__)

if app.debug:
    logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    searchbox = request.form.get("text")
    logger.debug(f"Livesearch incoming: {livesearch}")
    result = words_db.get(searchbox)
    logger.debug(f"Livesearch outgoing: {result}")
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
