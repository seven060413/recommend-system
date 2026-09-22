from flask import Flask, jsonify
from flask_cors import CORS

from data import users

from recommend import (
    get_top_users,
    get_recommend_products
)


app = Flask(__name__)

# 允许前端跨域访问
CORS(app)


# 中文正常显示
app.json.ensure_ascii = False


@app.route("/recommend")
def recommend():

    # 当前用户张三的兴趣
    current_user = [
        "手机",
        "耳机",
        "充电宝"
    ]


    # 找相似用户
    top_users = get_top_users(
        current_user,
        users
    )


    # 推荐商品
    products = get_recommend_products(
        current_user,
        top_users
    )


    return jsonify({

        "similarUsers": top_users,

        "recommendProducts": products

    })


# 测试接口
@app.route("/")
def index():

    return jsonify({
        "message": "推荐系统后端运行正常"
    })



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )