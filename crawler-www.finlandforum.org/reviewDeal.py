import re
# 处理字符串文本内容
def deal_review(review) :
    # 去除 注释
    review = re.sub(r"<!--.*-->", "", review, re.S)
    # 去除多余的空格
    review = re.sub(r"\s+", " ", review)
    return review
    