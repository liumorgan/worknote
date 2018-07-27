from lxml import etree
root = etree.parse("bookstore.xml")
find = etree.XPath('//book')
allbook=find(root)
print(dir(allbook[0]))
for book in allbook:
	print(book.find('title').text)
	
for book in allbook:
	print(book.xpath('title/@lang'))	
	
find = etree.XPath('/bookstore/book')
allbook=find(root)
for book in allbook:
	print(book.find('title').text)	
	
find = etree.XPath('//@lang')
alllang=find(root)
for lang in alllang:
	print(lang)		
	
find = etree.XPath('/bookstore/book[1]')
print(find(root)[0].find('title').text)
print(find(root)[0].find('title').attrib['lang'])	

find = etree.XPath('/bookstore/book[last()]')
print(find(root)[0].find('title').text)
print(find(root)[0].find('title').attrib['lang'])	

find = etree.XPath('//title[@lang=\'eng\']')
alltitle=find(root)
for title in alltitle:
	print(title.text)
	
find = etree.XPath('/bookstore/book[price>35.00]/title')
alltitle=find(root)
for title in alltitle:
	print(title.text)			