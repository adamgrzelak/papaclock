from flask import Flask, render_template, Markup
from papamap import *


app = Flask(__name__)


@app.route("/")
def home():
    meridian = get_papa_meridian()
    papamap = create_map(meridian)
    return render_template("index.html", map=Markup(papamap))


app.run(debug=True)
