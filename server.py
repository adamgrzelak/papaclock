from flask import Flask, render_template, Markup, make_response
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
    return render_template("table.html")


@app.route("/get_table")
def get_table():
    table = get_nearest_timezome()
    table = table.to_html(index=False)
    return make_response({"table": Markup(table)})


@app.route("/get_map")
def get_map():
    meridian = get_papa_meridian()
    papamap = create_map(meridian)
    return make_response({"papamap": Markup(papamap)})


app.run(debug=True)
