''' Map sites meeting specified criteria '''

import sys
import datetime
import click
import numpy as np
import pandas as pd
from dataretrieval import nwis
from pyproj import Transformer
import xyzservices.providers as xyz

import bokeh
from bokeh.models import ColumnDataSource, TapTool
from bokeh.plotting import figure, show


@click.command()
@click.option('--parameter', 'parameterCd', multiple=True, default=['00010'],
              help='Map stations with specified USGS parameter codes.')
@click.option('--state', 'stateCd', help='State code, e.g.: AK')
@click.option('--county', 'countyCd', help='County FIPS code, e.g.: 47410')
@click.option('--bbox', 'bBox', help='Bounds in W S E N order with decimal degree units.')
@click.option('--start', 'startDt', default=(datetime.datetime.today().date()-datetime.timedelta(days=365)),
              help='Start date in yyyy-mm-dd format.')
@click.option('--end', 'endDt', default=datetime.datetime.today().date(),
              help='End date in yyyy-mm-dd format.')
def cli_map(parameterCd, stateCd, countyCd, bBox, startDt, endDt):
	'''
	Map sites meeting specified criteria.

	This opens a Bokeh web-map of sites meeting user-specified criteria.

	Example:

	python click_map.py --bbox "-92.8,44.2,-88.9,46.0" --start 2010-01-01 --parameter 63680 --parameter 00060

	'''

	def do_transform(lon, lat, transformer):
	  return transformer.transform(lon, lat)


	if int(bokeh.__version__[0]) < 3:
	    print("Incompatible Bokeh version")

	ctx_kwds = (click.get_current_context()).params
	kwds = dict((k, v) for k, v in ctx_kwds.items() if v != None)
	# you are allowed one major filter from: bbox, state, county, huc
	# print(kwds)

	sites, md = nwis.get_info(**kwds)

	# print(sites)
	# print(md)

	WGS_TO_WEBMERCATOR = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

	x, y = do_transform(sites['dec_long_va'], sites['dec_lat_va'], WGS_TO_WEBMERCATOR)
	sites['northing'] = y.tolist()
	sites['easting'] = x.tolist()

	# range bounds supplied in web mercator coordinates
	collar = 5000

	p = figure(
	    x_range=(x.min()-collar, x.max()+collar),
	    y_range=(y.min()-collar, y.max()+collar),
	    x_axis_type="mercator",
	    y_axis_type="mercator",
	    tooltips = [
	        ("name", "@station_nm"),
	        ("number", "@site_no"),
	        ("(Long, Lat)", "(@dec_long_va, @dec_lat_va)")
	    ]
	)

	source = ColumnDataSource(sites)

	p.add_tile(xyz.OpenStreetMap.Mapnik)

	p.circle(
	    x='easting', y='northing',
	    size=10,
	    fill_color='blue', fill_alpha=0.6,
	    line_color=None,
	    source=source
	)

	show(p)


if __name__ == '__main__':
    cli_map()
