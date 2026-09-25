from data import users



# =====================
# Jaccard
# =====================

def compute_jaccard(A,B):

    intersection=[
        x for x in A
        if x in B
    ]

    union=list(set(A+B))


    sim=0

    if len(union)>0:
        sim=len(intersection)/len(union)


    return {
        "intersection":intersection,
        "union":union,
        "sim":sim
    }



# =====================
# 找相似用户
# =====================

def get_similar_users(current_user):


    A=users[current_user]["preferences"]

    results=[]


    for name in users:

        if name==current_user:
            continue


        B=users[name]["preferences"]


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