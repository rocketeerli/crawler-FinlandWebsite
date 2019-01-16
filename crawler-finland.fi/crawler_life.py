import requests, re, json, copy
from bs4 import BeautifulSoup
import contentDeal
from requests.packages import urllib3

# 获取页面超链接信息
def get_html(url) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    html = requests.get(url, verify=False, headers=headers)
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    for i in soup.find_all('a', href=re.compile(r"https://finland.fi/life-society/.*")) :
        yield i.get('href')
    for index in range(2, 100) :
        html = requests.get(url + "page/" + str(index), verify=False, headers=headers)
        if not (html is None) :
            html.encoding='utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
            if "Page not found" in soup.title.string :
                break
            for i in soup.find_all('a', href=re.compile(r"https://finland.fi/life-society/.*")) :
                yield i.get('href')
        else :
            break
# 获取超链接页面详细信息
def get_html_link(link_list) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
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
        html_link = requests.get(i, headers=headers, verify=False)
        html_link.encoding='utf-8'
        soup = BeautifulSoup(html_link.text, 'lxml')
        title = soup.title.string
        url = i
        review = ""
        content_div = soup.select(".entry-content")[0]
        content_list = content_div.select("p")
        for k in range(1, 6) :
            appended_string = content_div.select("h" + str(k))
            for ap in appended_string :
                content_list.append(ap)
        content = ""
        for j in content_list :
            content = content + str(j)
        # 处理内容，替换字符串中的字符，去掉正文中的图片信息
        content = contentDeal.deal_content(content)
        # 通过标签名查找 时间 
        time = re.search(r"<meta property=\"article:published_time\" content=\"(.*?)\" />", html_link.text).group(1)
        type = "life"
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
    return dataList
# 保存数据
def save_data(content_list) :
    with open('../finland.fi/life.json', 'a', encoding='utf-8') as f:
        for json_data in content_list :
            f.write(json.dumps(json_data, ensure_ascii=False)+'\n')
            f.flush()
# 函数回调
def fun_call(url) :
    link_list = get_html(url)    # 返回一个生成器
    content_list = get_html_link(link_list)
    save_data(content_list)
# 主函数
def main() :
    # 去除 warning 
    urllib3.disable_warnings()
    url = 'https://finland.fi/category/life-society/'
    fun_call(url)
if __name__=='__main__':
    main()
