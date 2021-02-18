import redis   # 导入redis 模块
import pymysql
""" 玩转redis """
conn = pymysql.connect(host="localhost",user="root",passwd="root",db="tieba")
#连接池连接redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rs = redis.Redis(connection_pool=pool)

def data_convert():
    cursor = conn.cursor()
    sql = "select url from njcit_tiezi"
    cursor.execute(sql)
    results = cursor.fetchall()
    for res in results: 
        rs.sadd("tiezi_url",res[0])


def clear():
    rs.delete("tiezi_url")

data_convert()
# r.set('name', 'runoob')  # 设置 name 对应的值
# print(r['name'])
# print(r.get('name'))  # 取出键 name 对应的值
# print(type(r.get('name')))  # 查看类型
conn.close()
rs.close()