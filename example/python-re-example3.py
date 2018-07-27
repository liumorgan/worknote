import re
line="shandong province jinan city tel:13305311234"
matchobj = re.match(r'(\w*) province (\w*) city tel:(\d{11})',line,re.M|re.I)
print(matchobj.group())
print(matchobj.group(1))
print(matchobj.group(2))
print(matchobj.group(3))