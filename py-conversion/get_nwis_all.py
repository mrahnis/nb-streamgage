from datetime import date
import pandas as pnd
import matplotlib.pyplot as plt
import matplotlib.dates as dates

import dataretrieval.nwis as nwis


site1 = "015765195"
site2 = "015765185"
site3 = "01576516"

interval = 'daily'  # daily or instantaneous
index_col = 'datetime'
index_str = index_col+'_str'

if interval is 'instantaneous':
    service = 'iv'
else:
    service = 'dv'

start = '2008-10-01'
#start = '2021-11-16'
end = date.today()

""" site 1 """
df1 = nwis.get_record(sites=site1, service=service, start=start, end=end)
df1.reset_index(inplace=True)
df1.rename(columns={'datetime': 'datetime_str'}, inplace=True)

if interval is 'instantaneous':
    df1[index_str] = df1[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:])
    df1[index_col] = pnd.to_datetime(df1[index_str], utc=True)
    df1[index_col] = df1[index_col].dt.tz_convert('EST')
else:
    df1[index_str] = df1[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:19])
    df1[index_col] = pnd.to_datetime(df1[index_str]).map(lambda x: x.tz_localize('EST'))

df1.set_index(df1[index_col], inplace=True)
df1.to_csv('..\\data\\nwis_{}_{}_{}.csv'.format(site1, interval, 'all'))
df1.to_parquet('..\\data\\nwis_{}_{}_{}.parquet'.format(site1, interval, 'all'), index=True)
print('Wrote ..\\data\\nwis_{}_{}_{}.csv'.format(site1, interval, 'all'))


""" site 2 """
df2 = nwis.get_record(sites=site2, service=service, start=start, end=end)
df2.reset_index(inplace=True)
df2.rename(columns={'datetime': 'datetime_str'}, inplace=True)
if interval is 'instantaneous':
    df2[index_str] = df2[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:])
    df2[index_col] = pnd.to_datetime(df2[index_str], utc=True)
    df2[index_col] = df2[index_col].dt.tz_convert('EST')
else:
    df2[index_str] = df2[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:19])
    df2[index_col] = pnd.to_datetime(df2[index_str]).map(lambda x: x.tz_localize('EST'))
df2.set_index(df2[index_col], inplace=True)
df2.to_csv('..\\data\\nwis_{}_{}_{}.csv'.format(site2, interval, 'all'))
df2.to_parquet('..\\data\\nwis_{}_{}_{}.parquet'.format(site2, interval, 'all'), index=True)
print('Wrote ..\\data\\nwis_{}_{}_{}.csv'.format(site2, interval, 'all'))

""" site 3 """
df3 = nwis.get_record(sites=site3, service=service, start=start, end=end)
df3.reset_index(inplace=True)
df3.rename(columns={'datetime': 'datetime_str'}, inplace=True)
if interval is 'instantaneous':
    df3[index_str] = df3[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:])
    df3[index_col] = pnd.to_datetime(df3[index_str], utc=True)
    df3[index_col] = df3[index_col].dt.tz_convert('EST')
else:
    df3[index_str] = df3[index_str].apply(lambda x: str(x)[:10]+' '+str(x)[11:19])
    df3[index_col] = pnd.to_datetime(df3[index_str]).map(lambda x: x.tz_localize('EST'))
df3.set_index(df3[index_col], inplace=True)
df3.to_csv('..\\data\\nwis_{}_{}_{}.csv'.format(site3, interval, 'all'))
df3.to_parquet('..\\data\\nwis_{}_{}_{}.parquet'.format(site3, interval, 'all'), index=True)
print('Wrote ..\\data\\nwis_{}_{}_{}.csv'.format(site3, interval, 'all'))
