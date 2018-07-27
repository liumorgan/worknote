#coding:gbk

import re
pattern = re.compile('\d+')
m = pattern.search('one12twothree34four') 
m.group()

m = pattern.findall('one12twothree34four') 
print m

pattern = re.compile(r'\d+')

result1 = pattern.finditer('hello 123456 789')
result2 = pattern.finditer('one1two2three3four4', 0, 10)
print(result1)
print(result2)
print('result1....')
for m1 in result1:
    print("matching string:{} position:{}".format(m1.group(), m1.span()))

print('result2....')
for m2 in result2:
    print("matching string:{} position:{}".format(m2.group(), m2.span()))
	
p = re.compile(r'[\s\,;]+')
print(p.split('a,b;;c   d'))

p = re.compile(r'(\w+) (\w+)')  #\w=[A-Za-z0-9]
s = 'hello 123, hello 456'

print(p.sub(r'hello world', s))   #使用'hello world'替换'hello 123'和'hello 456'
print(p.sub(r'\2 \1', s))

def func(m):
    return 'hi' + ' ' + m.group(2)

print(p.sub(func, s))
print(p.sub(func, s, 1))
	