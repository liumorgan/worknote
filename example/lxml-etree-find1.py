from lxml import etree
root = etree.parse("xpath_test.xml")
find = etree.XPath('/bookstore/book[price>35.00]/title')
print(find(root)[0].text)