# -*- coding: utf-8 -*-
import xlsxwriter
workbook = xlsxwriter.Workbook('chart_data_table.xlsx') #可以生成.xls文件但是会报错
worksheet = workbook.add_worksheet('Sheet1') #工作页
#准备测试数据
bold = workbook.add_format({'bold': 1})
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
  [2, 3, 4, 5, 6, 7],
  [10, 40, 50, 20, 10, 50],
  [30, 60, 70, 50, 40, 30],
]
#插入数据
worksheet.write_row('A1', headings, bold)#行插入操作 注意这里的'A1'
worksheet.write_column('A2', data[0])#列插入操作 注意这里的'A2'
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])
#插入直方图1
chart1 = workbook.add_chart({'type': 'column'})#选择 直方图 'column'
chart1.add_series({
  'name':    '=Sheet1!$B$1',
  'categories': '=Sheet1!$A$2:$A$7',#X轴值（实在不知道怎么叫，就用XY轴表示）
  'values':   '=Sheet1!$B$2:$B$7',#Y轴值
  'data_labels': {'value': True}#显示数字，就是直方图上面的数字，默认不显示
})
#注意上面写法 '=Sheet1!$B$2:$B$7' Sheet1是指定工作页， $A$2:$A$7是从A2到A7数据，熟悉excel朋友应该一眼就能认得出来
#插入直方图2
chart1.add_series({
  'name':    ['Sheet1', 0, 2],
  'categories': ['Sheet1', 1, 0, 6, 0],
  'values':   ['Sheet1', 1, 2, 6, 2],
  'data_labels': {'value': True}
})
chart1.set_title({'name': 'Chart with Data Table'}) #直方图标题
chart1.set_x_axis({'name': 'Test number'}) #X轴描述
chart1.set_y_axis({'name': 'Sample length (mm)'})#有轴描述
chart1.set_table()
chart1.set_style(3)#直方图类型
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) #直方图插入到 D2位置
workbook.close()