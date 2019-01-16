import re
# 处理字符串文本内容
def deal_content(content) :
    # 将 h 标签 转成 p 标签
    content = re.sub(r"<h\d.*?>", "<p>", content)
    content = re.sub(r"</h\d>", "<p>", content)
    # 将 figcaption 标签转成 p 标签
    content = re.sub(r"figcaption>", "p>", content)
    # 将 p 标签规格化
    content = content.replace("</p>", "<p>")
    content = re.sub(r"<p.*?>", "<p>", content)
    # 将 br 标签变为空格
    content = re.sub(r"<br.*?>", " ", content)
    content = content.replace("</br>", " ")
    # 去除 a 开头的标签
    content = re.sub(r"<a.*?>", "", content)
    content = re.sub(r"</a.*?>", "", content)
    # 去除 b 开头的标签
    content = re.sub(r"<b.*?>", "", content)
    content = re.sub(r"</b.*?>", "", content)
    # 去除 e 开头的标签
    content = re.sub(r"<e.*?>", "", content)
    content = re.sub(r"</e.*?>", "", content)
    # 去除 f 开头的标签
    content = re.sub(r"<f.*?>", "", content)
    content = re.sub(r"</f.*?>", "", content)
    # 去除 i 开头的标签
    content = re.sub(r"<i.*?>", "", content)
    content = re.sub(r"</i.*?>", "", content)
    # 去除 l 开头的标签
    content = re.sub(r"<l.*?>", "", content)
    content = re.sub(r"</l.*?>", "", content)
    # 去除 s 开头的标签
    content = re.sub(r"<s.*?>", "", content)
    content = re.sub(r"</s.*?>", "", content)
    # 去除 t 开头的标签
    content = re.sub(r"<t.*?>", "", content)
    content = re.sub(r"</t.*?>", "", content)
    # 去除 u 开头的标签
    content = re.sub(r"<u.*?>", "", content)
    content = re.sub(r"</u.*?>", "", content)
    # 去除多余的空格
    content = re.sub(r"\s+", " ", content)
    return content
    