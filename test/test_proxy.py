from bs4 import BeautifulSoup
import json
import pymysql
import multiprocessing as mp
import requests
from user_agent import Agent

prefix_url = "https://tieba.baidu.com"
conn = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")

""" 构建代理 """
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

""" 构建请求头 """
def getHeader():
    header = {}
    agent_header = Agent()
    value = agent_header.get_user_agent()
    header['User-Agent'] = value
    header["Connection"] = "keep-alive"
    header["Accept"] = "text/html, */*; q=0.01"
    header["Accept-Encoding"] = "gzip, deflate, sdch"
    header["Accept-Language"] = "zh-CN,zh;q=0.8,ja;q=0.6"
    return header

def insert(title,url):
    cursor = conn.cursor()
    select_sql = "select * from njcit_tiezi where url='%s'" %(url)
    insert_sql = "insert into njcit_tiezi values('%s','%s')" %(title,url)
    cursor.execute(select_sql)
    if cursor.rowcount==0: #什么都没查到
        try:
            cursor.execute(insert_sql)
            conn.commit() 
            print(insert_sql)
        except:
            print("插入失败")
            conn.rollback()

#使用代理
def useProxy(url):
    proxy = get_proxy().get("proxy")
    header = getHeader()
    resp = requests.get(url, headers=header ,proxies={"http": "http://{}".format(proxy)},)
    html = resp.content.decode("utf-8")
    soup = BeautifulSoup(html,features="lxml")
    #代理没有被拦截
    if resp.status_code == 200 and getIntercept(soup) == 0:
        print("使用了代理IP: "+proxy+"  代理请求头: "+str(header))
        return resp
    else:
        if resp.status_code == 200:
            print("代理被拦截了")
            exit()
        else:
            print("代理IP状态码:"+resp.status_code)
        delete_proxy(proxy)
        useProxy(url)

def getSoup(url):
    header = getHeader()
    html = requests.get(url=url,headers=header).content.decode("utf-8")
    soup = BeautifulSoup(html,features="lxml")
    if getIntercept(soup):
        #被拦截了使用代理
        resp = useProxy(url)
        html = resp.content.decode("utf-8")
        soup = BeautifulSoup(html,features="lxml")
        return soup
    else:
        return soup

#1表示被拦截 0表示没有拦截
def getIntercept(soup):
    title_tag = soup.find("title")
    if title_tag is None:
        return 0
    title = title_tag.string
    if title == "百度安全验证":
        print("百度安全验证")
        return 1
    else:
        return 0

def insertTiezi(url):
    soup = getSoup(url)
    infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"})
    for info in infos:
        if(info.string!=None and info.string!='0'):
            insert(info.string,prefix_url+info["href"])

def getUrls(begin,end):
    return  [
        "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)
        for pn in range(begin,end)
    ]

#2000-3600 end4000 
if __name__ == '__main__':
    urls = getUrls(4200,5000)
    pool = mp.Pool(4)
    pool.map(insertTiezi,urls)