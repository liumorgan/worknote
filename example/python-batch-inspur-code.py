# -*- coding: utf-8 -*-

import urllib
import urlparse
import json

def get_code(self_url):	
	url_tuple = urlparse.urlparse(self_url)
	strparam=url_tuple.query
	dicparam={};
	for param in strparam.split('&'):
		kv = param.split('=')
		dicparam[kv[0]] = kv[1]
	#print (dicparam)

	code_url=r'http://10.6.6.9//a/ajax.php?'
	dicparam['tradecode']='get_guest_netcode'
	paramlist=['tradecode','user_name','device_id','roleid']
	for param in paramlist:
		code_url=code_url + param + "=" + dicparam[param] + "&"
	code_url=code_url[:-1]
	#print(code_url)
	response = urllib.urlopen(code_url)
	result=response.readline()
	#print(result)
	strjson= result[result.index('=') + 1: ]
	js=json.loads(strjson)
	code = js['Code']
	return code
	

self_url=r'http://10.6.6.9//a/roleguestcode.html?user_name=bGl1cmc:&device_id=595865&roleid=1&local_lguage_set=zh'
for i in range(2):
	print (get_code(self_url))