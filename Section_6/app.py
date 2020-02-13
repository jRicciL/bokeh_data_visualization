from flask import Flask, render_template
from datetime import datetime
# import the bokhe plot components
from Bokeh_plot import js, div, cdn_js, cdn_js_1, cdn_css

# instantiate the flask app
app = Flask(__name__)

# Create an index page
@app.route('/')
def index():
    return render_template('index.html',
    js = js, div = div,
    cdn_css = cdn_css, cdn_js = cdn_js)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)