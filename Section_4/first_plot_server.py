import pandas as pd

from bokeh.plotting import figure, curdoc
# from bokeh.layouts import layout, column
from bokeh.palettes import Spectral4
from bokeh.sampledata.stocks import AAPL, IBM, MSFT, GOOG

p = figure(plot_width = 1200, plot_height = 400, x_axis_type = 'datetime')
p.title.text = 'First Plot with Bokeh Server'
p.title.align = 'center'
p.title.text_font_size = '2em'
p.axis.axis_line_width = 3
p.axis.major_tick_line_width = 6

# Text
p.axis.axis_label_text_font_size = '1.5em'
p.axis.axis_label_text_font_style = 'bold'
p.axis.major_label_text_font_size = '1.2em'
p.xaxis.axis_label = 'X axis'
p.yaxis.axis_label = 'Year'

# Responsive plot
p.sizing_mode = 'scale_both'

for data, name, color in zip([AAPL, IBM, MSFT, GOOG],  ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    p.line(df['date'], df['close'], line_width = 3,
            color = color, alpha = 0.8, legend = name,
            muted_color=color, muted_alpha=0.1)

p.legend.location = 'top_left'
p.legend.click_policy = 'hide'


curdoc().add_root(p)

