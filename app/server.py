import re

from flask import Flask
from flask import make_response
from flask import render_template
from markupsafe import Markup

from app.papamap import create_map
from app.papamap import get_nearest_timezome
from app.papamap import get_papa_meridian


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
        if re.match(r"21:37:..", val) is not None:
            return f"<span style='color: #F2DF3A; font-weight: bold;'>{val}</span>"
        else:
            return val

    table = get_nearest_timezome()
    is_papatime = (
        table["time"].apply(lambda x: re.match(r"21:37:..", x) is not None).any()
    )
    table = table.rename(columns={"timezone": "Strefa Czasowa", "time": "Godzina"})
    table = table.to_html(
        index=False, formatters={"Godzina": yellow_hour}, escape=False
    )
    if is_papatime:
        return make_response(
            {
                "table": table,
                "message": "<img src='../static/papaj.gif' alt='' "
                "style='margin-bottom: 2%; border-radius: 2%;'>"
                "<h2 class='message'>Gdzieś na świecie jest 21:37!</h2>",
            }
        )
    else:
        return make_response(
            {
                "table": table,
                "message": "<h4 class='message'>21:37 nadchodzi w następujących miejscach:</h4>",
            }
        )


@app.route("/get_map")
def get_map():
    meridian = get_papa_meridian()
    papamap = create_map(meridian)
    return make_response({"papamap": Markup(papamap)})


if __name__ == "__main__":
    app.run(debug=True)
