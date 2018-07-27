# -*- coding: utf-8 -*-
import xlrd
xlsfile = r'e:\test1.xls' 
book = xlrd.open_workbook(xlsfile)
sheet0 = book.sheet_by_index(0)
print "1 -",sheet0
sheet_name = book.sheet_names()[0]
print "2 -",sheet_name
sheet1 = book.sheet_by_name(sheet_name)
nrows = sheet0.nrows 
ncols = sheet0.ncols    #获取列总数
print "3 -",nrows
print "4 -",ncols

#循环打印每一行的内容
for i in range(nrows):
	for j in range(ncols):
		cell_value = sheet0.cell_value(i,j)
		print cell_value,"\t",
	print