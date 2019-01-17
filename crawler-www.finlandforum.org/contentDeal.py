import re
# 处理字符串文本内容
def deal_content(content) :
    # 去除多余的空格
    content = re.sub(r"\s+", " ", content)
    return content
    