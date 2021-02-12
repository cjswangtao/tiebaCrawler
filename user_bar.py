""" 在个人主页抓取个人关注的吧 """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

url = "https://tieba.baidu.com/home/main?un=%E4%B8%BF%E4%B8%A8%E6%83%85%E4%B9%A6"
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
#<a data-fid="763965" target="_blank" locate="like_forums#ihome_v1" href="/f?kw=%E6%88%B4%E5%8D%97%E9%AB%98%E7%BA%A7%E4%B8%AD%E5%AD%A6&amp;fr=home" title="戴南高级中学" class="u-f-item unsign"><span>戴南高级中学</span><span class="forum_level lv4"></span></a>
#<a data-fid="537361" target="_blank" locate="like_forums#ihome_v1" href="/f?kw=%E5%8D%97%E4%BA%AC%E4%BF%A1%E6%81%AF%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&amp;fr=home" title="南京信息职业技术学院" class="u-f-item unsign"><span>南京信息职业技术...</span><span class="forum_level lv5"></span></a>
#<a data-fid="59099" target="_blank" locate="like_forums#ihome_v1" href="/f?kw=%E6%9D%8E%E6%AF%85&amp;fr=home" class="u-f-item unsign"><span>李毅</span><span class="forum_level lv3"></span></a>
elems = soup.find_all("a",{"target":"_blank","locate":"like_forums#ihome_v1"})
for elem in elems:
    if(elem!=None):
        print(elem.find("span").string)

