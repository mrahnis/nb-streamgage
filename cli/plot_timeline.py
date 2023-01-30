''' display a gage parameter timeline '''

import sys
import datetime
import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataretrieval import nwis


@click.command()
@click.argument('gage', nargs=1, default='01575900')
@click.option('--parameter', 'parameters', multiple=True, default=['00010'],
              help='Map stations with specified USGS parameter codes.')
@click.option('--start', default=(datetime.datetime.today().date()-datetime.timedelta(days=3*365)), prompt='Start date',
              help='Start date in yyyy-mm-dd format.')
@click.option('--end', default=datetime.datetime.today().date(), prompt='End date',
              help='End date in yyyy-mm-dd format.')
def cli_gage_timeline(gage, parameters, start, end):

	service = 'iv' # daily value dv, or instantaneous value iv

	df = nwis.get_record(sites=gage, service=service, start=start, end=end)
	'''
	if parameterCd in list(df.columns):
		pass
	else:
		click.echo('{} is not present'.format(parameterCd))
		click.echo('Available columns: {}'.format(list(df.columns)))
		sys.exit()
	'''
	df.reset_index(inplace=True)
	df.rename(columns={'datetime': 'datetime_str'}, inplace=True)
	df['datetime_str'] = df['datetime_str'].apply(lambda x: str(x)[:10]+' '+str(x)[11:])
	df['datetime'] = pd.to_datetime(df['datetime_str'], utc=True)
	df['datetime'] = df['datetime'].dt.tz_convert('EST')
	df.set_index(df['datetime'], inplace=True)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title('Gage No {}'.format(gage))

	for i, parameter in enumerate(parameters):
		events = (df[parameter]).where(df[parameter].isna(), i)
		events.plot(ax=ax, alpha=0.5, linewidth=20.0, solid_capstyle='butt')

	plt.yticks(np.arange(len(parameters)), parameters)
	plt.show()


if __name__ == '__main__':
    cli_gage_timeline()
