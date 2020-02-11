import pandas as pd 
import numpy as np 

import requests
from bs4 import BeautifulSoup

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.layouts import layout
from datetime import datetime
# color palettes
from bokeh.transform import factor_cmap
# Change data
from bokeh.models import Select
# Select options
options = [
    ('bitstampUSD', 'BitStampUSD'),
    ('krakenUSD', 'KrakenUSD'),
    ('bitflyerUSD', 'BitFlyerUSD')
]
select = Select(title = 'Market name',
options = options, value = 'bitstampUSD')

MARKETS = ['bitstampUSD', 'krakenUSD', 'bitflyerUSD']
color_map = factor_cmap('market', 'Dark2_3', MARKETS)

# Function for webscrapping
def scrap_value(market='bitstampUSD'):
    URL = F'https://bitcoincharts.com/markets/{market}.html'
    HEADER = {'User-Agent': 'Mozilla/5.0'}

    r = requests.get(URL, headers = HEADER)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.find_all('div', {'id': 'market_summary'})[0].span.text)
    last_trade = float(soup.find_all('div', 
    {'id': 'market_summary'})[0].span.text)
    return(last_trade)

source = ColumnDataSource({
    'x': [datetime.now()]*3,
    'y': [scrap_value(select.value)]*3,
    'market': MARKETS
})

f = figure()
# Create the glyphs
# Color changes accordingly the market
f.line(x = 'x', y = 'y', source = source)
# We can use different glyphs
f.circle(x='x', y='y', legend_group = 'market', color=color_map, line_color = 'blue',
source=source, size = 12)


# intermediate function
# No needed because we used:
# lambda attr, fdfdold, new: update()
#def update_intermediate(attr, old, new):
#    update()

# Create periodic function
def update():
    # updates the data
    y = scrap_value(select.value)
    # x is the last x data
    x = datetime.now()
    new_data = {
        # Create random points
        'x': [x],
        'y': [y],
        'market': [select.value]
    }
    source.stream(new_data, rollover = 100)
    #n_points = len(source.data['x'])
    #source.data['market'] = [select.value] * n_points
    

f.xaxis.formatter = DatetimeTickFormatter(
    seconds = ['%Y-%m-%d-%H:%M:%S'],
    minsec = ['%Y-%m-%d-%H:%M:%S'],
    minutes = ['%Y-%m-%d-%H:%M:%S'],
    hourmin = ['%Y-%m-%d-%H:%M:%S'],
    hours = ['%Y-%m-%d-%H:%M:%S'],
    days = ['%Y-%m-%d-%H:%M:%S'],
    months = ['%Y-%m-%d-%H:%M:%S'],
    years = ['%Y-%m-%d-%H:%M:%S']
)

# Rotate the labels
f.xaxis.major_label_orientation = np.pi /4
f.legend.location = 'top_left'
# the intermediate functions works as an interface to call update() from periodic_callback
select.on_change('value',  lambda attr, old, new: update())

lay_out = layout([[f, [select]]])
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 2000)