import pandas as pnd
import matplotlib.pyplot as plt

interval = 'instantaneous'  # instantaneous or daily

if interval is 'instantaneous':
    file = "BSR_15min_sediment_loads_WY2009_2015.csv"
    index_col = 'datetime'
    data_col = 'SSC_conc'
    col_names = [
        'siteNo',
        'datetime_str',
        'Q_inst',
        'Q_source',
        'Turb_inst',
        'Turb_source',
        'SSC_conc',
        'SSC_source',
        'uv15min_SSC_Load'
    ]
else:
    file = "BSR_daily_sediment_loads_2009_2015.csv"
    index_col = 'datetime'
    data_col = 'daily_SSC_Load'
    col_names = [
        'siteNo',
        'datetime_str',
        'daily_SSC_Load',
        'daily_count'
    ]

site1 = "015765195"
site2 = "015765185"
site3 = "01576516"


loads = pnd.read_csv(
    '..\\data-download\\loads\\{}'.format(file),
    header=0,
    names=col_names,
    parse_dates=False
)

# make the site_no column
loads['site_no'] = loads['siteNo'].apply(lambda x: x[5:])
loads.drop('siteNo', axis=1, inplace=True)

# format the data
loads1 = loads[loads['site_no'] == site1].copy()
loads2 = loads[loads['site_no'] == site2].copy()
loads3 = loads[loads['site_no'] == site3].copy()

# localize to set the missing timezone, metadata indicates the USGS times are EST
#loads1[index_col] = pnd.to_datetime(loads1[col_names[1]], format='%Y-%m-%d %H:%M:%S')
loads1[index_col] = pnd.to_datetime(loads1['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
loads2[index_col] = pnd.to_datetime(loads2['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))
loads3[index_col] = pnd.to_datetime(loads3['datetime_str'].str.strip()).map(lambda x: x.tz_localize('EST'))

print(loads1.head())
print(loads1.dtypes)

loads1.drop('datetime_str', axis=1, inplace=True)
loads2.drop('datetime_str', axis=1, inplace=True)
loads3.drop('datetime_str', axis=1, inplace=True)

# reset the index to datetime column
loads1.reset_index(drop=True, inplace=True)
loads2.reset_index(drop=True, inplace=True)
loads3.reset_index(drop=True, inplace=True)

loads1.set_index(index_col, inplace=True)
loads2.set_index(index_col, inplace=True)
loads3.set_index(index_col, inplace=True)

# write out the data
loads1.to_csv('..\\data\\lang_{}_{}_loads.csv'.format(site1, interval))
loads1.to_parquet('..\\data\\lang_{}_{}_loads.parquet'.format(site1, interval), index=True)

loads2.to_csv('..\\data\\lang_{}_{}_loads.csv'.format(site2, interval))
loads2.to_parquet('..\\data\\lang_{}_{}_loads.parquet'.format(site2, interval), index=True)

loads3.to_csv('..\\data\\lang_{}_{}_loads.csv'.format(site3, interval))
loads3.to_parquet('..\\data\\lang_{}_{}_loads.parquet'.format(site3, interval))
