import threading as td
import time

def T1():
    print("T1 start")
    time.sleep(0.5)
    print("T1 finish")
def T2():
    print("T2 start")
    # time.sleep(10)
    time.sleep(0.1)
    print("T2 finish")

t1 = td.Thread(target=T1,args=())

t2 = td.Thread(target=T2,args=())

t1.start()
t1.join()
t2.start()
t2.join()
print("end")