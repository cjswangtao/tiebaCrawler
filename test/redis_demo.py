from redis import Redis   # 导入redis 模块

r = Redis(host='localhost', port=6379,db=0,password="root")  
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型