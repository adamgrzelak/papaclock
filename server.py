from flask import Flask, Markup, render_template, make_response
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
    def yellow_hour(val):
        if "21:37" in val:
            return f"<span style='color: #F2DF3A; font-weight: bold;'>{val}</span>"
        else:
            return val
    table = get_nearest_timezome()
    is_papatime = table["time"].apply(lambda x: "21:37" in x).any()
    table = table.to_html(index=False, formatters={"time": yellow_hour}, escape=False)
    if is_papatime:
        return make_response({"table": table,
                              "icon": "<img src='static/papaj.gif' alt=''>"})
    else:
        return make_response({"table": table,
                              "icon": ""})


@app.route("/get_map")
def get_map():
    meridian = get_papa_meridian()
    papamap = create_map(meridian)
    return make_response({"papamap": Markup(papamap)})


app.run(debug=True)
