from lxml import etree
import re
tree = etree.parse("xpath_test2.xml")
find = etree.XPath('/bookstore/book[@category="WEB"]/title')
for book in find(tree):
	print(book.text)
	
for tt in  tree.xpath('//book[@category="WEB"]/title/text()'):
	print(tt)

regexpNS = "http://exslt.org/regular-expressions"
find = etree.XPath("//*[re:test(., '^XML$', 'i')]",namespaces={'re':regexpNS})	
for book in find(tree):
	print(book.text)


	