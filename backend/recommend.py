from data import users



# =====================
# Jaccard
# =====================

def compute_jaccard(A, B):

    set_A=set(A)
    set_B=set(B)

    intersection=set_A & set_B

    union=set_A | set_B


    sim=0

    if len(union)>0:
        sim=len(intersection)/len(union)


    return {
        "intersection":list(intersection),
        "union":list(union),
        "sim":sim
    }


# =====================
# 找相似用户
# =====================

def get_similar_users(current_user):

# 用户不存在处理
    if current_user not in users:
        return []


    A = users[current_user].get(
        "preferences",
        []
    )

    results=[]

    for name in users:

        if name==current_user:
            continue


        B = users[name].get("preferences",[])


        score=compute_jaccard(A,B)


        results.append({

            "user":name,
            "preferences":B,
            "intersection":score["intersection"],
            "union":score["union"],
            "sim":score["sim"]

        })


    results.sort(
        key=lambda x:x["sim"],
        reverse=True
    )


    return results[:3]



# =====================
# 商品推荐
# =====================

def recommend(username):


    # 当前用户喜欢
    current_pref = users[username]["preferences"]
    # 🌟 边界情况处理：冷启动（用户没有任何偏好）
    if not current_pref:
        return {
            "user": username,
            "similar_users": [],  # 没有相似用户
            "recommendations": ["手机", "耳机", "笔记本", "充电宝"], # 降级：直接推荐全局热门商品
            "is_cold_start": True # 标记：告诉前端这是冷启动状态
        }


    # 找相似用户
    similar_users=get_similar_users(username)


    recommend_items=[]


    for user in similar_users:


        for item in user["preferences"]:


            # 相似用户喜欢
            # 当前用户没有

            if item not in current_pref:

                if item not in recommend_items:

                    recommend_items.append(item)



    return {

        "user":username,

        "similar_users":similar_users,

        "recommendations":recommend_items

    }