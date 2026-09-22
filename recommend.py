def jaccard(A, B):
    """
    计算两个用户偏好集合的Jaccard相似度
    """
    A=set(A)
    B=set(B)

    intersection = A & B   # 交集

    union = A | B          # 并集


    if len(union) == 0:
        return 0


    return len(intersection) / len(union)



def get_top_users(current_user, users):

    """
    计算当前用户和其他用户的相似度
    """

    result = []


    for user in users:

        score = jaccard(
            current_user,
            user["items"]
        )


        result.append(
            {
                "name": user["name"],
                "score": score,
                "items": list(user["items"])
            }
        )


    # 按相似度从大到小排序
    result.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return result[:3]



def get_recommend_products(current_user, similar_users):

    """
    推荐：
    相似用户有，但是当前用户没有的商品
    """

    recommendations = []

    current_user = set(current_user)
    for user in similar_users:

        products =set(user["items"]) - current_user


        for p in products:

            recommendations.append(
                {
                    "product":p,
                    "reason":user["name"]+"也喜欢"
                }
            )


    return recommendations