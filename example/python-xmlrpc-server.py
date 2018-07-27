#helloserver_simple.py

from SimpleXMLRPCServer import SimpleXMLRPCServer

def hello():
    print "hello,world!"
    return "hello client from server!"

svr=SimpleXMLRPCServer(("", 8081), allow_none=True)
svr.register_function(hello)
svr.serve_forever()



#helloserver_thread.py

def hello():
    print "hello,world!"
    return "hello from server"
from SimpleXMLRPCServer import SimpleXMLRPCServer 
from SocketServer import ThreadingMixIn 
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

svr=ThreadXMLRPCServer(("", 8081), allow_none=True)
svr.register_function(hello)
svr.serve_forever()