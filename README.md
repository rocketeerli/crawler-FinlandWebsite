# 介绍

本项目是我开始学习 Python 爬虫时写的，代码功能就是爬取网站内容，并转成 json 格式存储到文件中，架构比较简单。

爬取的是芬兰的一些网站，主要利用的是 get() 方法，下面是一些网址。除了 [芬兰](https://finland.fi/) 外，其他的网站都是静态的。这里我并没有全部爬取，只选取2、3、4、6，四个网站进行爬取。

# 芬兰网站

## 1.今日芬兰： http://finlandtoday.fi/

## 2.芬兰日常： http://www.dailyfinland.fi/

## 3.赫尔辛基时间： http://www.helsinkitimes.fi/

## 4.芬兰： https://finland.fi/

## 5.芬兰时间：http://www.finlandtimes.fi/

## 6.芬兰论坛：https://www.finlandforum.org/

## 7.网址：http://www.designforum.fi/

# 爬取结果的 json 格式

主要有 6 个属性，分别是 标题、链接、评论、内容、时间和类型。

其中一个爬取结果的例子如下：

{
    "title":"I'm finish 9 month's",
    "url":"https://www.finlandforum.org/viewtopic.php?f=2&t=97699&sid=c5d80bd59f5ef4d33805d96bad9c3d6f",
    "review":"<p>The resolution is coming soon<p><p>I hope today I finish 9 months<p>",
    "content":"Hi guys I waiting for nine months for family ties. I have had an interview at the embassy in Morocco and I'm still waiting a response ",
    "time":" Fri Dec 07, 2018 3:41 pm",
    "type":"forum"
}