>>>import re
>>>pattern = re.compile('\d+')
>>>m = pattern.search('one12twothree34four')  #这里如果使用match方法则不匹配
>>>m
<_sre.SRE_Match object at 0x10cc03ac0>
>>>m.group()
'12'
>>>m = pattern.search('one12twothree34four', 10, 30)   #指定字符串区间  
>>>m
<_sre.SRE_Match object at 0x10cc03b28>
>>>m.group()
'34'
>>>m.span()
(13, 15)
>>> m = pattern.findall('one12twothree34four') 
>>> print m
['12', '34']