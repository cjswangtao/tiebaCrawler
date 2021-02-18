""" 爬一个帖子的用户信息用户url存入数据库(含楼中楼)"""
from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import re
import json
from urllib.parse import quote
import string
import pymysql
import multiprocessing as mp
#
# #
#数据库建立连接
conn = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")


#个人主页的通用url
one_base_url = "https://tieba.baidu.com/home/main?un="
base_url = "https://tieba.baidu.com/"
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
}

#解析url为soup
def getSoup(url):
    agent_url = Request(url=url,headers=headers)
    html = urlopen(agent_url).read().decode("utf-8")
    soup = BeautifulSoup(html,features="lxml")
    return soup

#获得url楼中楼使用
def getUrl(tid,pid,pn):
    return "https://tieba.baidu.com/p/comment?tid="+tid+"&pid="+pid+"&pn="+str(pn)

#将数据插入数据库
def insert(user_name,user_url,tiezi_url):
    cursor = conn.cursor()
    select_sql = "select * from njcit_user where user_name='%s'" %(user_name)
    insert_sql = "insert into njcit_user values('%s','%s','%s')" %(user_name,user_url,tiezi_url)
    cursor.execute(select_sql)
    if cursor.rowcount==0: #什么都没查到
        try:
            cursor.execute(insert_sql)
            conn.commit() 
            print(insert_sql)
        except:
            print("插入失败")
            conn.rollback()

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
    sql = "select url from njcit_tiezi limit %d,%d" %(begin,end)
    cursor = conn.cursor()
    cursor.execute(sql)
    print(sql)
    results = cursor.fetchall()
    return [res[0] for res in results]

# 开启进程池 11.042
if __name__ == '__main__':
    pool = mp.Pool(4)
    for i in range(0,30):
        #0-4 4-8 8-12 12-16
        #0   1   2    3     -> i*4
        pool.map(insertUsers,getTieziUrls(i*4,4))
        mp.Lock()
# conn.close() 

