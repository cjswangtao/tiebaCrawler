""" 在个人主页抓取个人关注的吧 """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random


url = "https://tieba.baidu.com/home/main?un=%E4%B8%BF%E4%B8%A8%E6%83%85%E4%B9%A6"
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
elems = soup.find_all("a",{"target":"_blank","locate":"like_forums#ihome_v1"})
for elem in elems:
    if(elem!=None):
        print(elem.find("span").string)

