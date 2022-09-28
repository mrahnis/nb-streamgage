import pandas as pnd
import matplotlib.pyplot as plt


site1 = "015765195"
site2 = "015765185"
site3 = "01576516"

file3 = "Daily Mean Water Temperature at Site 01576516 20121001_20130411.csv"
file2 = "Daily Mean Water Temperature at Site 015765185 20121028_20130411.csv"
file1 = "Daily Mean Water Temperature at Site 015765195 20081008_20121115.csv"

# file1_instant = "Instantaneous Water Temperature at Site 01576516 20130412_20160413.csv"

interval = 'daily'
col_names = ['datetime_str', '00010_Mean', 'hist_mean', 'hist_median', 'diff_hist_mean', 'diff_hist_median', 'comment']

temps1 = pnd.read_csv(
    '..\\data-download\\temperature\\{}'.format(file1),
    header=0,
    names=col_names,
    parse_dates=False
)
temps2 = pnd.read_csv(
    '..\\data-download\\temperature\\{}'.format(file2),
    header=0,
    names=col_names,
    parse_dates=False
)
temps3 = pnd.read_csv(
    '..\\data-download\\temperature\\{}'.format(file3),
    header=0,
    names=col_names,
    parse_dates=False
)

"""
temps = pnd.read_csv(
    '.\\temperature\\{}'.format(file1_instant),
    index_col="Date Time (UTC -5:00)",
    parse_dates=True
)
"""

# add the site_no column
temps1['site_no'] = int(site1)
temps2['site_no'] = int(site2)
temps3['site_no'] = int(site3)

# fix number problems
temps1['00010_Mean'] = pnd.to_numeric(temps1['00010_Mean'], errors='coerce')
temps2['00010_Mean'] = pnd.to_numeric(temps2['00010_Mean'], errors='coerce')
temps3['00010_Mean'] = pnd.to_numeric(temps3['00010_Mean'], errors='coerce')

# localize to set the missing timezone
index_col = 'datetime'
temps1[index_col] = pnd.to_datetime(temps1['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
temps2[index_col] = pnd.to_datetime(temps2['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
temps3[index_col] = pnd.to_datetime(temps3['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))

print(temps1.head())
print(temps1.dtypes)

# reset the index to datetime column
temps1.reset_index(drop=True, inplace=True)
temps2.reset_index(drop=True, inplace=True)
temps3.reset_index(drop=True, inplace=True)

temps1.set_index(index_col, inplace=True)
temps2.set_index(index_col, inplace=True)
temps3.set_index(index_col, inplace=True)

# drop the old date column
temps1.drop('datetime_str', axis=1, inplace=True)
temps2.drop('datetime_str', axis=1, inplace=True)
temps3.drop('datetime_str', axis=1, inplace=True)

# write out the new files
temps1.to_csv('.\\output\\lang_{}_{}_{}.csv'.format(site1, interval, 'temp'))
temps1.to_parquet('.\\output\\lang_{}_{}_{}.parquet'.format(site1, interval, 'temp'), index=True)

temps2.to_csv('.\\output\\lang_{}_{}_{}.csv'.format(site2, interval, 'temp'))
temps2.to_parquet('.\\output\\lang_{}_{}_{}.parquet'.format(site2, interval, 'temp'), index=True)

temps3.to_csv('.\\output\\lang_{}_{}_{}.csv'.format(site3, interval, 'temp'))
temps3.to_parquet('.\\output\\lang_{}_{}_{}.parquet'.format(site3, interval, 'temp'), index=True)
