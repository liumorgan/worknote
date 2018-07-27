# -*- coding: utf-8 -*-
#导入xlwt模块
import xlwt
import datetime
book = xlwt.Workbook(encoding='utf-8')

sheet = book.add_sheet('test', cell_overwrite_ok=True)

sheet.write(0, 0, label = 'Row 0, Column 0 Value')
#设置格式写入：
font = xlwt.Font() # 字体
font.name = 'Times New Roman'
font.bold = True
font.underline = True
font.italic = True
style = xlwt.XFStyle() # 创建一个格式
style.font = font # 设置格式字体
sheet.write(2, 2, 'Formatted value',style)

#写入日期：
style = xlwt.XFStyle()
style.num_format_str = 'M/D/YY' # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
sheet.write(0, 0, datetime.datetime.now(), style)
#写入公式：
sheet.write(0, 0, 5) # Outputs 5
sheet.write(0, 1, 2) # Outputs 2
sheet.write(1, 0, xlwt.Formula('A1*B1')) # 输出 "10" (A1[5] * A2[2])
sheet.write(1, 1, xlwt.Formula('SUM(A1,B1)')) # 输出 "7" (A1[5] + A2[2])
#写入链接：
sheet.write(2, 3, xlwt.Formula('HYPERLINK("http://www.google.com";"Google")')) #输出 "Google"链接到http://www.google.com 
 

book.save(r'e:\test2.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错