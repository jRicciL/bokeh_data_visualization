import pandas as pd

from bokeh.plotting import figure, curdoc
# from bokeh.layouts import layout, column
from bokeh.palettes import Spectral4
from bokeh.sampledata.stocks import AAPL, IBM, MSFT, GOOG

p = figure(plot_width = 800, plot_height = 250, x_axis_type = 'datetime')
p.title.text = 'First Plot with Bokeh'
p.title.align = 'center'

for data, name, color in zip([AAPL, IBM, MSFT, GOOG],  ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    p.line(df['date'], df['close'], line_width = 2,
            color = color, alpha = 0.8, legend = name,
            muted_color=color, muted_alpha=0.1)

p.legend.location = 'top_left'
p.legend.click_policy = 'hide'


curdoc().add_root(p)

