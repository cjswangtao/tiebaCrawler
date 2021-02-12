from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import json
from urllib.parse import quote
import  string
""" 整合了三个部分功能的完整版爬虫 """

result = {} #贯穿全文的dict
pn = 0
#贴吧url前缀
prefix_url = "https://tieba.baidu.com"
#个人主页的通用url
one_base_url = "https://tieba.baidu.com/home/main?un="
#南京信息职业技术学院吧第一页的url
base_url = "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)

#打开南京信息职业技术学院吧的主页,获取该也全部帖子的url
html = urlopen(base_url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"})
for info in infos:
    if(info.string!=None and info.string!='0'):
        layer_url = prefix_url+info["href"]

        #依次打开第一页帖子的全部url
        html = urlopen(layer_url).read().decode('utf-8')
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
            html = urlopen(layer_url).read().decode('utf-8')
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
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    bars = soup.find_all("a",{"target":"_blank","locate":"like_forums#ihome_v1"})
    for bar in bars:
        if(bar!=None):
            result[key].append(bar.find("span").string)
            print(key+"\t"+bar.find("span").string)

print(result)

#将result中的数据保存到user.json中
fo = open("demo.json","w")
s = json.dumps(result)
fo.write(s)
fo.close()