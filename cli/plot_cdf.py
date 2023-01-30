''' plot annual pdf and cdf for a turbidity series'''

import sys
import datetime
import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataretrieval import nwis


@click.command()
@click.argument('gage', nargs=1, default='01575900')
@click.option('--parameter', default='00010', prompt='Parameter to plot',
              help='USGS parameter code to plot.')
@click.option('--start', default=(datetime.datetime.today().date()-datetime.timedelta(days=3*365)), prompt='Start date',
              help='Start date in yyyy-mm-dd format.')
@click.option('--end', default=datetime.datetime.today().date(), prompt='End date',
              help='End date in yyyy-mm-dd format.')
@click.option('--logx', default=False, help='Plot the parameter values on a log-scale x-axis.', prompt='Log x-axis')
def cli_gage_cdf(gage, parameter, start, end, logx):

	service = 'iv' # daily value dv, or instantaneous value iv

	df = nwis.get_record(sites=gage, service=service, start=start, end=end)

	if parameter in list(df.columns):
		pass
	else:
		click.echo('{} is not present'.format(parameter))
		click.echo('Available columns: {}'.format(list(df.columns)))
		sys.exit()

	df.reset_index(inplace=True)
	df.rename(columns={'datetime': 'datetime_str'}, inplace=True)
	df['datetime_str'] = df['datetime_str'].apply(lambda x: str(x)[:10]+' '+str(x)[11:])
	df['datetime'] = pd.to_datetime(df['datetime_str'], utc=True)
	df['datetime'] = df['datetime'].dt.tz_convert('EST')
	df.set_index(df['datetime'], inplace=True)

	df['WY'] = df.index.shift(3,freq='m').year
	df['WDOY'] =  df.index.dayofyear

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	wys = df['WY'].unique()
	colors = plt.colormaps['viridis_r'](np.linspace(0,1,len(wys)))

	# get pdf and cdf for each wateryear
	for wy, color in zip(wys, colors):
		wy_df = df[df['WY']==wy]
		wy_stats = wy_df.groupby(parameter)[parameter].agg('count').pipe(pd.DataFrame).rename(columns = {parameter: 'frequency'})

		wy_stats['pdf'] = wy_stats['frequency'] / sum(wy_stats['frequency'])
		wy_stats['cdf'] = wy_stats['pdf'].cumsum()
		wy_stats = wy_stats.reset_index()

		wy_stats.plot(x=parameter, y='cdf', ax=ax, logx=logx, alpha=0.7, color=color, label='{} WY'.format(wy))

	ax.set_title('Gage No {}'.format(gage))
	ax.set_ylabel('cumulative percent')
	ax.set_xlabel('parameter')


	'''
	piv = pd.pivot_table(df, index=['WDOY'],columns=['WY'], values=['63680'])

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title('Gage No {}'.format(gage))
	ax.set_ylabel('turbidity')
	piv.plot(ax=ax, alpha=0.5)
	'''

	plt.show()


if __name__ == '__main__':
    cli_gage_cdf()
