<h2>贴吧爬虫</h2>

```
背景：零基础小白放假在家闲的没事，想爬取南京信息职业技术学院贴吧用户关注的贴吧因此写来的项目
实现的时间大概是大半天，有部分网页基础，没有系统的学过python！平时了解了一丢丢基本的语法
不足：贴吧有防爬虫机制(应该是发现ip大量的刷新页面需要验证)，因为是小白入门所以没有解决这个问题
      我当时用无线网来爬取信息的,无法使用的时候换了手机的热点(相当于换了ip地址)
```
<h4>实现的思路大致如下:</h4>
<p>1.保存南京信息职业技术学院吧的网址,获得(0,n)页帖子的url(tiezi.py)保存到数据库</p>
<p>2.根据排名第二精品贴分析，获取层主的全部url(user.py)</p>
<p>3.根据个人主页来获取关注的贴吧(user_bar.py)</p>
<p>4.楼中楼通过xhr分析(answer.py)
```
本项目的几个python文件是互相独立的，test文件夹是为了实现思路而写的
demo.py是其他三个独立模块代码的集合
运行方式：
   1.安装python环境并配置环境变量
   2.pip3 install beautifulsoup4
   3.pip3 install lxml
   ...
```

<h4>常见反爬思路:</h4>

```
    1.设置下载等待时间/下载频率
    2.修改User-Agent(user_agent.py为User-Agent池)
        UserAgent 就是用户代理，又叫报头，是一串字符串，相当于浏览器的身份证号。在利用爬虫爬取网站数据时，频繁更换它可以避免触发相应的反爬机制。
        pip install fake-useragent(User-Agent包)也可以使用user_agent.py提供的User-Agent池
    3.设置cookies
    4.分布式爬取
    5.动态IP代理
        解决办法使用动态代理ip:https://github.com/jhao104/proxy_pool(免费的ip池)

```

<h4>问题分析</h4>

```
当无法运行文件的时候打开贴吧，出现安全验证
    1.将url复制到三个不同浏览器无法解决问题（user-agent无法解决）
    2.ip封锁
        手机热点貌似不会禁
```


