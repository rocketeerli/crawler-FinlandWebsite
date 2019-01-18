import re
# 处理字符串文本内容
def deal_review(review) :
    # 去除 p 开头的标签
    review = re.sub(r"<p.*?>", "", review)
    review = re.sub(r"</p.*?>", "", review)
    # 去除 e 开头的标签
    review = re.sub(r"<e.*?>", "", review)
    review = re.sub(r"</e.*?>", "", review)
    # 去除 o 开头的标签
    review = re.sub(r"<o.*?>", "", review)
    review = re.sub(r"</o.*?>", "", review)
    # 去除 注释
    review = re.sub(r"<!--.*-->", "", review, re.S)
    # 去除多余的空格
    review = re.sub(r"\s+", " ", review)
    return review
    