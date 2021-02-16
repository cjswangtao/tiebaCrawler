""" 整合了三个部分功能的完整版爬虫，爬用户关注的吧(不包含楼中楼) """
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import re
import json
from urllib.parse import quote
import  string
import requests

#构建请求头,伪装浏览器
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
}

result = {} #贯穿全文的dict
pn = 0
#贴吧url前缀
prefix_url = "https://tieba.baidu.com"
#个人主页的通用url
one_base_url = "https://tieba.baidu.com/home/main?un="

#打开南京信息职业技术学院吧的主页,获取该也全部帖子的url,20页帖子的url
#修改
for pn in range(0,1):
    #南京信息职业技术学院吧第n页的url
    base_url = "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)
    agent_url = Request(url=base_url,headers=headers)
    html = urlopen(agent_url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"}) #获取第一页所以所有帖子的名称和id
    for info in infos:
        if(info.string!=None and info.string!='0'):
            layer_url = prefix_url+info["href"]
            #依次打开每页帖子的url
            #修改
            agent_url = Request(layer_url,headers=headers)
            html = urlopen(agent_url).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')
            page = soup.find_all("span",{"class":"red","style":""}) #获该帖子的页数
            pns = int(page[0].string)
            #获取帖子第一页全部层主的id,将数据存入result中
            users = soup.find_all("img",{"username":re.compile("^[\u4e00-\u9fa5_a-zA-Z0-9]+$"),"class":""})
            for user in users:
                print(user["username"])
                if(user["username"] not in result):
                    result[user["username"]] = [1]
                else:
                    result[user["username"]][0] = result[user["username"]][0] + 1
            #获该帖子取其它页层主的id,将数据存入result中
            for i in range(2,pns+1):
                layer_url = layer_url+"?pn="+str(i)
                agent_url = Request(layer_url,headers=headers)
                html = urlopen(agent_url).read().decode('utf-8')
                soup = BeautifulSoup(html, features='lxml')
                users = soup.find_all("img",{"username":re.compile("^[\u4e00-\u9fa5_a-zA-Z0-9]+$"),"class":""})
                for user in users:
                    print(user["username"])
                    if(user["username"] not in result):
                        result[user["username"]] = [1]
                    else:
                        result[user["username"]][0] = result[user["username"]][0] + 1

#2.生成用户主页对应的url
for key in result:
    home_url = one_base_url + quote(key, safe = string.printable) #百度: python url中出现汉子的处理方式
    result[key].append(home_url)
print(result)

#3.根据用户主页对应的url抓取该用户关注的全部贴吧
for key in result:
    url = result[key][1]
    agent_url = Request(url,headers=headers)
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    bars = soup.find_all("a",{"target":"_blank","locate":"like_forums#ihome_v1"})
    for bar in bars:
        if(bar!=None):
            result[key].append(bar.find("span").string)
            print(key+"\t"+bar.find("span").string)

print(result)

#将result中的数据保存到user.json中
fo = open("demo01.json","w",encoding="utf-8")
s = json.dumps(result,ensure_ascii=False)
fo.write(s)
fo.close()
