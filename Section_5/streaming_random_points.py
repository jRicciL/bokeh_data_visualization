import pandas as pd 
import numpy as np 

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import Range1d

f = figure()

source = ColumnDataSource({
    'x': [],
    'y': [],
    'z': []
})

# Create the glyphs
f.circle(x='x', y='y', color='cyan', line_color = 'blue', size = 'z',
source=source)
# We can use different glyphs
f.line(x = 'x', y = 'y', source = source)

# Create periodic function
def update():
    # updates the data
    new_data = {
        # Create random points
        'x': np.random.randint(100, size = 10),
        'y': np.random.randint(100, size = 10),
        # The size of the dots also var
        'z': np.random.randint(low = 10, high = 30, size = 10)
    }
    source.stream(new_data, rollover = 15)

# personalization of the plot
# Adding static axis
f.x_range = Range1d(0, 100)
f.y_range = Range1d(0, 100)

# Add figure to curdoc
# The function uodate will be called every 1000 mseconds
curdoc().add_root(f)
curdoc().add_periodic_callback(update, 100)