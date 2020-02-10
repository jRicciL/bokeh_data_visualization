# herein we are running a bokeh server
# how to create widgets with bokeh

# importing libraries
from bokeh.plotting import show
from bokeh.io import curdoc # output_file
from bokeh.models.widgets import TextInput, Button, Paragraph
from bokeh.layouts import layout

# prepare the bokeh output file
# output_file('simple_bokeh.html') ## We don't need it if we use bokeh server

# Create widgets
text_input = TextInput(value = 'Perro')
button = Button(label = 'Generar texto')
# New paragraph to be updated
output = Paragraph()

# Update function
def update():
    output.text = F'Hello, {text_input.value}'

button.on_click(update)

_layout = layout([[button, text_input], [output]])

# Showing function
## show(_layout) ## We don't need it if we use bokeh server

# now with bokeh server
curdoc().add_root(_layout)