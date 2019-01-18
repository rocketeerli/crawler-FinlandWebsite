# -*- coding: utf-8 -*-
import requests, re, json, copy
from bs4 import BeautifulSoup
import contentDeal
import reviewDeal
from requests.packages import urllib3

# 获取每个版块的超链接信息
def get_html(url) :
    url_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    html = requests.get(url, verify=False, headers=headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    for i in soup.find_all('a', {'class' : "forumtitle"}) :
        url_list.append("https://www.finlandforum.org" + re.search(r".(/.*)", i.get('href')).group(1))
    return url_list
# 获取每个版块内部 每一页的 页面 超链接
def get_page_html(topic_link_list) :
    url_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    for i in topic_link_list :
        html = requests.get(i, verify=False, headers=headers)
        html.encoding='utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        permission = re.search(r"<strong>You do not have the required permissions to view or read topics within this forum.</strong>", html.text)
        if not (permission is None) :
            print("visiting website is dennied")
            continue
        # 找到总页数
        page_total = re.search(r"<strong>(\d+)</strong></span></a>", html.text)
        if page_total is not None :
            page_total = int(page_total.group(1))
        else :
            page_total = 1
        # 遍历第一页
        for j in soup.find_all('a', {'class' : "topictitle"}) :
            url = re.search(r".(/.*)", j.get('href')).group(1).replace("amp;", "")
            url_list.append("https://www.finlandforum.org" + url)
        # 如果页数为 1 ，跳出此次循环
        if page_total == 1 :
            continue
        # 从第二页开始，遍历每一页
        page_url = soup.find_all('a', {'class' : 'button', 'role' : 'button'})[1].get('href')
        page_url = re.search(r".(/.*)", page_url).group(1).replace("amp;", "")
        page_url = page_url[0:-2]
        for j in range(2, page_total+1) :
            url = page_url + str((j - 1) * 50)
            url_list.append("https://www.finlandforum.org" + url)
        return url_list
# 获取每一页的页面超链接内的话题链接
def get_all_html(page_link_list) :
    url_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    html = requests.get(page_link_list, verify=False, headers=headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    for j in soup.find_all('a', {'class' : "topictitle"}) :
        url = re.search(r".(/.*)", j.get('href')).group(1).replace("amp;", "")
        url_list.append("https://www.finlandforum.org" + url)
    return url_list

# 获取超链接页面详细信息
def get_html_link(link_list) :
    # 创建字典
    data = {'title': '', 'url': '','review': '', 'content': '', 'time': '', 'type': ''}
    dataList = []
    url_list = []    # 存储所有访问过的 url， 避免重复访问
    # 遍历所有子链接
    for i in link_list :
        # 判断是否遍历过
        flag = 0
        for url in url_list :
            if url == str(i) :
                flag = 1
                break
        if flag == 1 :
            continue
        url_list.append(i)
        # 正常请求
        html_link = requests.get(i)
        html_link.encoding='utf-8'
        soup = BeautifulSoup(html_link.text, 'lxml')
        # 去除 js 代码
        [s.extract() for s in soup('script')]
        # 去掉结尾的论坛标记
        title = soup.title.string.replace(" - Finland Forum", "")
        url = i
        # 提取 论坛 内容
        content = soup.select(".content")
        if content is None :
            print(i)
            print("内容为空， 跳过此网站")
            continue
        if len(content) == 0 :
            print(str(url) + "\t 此网站无内容 跳过此网站")
            continue
        content = content[0].text
        # 处理内容，替换字符串中的字符，去掉正文中的图片信息
        content = contentDeal.deal_content(content)
        # 提取 论坛 评论
        reviews = soup.select(".content")
        review = ""
        if len(reviews) > 2 :
            for rev in reviews[2:] :
                review = review + "<p>" + reviewDeal.deal_review(rev.text) + "<p>"
        # 通过标签名查找 时间 
        time = ""
        if len(soup.select('.author')) == 0 :
            print(str(url) + "\t此网站时间不可获取")
        else :
            time = soup.select('.author')[0].get_text()[-26:-1]
        type = "forum"
        # 给字典赋值
        data['title'] = title
        data['url'] = url
        data['review'] = review
        data['content'] = content
        data['time'] = time
        data['type'] = type
        # 加入 List
        dataList.append(data)
        # 更改字典地址
        data = copy.copy(data)

        # 检查 话题 页数
        page_total = re.search(r"<strong>(\d+)</strong></span></a>", html_link.text)
        if page_total is not None :
            page_total = int(page_total.group(1))
        else :
            page_total = 1
        # 如果有很多页，继续遍历
        if page_total == 1 :
            continue
        # 获取网页地址
        # 从第二页开始，遍历每一页
        page_url = soup.find_all('a', {'class' : 'button', 'role' : 'button'})[1].get('href')
        page_url = re.search(r".(/.*)", page_url).group(1).replace("amp;", "")
        page_url = page_url[0:-2]
        for j in range(2, page_total+1) :
            url = page_url + str((j - 1) * 15)
            inner_after(dataList, data, "https://www.finlandforum.org" + url)
            # 更改字典地址
            data = copy.copy(data)
    return dataList

# 存储后几页的评论
def inner_after(dataList, data, url) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    html_link = requests.get(url, verify=False, headers=headers)
    html_link.encoding='utf-8'
    soup = BeautifulSoup(html_link.text, 'lxml')
    # 去除 js 代码
    [s.extract() for s in soup('script')]
    # 去掉结尾的论坛标记
    title = soup.title.string.replace(" - Finland Forum", "")
    url = url
    # 提取 论坛 内容  后几页论坛内容为空
    content = ""
    # 提取 论坛 评论
    reviews = soup.select(".content")
    review = ""
    for rev in reviews :
        if re.search(r"<!--.*-->", rev.text, re.S) is not None :
            continue
        review = review + "<p>" + reviewDeal.deal_review(rev.text) + "<p>"
    # 通过标签名查找 时间 
    time = ""
    if len(soup.select('.author')) == 0 :
        print(str(url) + "\t此网站时间不可获取")
    else :
        time = soup.select('.author')[0].get_text()[-26:-1]
    type = "forum"
    # 给字典赋值
    data['title'] = title
    data['url'] = url
    data['review'] = review
    data['content'] = content
    data['time'] = time
    data['type'] = type
    # 加入 List
    dataList.append(data)

# 单独网页存储
def visit_single_html(url) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 创建字典
    data = {'title': '', 'url': '','review': '', 'content': '', 'time': '', 'type': ''}
    dataList = []
    # 正常请求
    html_link = requests.get(url, verify=False, headers=headers)
    html_link.encoding='utf-8'
    soup = BeautifulSoup(html_link.text, 'lxml')
    # 去除 js 代码
    [s.extract() for s in soup('script')]
    # 去掉结尾的论坛标记
    title = soup.title.string.replace(" - Finland Forum", "")
    # 提取 论坛 内容
    content = soup.select(".content")
    if content is None :
        print(url)
        print("内容为空， 跳过此网站")
        return dataList
    if len(content) == 0 :
        print(str(url) + "\t 此网站无内容")
        return dataList
    content = content[0].text
    # 处理内容，替换字符串中的字符，去掉正文中的图片信息
    content = contentDeal.deal_content(content)
    # 提取 论坛 评论
    reviews = soup.select(".content")
    review = ""
    if len(reviews) > 2 :
        for rev in reviews[2:] :
            review = review + "<p>" + reviewDeal.deal_review(rev.text) + "<p>"
    # 通过标签名查找 时间 
    time = ""
    if len(soup.select('.author')) == 0 :
        print(str(url) + "\t此网站时间不可获取")
    else :
        time = soup.select('.author')[0].get_text()[-26:-1]
    type = "forum"
    # 给字典赋值
    data['title'] = title
    data['url'] = url
    data['review'] = review
    data['content'] = content
    data['time'] = time
    data['type'] = type
    # 加入 List
    dataList.append(data)
    # 更改字典地址
    data = copy.copy(data)

    # 检查 话题 页数
    page_total = re.search(r"<strong>(\d+)</strong></span></a>", html_link.text)
    if page_total is not None :
        page_total = int(page_total.group(1))
    else :
        page_total = 1
    # 如果有很多页，继续遍历
    if page_total == 1 :
        return dataList
    # 获取网页地址
    # 从第二页开始，遍历每一页
    page_url = soup.find_all('a', {'class' : 'button', 'role' : 'button'})[1].get('href')
    page_url = re.search(r".(/.*)", page_url).group(1).replace("amp;", "")
    page_url = page_url[0:-2]
    for j in range(2, page_total+1) :
        url = page_url + str((j - 1) * 15)
        inner_after(dataList, data, "https://www.finlandforum.org" + url)
        # 更改字典地址
        data = copy.copy(data)
    return dataList

# 保存数据
def save_data(content_list) :
    with open('../www.finlandforum.org/forum.json', 'a', encoding='utf-8') as f:
        for json_data in content_list :
            f.write(json.dumps(json_data, ensure_ascii=False)+'\n')
            f.flush()
# 函数回调
def fun_call(url, page_link_list) :
    if "viewtopic" in page_link_list :
        content_list = visit_single_html(page_link_list)
        save_data(content_list)
    else :
        link_list = get_all_html(page_link_list)
        content_list = get_html_link(link_list)
        save_data(content_list)
# 主函数
def main() :
    # 去除 warning 
    urllib3.disable_warnings()
    url = 'https://www.finlandforum.org/'
    topic_link_list = get_html(url)
    page_link_list = get_page_html(topic_link_list)
    for link in page_link_list :
        print(link)
        fun_call(url, link)
if __name__=='__main__':
    main()
