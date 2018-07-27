#!/usr/bin/python
# -*- coding: GBK -*-

import threading
import time
 
exitFlag = 0
 
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        self.print_time(self.name, self.counter)
        print "Exiting " + self.name
		
    def print_time(self,threadName, counter):
        while counter:
			time.sleep(1)
			print "%s: %s" % (threadName, time.ctime(time.time()))
			counter -= 1

threads=[]
for i in range(3): 
    t = myThread(1, "Thread-%d"%i, 20)
    threads.append(t)
    t.setDaemon(True)
    t.start()

for i in range(len(threads)):
    threads[i].join()


print "Exiting Main Thread"