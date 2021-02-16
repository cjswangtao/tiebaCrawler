import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="root",db="tieba")
cursor = db.cursor()
# sql = "insert into njcit_tiezi values('1','2')"

def insert(title,url):
    cursor = db.cursor()
    sql = "insert into njcit_tiezi values('%s','%s')" %(title,url)
    print(sql)
    cursor.execute(sql)
    db.commit()

def select(url):
    sql = "select * from njcit_tiezi where url= '%s'" %(url)
    cursor.execute(sql)
    print(cursor.rowcount)

# insert('ddd','ads')
# insert('ccc','bder')
select("aaa")
# print()
db.close()
