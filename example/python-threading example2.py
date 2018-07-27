# -*- coding: utf-8 -*-
import threading
import time

def run(n):
    print("task",n)
    time.sleep(2)

res=[]#存线程实例
start_time=time.time()
for i in range(50):#创建线程50个线程
    t=threading.Thread(target=run,args=("t-%s"%i,))
    t.start()
    res.append(t)

for r in res:#循环线程实例列表，等待所有的线程执行完毕
    r.join()#线程执行完毕后，才会往后执行，相当于C语言中的wait()
print("--------all threads has finished...")
print("cost:",time.time()-start_time)#结果是  cost: 2.006114959716797