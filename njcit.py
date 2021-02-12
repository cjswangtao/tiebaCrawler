from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

""" 获取https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn=0页面的所有帖子名称和url """
pn = 0
prefix_url = "https://tieba.baidu.com"
base_url = "https://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&ie=utf-8&pn="+str(pn)
html = urlopen(base_url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
infos = soup.find_all("a",{"target":"_blank","rel":"noreferrer","class":"j_th_tit"})
for info in infos:
    if(info.string!=None and info.string!='0'):
        print(info.string+"\t"+"url:"+prefix_url+info["href"])

        
