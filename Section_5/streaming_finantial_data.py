import pandas as pd 
import numpy as np 

import requests
from bs4 import BeautifulSoup

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models import DatetimeTickFormatter

from datetime import datetime

# Function for webscrapping
URL = 'https://bitcoincharts.com/markets/bitstampUSD.html'
HEADER = {'User-Agent': 'Mozilla/5.0'}

def scrap_value():
    r = requests.get(URL, headers = HEADER)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup.find_all('div', {'id': 'market_summary'})[0].span.text)
    last_trade = float(soup.find_all('div', 
    {'id': 'market_summary'})[0].span.text)
    return(last_trade)

source = ColumnDataSource({
    'x': [],
    'y': []
})

f = figure()
# Create the glyphs
f.circle(x='x', y='y', color='cyan', line_color = 'blue',
source=source)
# We can use different glyphs
f.line(x = 'x', y = 'y', source = source)


# Create periodic function
def update():
    # updates the data
    y = scrap_value()
    # x is the last x data
    x = datetime.now()
    new_data = {
        # Create random points
        'x': [x],
        'y': [y],
    }
    source.stream(new_data, rollover = 100)

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

curdoc().add_root(f)
curdoc().add_periodic_callback(update, 2000)