""" 在个人主页抓取个人关注的吧 """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import pymysql
import threading 

#数据库建立连接
def db_conn():
    conn = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")
    return conn

#关闭数据库连接
def db_close(conn):
    conn.close()

#获得soup
def getSoup(url):
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    return soup

#获得用户的贴吧
def getBars(url):
    bars = []
    soup = getSoup(url)
    elems = soup.find_all("a",{"target":"_blank","locate":"like_forums#ihome_v1"})
    for elem in elems:
        if(elem!=None):
            bars.append(elem.find("span").string)
    return ",".join(str(bar) for bar in bars)

#获取用户urls
def getUserUrls(begin,end):
    conn = db_conn()
    sql = "select user_url from njcit_user limit %d,%d" %(begin,end)
    cursor = conn.cursor()
    cursor.execute(sql)
    print(sql)
    results = cursor.fetchall()
    db_close(conn)
    return [res[0] for res in results]

def update_user(user_url):
    bars = getBars(user_url) 
    conn = db_conn()
    cursor = conn.cursor()
    sql = "update njcit_user set user_bar = '%s' where user_url = '%s'" %(bars,user_url)
    try:
        print(sql)
        cursor.execute(sql)
        conn.commit() 
    except:
        conn.rollback()
        print("插入失败")
    finally:
        db_close(conn)
    

#开启多线程
def multi_thead(urls):
    threads = []

    for url in urls:
        threads.append(
            threading.Thread(target=update_user,args=(url,))
        )
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

#调用多线程
if __name__ == '__main__':
    for start in range(0,1000,200):
        urls = getUserUrls(9000,97)
        multi_thead(urls)

    




