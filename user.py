""" 多线程爬取用户的数据"""
from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.parse import quote
import string
import pymysql
import threading 
#
# #
#数据库建立连接
def db_conn():
    conn = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")
    return conn

#关闭数据库连接
def db_close(conn):
    conn.close()

#个人主页的通用url
one_base_url = "https://tieba.baidu.com/home/main?un="
base_url = "https://tieba.baidu.com/"


def getSoup(url):
    html = requests.get(url).content.decode("utf-8")
    soup = BeautifulSoup(html,features="lxml")
    return soup

#获得url楼中楼使用
def getUrl(tid,pid,pn):
    return "https://tieba.baidu.com/p/comment?tid="+tid+"&pid="+pid+"&pn="+str(pn)

#将数据插入数据库
def insert(user_name,user_url,tiezi_url):
    conn = db_conn()
    cursor = conn.cursor()
    select_sql = "select * from njcit_user where user_name='%s'" %(user_name)
    insert_sql = "insert into njcit_user values('%s','%s','%s','')" %(user_name,user_url,tiezi_url)
    cursor.execute(select_sql)
    if cursor.rowcount==0: #什么都没查到
        try:
            print(insert_sql)
            cursor.execute(insert_sql)
            conn.commit() 
        except:
            print("插入失败")
            conn.rollback()
        finally:
            db_close(conn)

#将帖子的信息插入数据库层
def insertUsers(tiezi_url):
    tid = tiezi_url.replace("https://tieba.baidu.com/p/","")
    soup = getSoup(tiezi_url)
    pages = soup.find_all("span",{"class":"red","style":""}) #获取贴吧红色的数字
    #判空
    if len(pages) == 0:
        total_pages = 2
    else:
        total_pages = int(pages[0].string) + 1
    for i in range(1,total_pages):
        users = soup.find_all("img",{"username":re.compile("^[\u4e00-\u9fa5_a-zA-Z0-9]+$"),"class":""})
        for user in users:
            user_name = user["username"]
            user_url = one_base_url + quote(user_name, safe = string.printable)
            insert(user_name,user_url,tiezi_url)
        #插入楼中楼的数据
        elems = soup.find_all("div",{"class":"l_post j_l_post l_post_bright"})
        #获得该页的全部pid
        for elem in elems:
            pid = elem["data-pid"]
            #获得楼中楼最后一页的数字pns
            url = getUrl(tid,pid,1)
            soup = getSoup(url)
            a_pages = soup.find_all("a",{"href":re.compile("#[0-9]")})
            if len(a_pages) == 0:
                pns = 2
            else:
                for a_page in a_pages:
                    if a_page.string == "尾页":
                        pns = int(a_page["href"].replace("#","")) + 1
                         
            #爬楼中楼
            for pn in range(1,pns):
                soup = getSoup(getUrl(tid,pid,pn))
                tags = soup.findAll("a",{"rel":"noopener","class":"j_user_card lzl_p_p"})
                for tag in tags:
                    user_name = tag["username"]
                    one_url = tag["href"]
                    user_url = base_url + one_url
                    insert(user_name,user_url,tiezi_url)


def getTieziUrls(begin,end):
    conn = db_conn()
    sql = "select url from njcit_tiezi limit %d,%d" %(begin,end)
    cursor = conn.cursor()
    cursor.execute(sql)
    print(sql)
    results = cursor.fetchall()
    db_close(conn)
    return [res[0] for res in results]

#开启多线程
def multi_thead(urls):
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target=insertUsers,args=(url,))
        )
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    

if __name__ == '__main__': 
    for start in range(0,1000,200):
        urls = getTieziUrls(start,200)
        multi_thead(urls)
# conn.close() 
