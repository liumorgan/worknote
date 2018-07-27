#!/usr/bin/python

from string import atoi
from time import sleep
from sys import *

from cmspcli import *

if __name__ == "__main__":
	ip="10.110.13.101"
	port=1201
	user="imqAdmin"
	passwd="pw2017@GL!"
	topic=""
	cloud=0
	
	cl = CmspCli()
	cl.connectcmsp(ip,port,user,passwd,topic,cloud)
	topiclist=cl.getalltopic()
	for topic in topiclist:
		print  topic
	
	cl.opentopic("t1")
	infolist = cl.gettopicinfo("t1")
	for line in infolist:
		print line
	print cl.getqueuefilename("t2")	
	print "t2 count = ", cl.getmsgcount("t2")
	cl.putmq("aaaaaaaaaaaaaa")
	print "t2 count = ", cl.getmsgcount("t2")
	
	result=cl.getmq()
	print result[2]

	grpMsg = POINTER(c_ubyte)()
	for i in range(10):
		cl.putmsgtogroup("1111111",grpMsg)
	cl.putmqgroup(grpMsg)
	print "t1 count = ", cl.getmsgcount("t1")

	grpresult=cl.getmqgroup()
	while True:
		(ret,nsize,msg)=cl.getmsgfromgroup(grpresult)
		if ret == 0:
			print msg
		else:
			break
			
	cl.closecmsp()
