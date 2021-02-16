""" 爬楼不包含楼中楼(楼主用户信息)"""
from bs4 import BeautifulSoup
import urllib.request
import re
import json
from urllib.parse import quote
import string

result={}
#4796371684帖子的url
layer_url = "https://tieba.baidu.com/p/4796371684"
#个人主页的通用url
one_base_url = "https://tieba.baidu.com/home/main?un="

#获得该帖子的总页数和第一页层主的username
html = urlopen(layer_url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
page = soup.find_all("span",{"class":"red","style":""}) #获取贴吧红色的数字
pns = int(page[0].string)
users = soup.find_all("img",{"username":re.compile("^[\u4e00-\u9fa5_a-zA-Z0-9]+$"),"class":""})
for user in users:
    if(user["username"] not in result):
        result[user["username"]] = [1]
    else:
        result[user["username"]][0] = result[user["username"]][0] + 1

#获得该帖子的其他页层主的username
for i in range(2,pns+1):
    layer_url = "https://tieba.baidu.com/p/4796371684?pn="+str(i)
    html = urlopen(layer_url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    users = soup.find_all("img",{"username":re.compile("^[\u4e00-\u9fa5_a-zA-Z0-9]+$"),"class":""})
    for user in users:
        if(user["username"] not in result):
            result[user["username"]] = [1]
        else:
            result[user["username"]][0] = result[user["username"]][0] + 1


#注意浏览器中文是gbk所以需要转换编码
one_base_url = "https://tieba.baidu.com/home/main?un="
for key in result:
    one_url = one_base_url + quote(key, safe = string.printable)
    result[key].append(one_url)
print(result)

#将result写如user.json
fo = open("user.json", "w")
fo.write(json.dumps(result,ensure_ascii=False))
fo.close()

    

