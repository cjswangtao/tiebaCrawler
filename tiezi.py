""" 代码和屎一样 """
from bs4 import BeautifulSoup
import json
import pymysql
import threading
import requests

prefix_url = "https://tieba.baidu.com"

#数据库建立连接
def db_conn():
    conn = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")
    return conn

#关闭数据库连接
def db_close(conn):
    conn.close()


def insert(title,url):
    conn = db_conn()
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
    db_close(conn)

def getSoup(url):
        resp = requests.get(url)
        html = resp.content.decode("utf-8")
        soup = BeautifulSoup(html,features="lxml")
        return soup

# #1表示被拦截 0表示没有拦截(之前写的代理拦截用的，没啥用)
# def getIntercept(soup):
#     title_tag = soup.find("title")
#     if title_tag is None:
#         return 0
#     title = title_tag.string
#     if title == "百度安全验证":
#         print("百度安全验证")
#         return 1
#     else:
#         return 0

def insertTiezi(url):
    soup = getSoup(url)
    infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"})
    for info in infos:
        if(info.string!=None and info.string!='0'):
            insert(info.string,prefix_url+info["href"])

#pn翻页的步长为50
def getUrls(begin,end):
    return  [
        "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)
        for pn in range(begin,end,50)
    ]

def multi_thead(urls):
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target = insertTiezi,args = (url,))
        )
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

#多线程 15.936s
if __name__ == '__main__':
    urls = getUrls(0,1200)
    multi_thead(urls)