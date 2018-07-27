#pip install pyDNS
import DNS
query = "dns"
url='www.baidu.com'
DNS.DiscoverNameServers()
reqobj = DNS.Request(url)
answerobj = reqobj.req(name = query, qtype = DNS.Type.A)
for item in answerobj.answers:
	ip = ("%s") % (item['data']) 
	print ip