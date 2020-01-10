# firs we load the data
import pandas as pd
import os, sys
import pickle

from bokeh.plotting import figure, curdoc
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral5
from bokeh.models import ColumnDataSource

#----------------------------------------
# This section is not directly related to the plotting tutorial
# Loadding the data
json_file = './data/TABLA_MTDATA_CDK2_402_crys_LIGS_INFO_LABELS.json'
# Mds points
mds_file = './data/cMDS_Pisani_402_obj.pyobj'
if os.path.isfile(json_file) and os.path.isfile(mds_file):
    df_cdk2 = pd.read_json(json_file)
    with open(mds_file, 'rb') as f:
        mds = pickle.load(f)
        mds = mds[0]
else: sys.exit('El archivo json/mds no existe.\nEjecución terminada.')
# Updating the data
df_cdk2['mds_1'] = mds[0]
df_cdk2['mds_2'] = mds[1]
#----------------------------------------

# ColumnData Source
source = ColumnDataSource(data = df_cdk2)

# Creating the colormap
P_LABELS = df_cdk2['Labels_conf'].unique()
cmap_color = factor_cmap('Labels_conf', 'Dark2_5', P_LABELS)

#Creating the plot
f = figure(plot_width = 1200, plot_height = 1200)
f.match_aspect = True
f.title.text = 'MDS projection - CDK2 pdb crystals'
f.sizing_mode = 'scale_height'
f.toolbar_location = 'above'
f.toolbar.logo = None

# Plotting some points
f.circle(x = 'mds_1', y = 'mds_2', source = source, size = 15, color = cmap_color, alpha = 0.7)

# To create the plot with bokeh server
curdoc().add_root(f)
# Execution:
# bokeh serve file.py
