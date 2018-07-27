from xmlrpclib import ServerProxy
svr=ServerProxy("http://10.110.13.186:8081")
print svr.hello()