import numpy as np
import pandas as pnd
import matplotlib.pyplot as plt
import matplotlib.dates as dates

file1 = "BSR_turb_ds_USGS_015765195_original.csv"
file2 = "BSR_turb_west_USGS_015765185_original.csv"
file3 = "BSR_turb_east_USGS_01576516_original.csv"

site1 = "015765195"
site2 = "015765185"
site3 = "01576516"

col_names = ['siteno', 'datetime_str', '63680', 'approval']

turb1 = pnd.read_csv(
    '..\\data-download\\turbidity\\{}'.format(file1),
    header=0,
    names=col_names,
    parse_dates=True
)
print('read file1')

turb2 = pnd.read_csv(
    '..\\data-download\\turbidity\\{}'.format(file2),
    header=0,
    names=col_names,
    parse_dates=True
)
print('read file2')

turb3 = pnd.read_csv(
    '..\\data-download\\turbidity\\{}'.format(file3),
    header=0,
    names=col_names,
    parse_dates=True
)
print('read file3')

# make the site_no column
turb1['site_no'] = turb1['siteno'].apply(lambda x: x[5:])
turb2['site_no'] = turb2['siteno'].apply(lambda x: x[5:])
turb3['site_no'] = turb3['siteno'].apply(lambda x: x[5:])
turb1.drop('siteno', axis=1, inplace=True)
turb2.drop('siteno', axis=1, inplace=True)
turb3.drop('siteno', axis=1, inplace=True)

index_col = 'datetime'

turb1[index_col] = pnd.to_datetime(turb1['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
turb2[index_col] = pnd.to_datetime(turb2['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
turb3[index_col] = pnd.to_datetime(turb3['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))

print(turb1.head())
print(turb1.dtypes)

# reindex to freq of 15T (15 minutes)
start = min(turb1.iloc[0].datetime, turb2.iloc[0].datetime, turb3.iloc[0].datetime)
print(start)
end = max(turb1.iloc[-1].datetime, turb2.iloc[-1].datetime, turb3.iloc[-1].datetime)
print(end)

turb1.set_index(turb1[index_col])
turb2.set_index(turb2[index_col])
turb3.set_index(turb3[index_col])

# fix numeric problems
turb1['63680'] = pnd.to_numeric(turb1['63680'], errors='coerce')
turb2['63680'] = pnd.to_numeric(turb2['63680'], errors='coerce')
turb3['63680'] = pnd.to_numeric(turb3['63680'], errors='coerce')

# set too small values to nan
mask1 = turb1['63680'] <= 0.00001
turb1.loc[mask1, '63680'] = np.NaN

mask2 = turb2['63680'] <= 0.00001
turb2.loc[mask2, '63680'] = np.NaN

mask3 = turb3['63680'] <= 0.00001
turb3.loc[mask3, '63680'] = np.NaN

# write out the new files
turb1.to_csv('..\\data\\lang_{}_{}_{}.csv'.format(site1, 'instantaneous', 'turbidity'))
turb2.to_csv('..\\data\\lang_{}_{}_{}.csv'.format(site2, 'instantaneous', 'turbidity'))
turb3.to_csv('..\\data\\lang_{}_{}_{}.csv'.format(site3, 'instantaneous', 'turbidity'))

turb1.to_parquet('..\\data\\lang_{}_{}_{}.parquet'.format(site1, 'instantaneous', 'turbidity'))
turb2.to_parquet('..\\data\\lang_{}_{}_{}.parquet'.format(site2, 'instantaneous', 'turbidity'))
turb3.to_parquet('..\\data\\lang_{}_{}_{}.parquet'.format(site3, 'instantaneous', 'turbidity'))
