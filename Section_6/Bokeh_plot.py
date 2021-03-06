# firs we load the data
import pandas as pd
import os, sys
import pickle

from bokeh.plotting import figure, curdoc
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource
# Labels
from bokeh.models import LabelSet
# Widgets
from bokeh.models.widgets import Select, RadioGroup
from bokeh.layouts import layout

# embeding
from bokeh.embed import components
# To generate the CDN request of bokeh js and css
from bokeh.resources import CDN

#----------------------------------------
# This section is not directly related to the plotting tutorial
# Loadding the data
json_file = './static/data/TABLA_MTDATA_CDK2_402_crys_LIGS_INFO_LABELS.json'
# Mds points
mds_file = './static/data/cMDS_Pisani_402_obj.pyobj'
if os.path.isfile(json_file) and os.path.isfile(mds_file):
    df_cdk2 = pd.read_json(json_file)
    with open(mds_file, 'rb') as f:
        mds = pickle.load(f)
        mds = mds[0]
else: sys.exit('El archivo json/mds no existe.\nEjecución terminada.')
# Updating the data
df_cdk2['mds_1'] = mds[0]
df_cdk2['mds_2'] = mds[1]
df_cdk2.reset_index(inplace = True)
df_cdk2.Resolution = df_cdk2.Resolution.round(2)
#----------------------------------------

# ColumnData Source
source = ColumnDataSource(data = df_cdk2)

# Creating the colormap
P_LABELS = df_cdk2['Labels_conf'].unique()
cmap_color = factor_cmap('Labels_conf', 'Dark2_6', P_LABELS)

#Creating the plot
f = figure(plot_width = 900, plot_height = 900,
active_scroll='wheel_zoom')
f.match_aspect = True
f.title.text = 'MDS projection - CDK2 pdb crystals'
f.sizing_mode = 'scale_height'
f.toolbar_location = 'above'
f.toolbar.logo = None

# Fist labels
labels = LabelSet(x = 'mds_1', y = 'mds_2', text = 'index', source = source)
f.add_layout(labels)

# Plotting some points
points_crystals = f.circle(x = 'mds_1', y = 'mds_2', source = source, size = 12, color = cmap_color, alpha = 0.7)

# Select labels widget
## These are the posible values to show
options = [("index", "PDB ID"),
            ("Inhib", "Ligand Name"),
            ("Resolution", "Resolution"),
            ('None', 'Hide')]
select = Select(title = 'Atribute to show',
    options = options)

# Function to update
def update_labels(attr, old, new):
    if select.value == 'None':
        labels.text_alpha = 0
    else:
        labels.text_alpha = 1
        labels.text = select.value
# The following code defines the action to perform
select.on_change("value", update_labels)

## Changing the size of the points
labels_sizes = ['Pequeño',
                'Mediano',
                'Grande']
list_sizes =  [8, 12, 15]
#select_size = Select(title = 'Points sizes', options = options_size)
radioGroup_size = RadioGroup(labels= labels_sizes, active = 1)
# Function to update
def update_points_size(attr, old, new):
    index = radioGroup_size.active
    points_crystals.glyph.size = list_sizes[index]
radioGroup_size.on_change("active", update_points_size)


# Makeup
f.title.align = 'center'
f.title.text_font_size = '2em'
f.axis.axis_line_width = 5
f.axis.major_tick_line_width = 6
# Text
f.axis.axis_label_text_font_size = '1.5em'
f.axis.axis_label_text_font_style = 'bold'
f.axis.major_label_text_font_size = '1.2em'
f.xaxis.axis_label = 'First Dimension'
f.yaxis.axis_label = 'Second Dimension'

# Create the lay_out
lay_out = layout([[f, [select, radioGroup_size]]])


# embeding in a flask app
# component returns the javascript and the html
js, div = components(lay_out)

# CDN reequest
cdn_js = CDN.js_files[0]
cdn_js_1 = CDN.js_files[2]
cdn_css = CDN.css_files