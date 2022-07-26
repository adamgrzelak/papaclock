from flask import Flask, render_template, Markup
from papamap import *


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meridian")
def meridian():
    meridian = get_papa_meridian()
    papamap = create_map(meridian)
    return render_template("meridian.html", map=Markup(papamap))


@app.route("/table")
def table():
    table = get_nearest_timezome()
    table = table.to_html(index=False)
    return render_template("table.html", table=Markup(table))


app.run(debug=True)
