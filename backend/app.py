from flask import Flask, jsonify
from flask_cors import CORS

from recommend import recommend


app = Flask(__name__)

CORS(app)

app.json.ensure_ascii = False


@app.route("/")
def index():

    return jsonify({
        "message":"推荐系统后端运行正常"
    })


@app.route("/recommend/<username>")
def get_recommend(username):

    result = recommend(username)

    return jsonify(result)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )