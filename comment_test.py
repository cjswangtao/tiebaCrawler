""" 爬取楼中楼(测试模块) """
#测试通过成功爬取4796371684帖子第一页的全部楼中楼评论
# 

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re
import json
from urllib.parse import quote
import  string
import requests

#4796371684帖子的url
tiezi_url = "https://tieba.baidu.com/p/4796371684"
# 伪装浏览器的请求头
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
}


#解析url为soup
def getSoup(url):
    agent_url = Request(url=url,headers=headers)
    html = urlopen(agent_url).read().decode("utf-8")
    soup = BeautifulSoup(html,features="lxml")
    return soup

#获得url
def getUrl(pid,pn):
    return "https://tieba.baidu.com/p/comment?tid=4796371684&pid="+pid+"&pn="+str(pn)


#根据xhr分析网络通信 获得基础的url组合,在网页源码搜索清洗
soup = getSoup(tiezi_url)
elems = soup.find_all("div",{"class":"l_post j_l_post l_post_bright"})

#获得该页的全部pid
for elem in elems:
    pid = elem["data-pid"]
    print(pid)
    #获得最后一页的数字pns
    url = getUrl(pid,1)
    soup = getSoup(url)
    a_pages = soup.find_all("a",{"href":re.compile("#[0-9]")})
    if len(a_pages) == 0:
        pns = 2
    else:
        for a_page in a_pages:
            if a_page.string == "尾页":
                pns = int(a_page["href"].replace("#","")) + 1

    # 获得楼中楼中所有的评论:
    for pn in range(1,pns):
        soup = getSoup(getUrl(pid,pn))
        span_tages = soup.find_all("span",{"class":"lzl_content_main"})
        for span_tage in span_tages:
            ans = re.sub(r'<\/?.+?\/?>',"",str(span_tage)) #清洗所有的标签
            print(ans)
    # 功能需求测试用
    # for pn in range(1,pns):
    #     soup = getSoup(getUrl(pid,pn))
    #     tags = soup.findAll("a",{"rel":"noopener","class":"j_user_card lzl_p_p"})
    #     for tag in tags:
    #         username = tag["username"]
    #         one_url = tag["href"]
    #         print(username+"\t"+one_url)



