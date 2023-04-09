import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/game', methods=['GET'])
def index():
    with open("index_game.html", encoding="UTF-8") as index:
        response = index.read()
    return response

@app.route('/asset/<string:path>', methods=['GET'])
def asset(path):
    with open(os.path.join("asset", path), encoding="UTF-8") as asset:
        response = asset.read()
    return response

@app.route('/pic/<string:path>', methods=['GET'])
def pic(path):
    with open(os.path.join("asset", path), mode="rb") as pic:
        response = pic.read()
    return response

if __name__ == '__main__':
    app.run(debug=True)