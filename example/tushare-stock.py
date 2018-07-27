
import tushare as ts
e = ts.get_hist_data('601318',start='2017-06-23',end='2017-06-26')
print e

ts.get_realtime_quotes(['600848','000980','000981'])

df = ts.get_today_ticks('601333')
df.head(10)
print(df)

df = ts.get_index()
print(df)

ts.get_k_data('600000')