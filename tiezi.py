from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")
""" 获取https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn=0页面的所有帖子名称和url """
prefix_url = "https://tieba.baidu.com"
#南京信息职业技术学院第一页
#爬取10页的帖子名称和网址

#将数据插入数据库
def insert(title,url):
    cursor = db.cursor()
    select_sql = "select * from njcit_tiezi where url='%s'" %(url)
    insert_sql = "insert into njcit_tiezi values('%s','%s')" %(title,url)
    cursor.execute(select_sql)
    if cursor.rowcount==0: #什么都没查到
        cursor.execute(insert_sql)
        db.commit() 
        print(insert_sql)


for pn in range(0,500):
    base_url = "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)
    html = urlopen(base_url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"})
    for info in infos:
        if(info.string!=None and info.string!='0'):
            insert(info.string,prefix_url+info["href"])


db.close()


        
