from datetime import datetime, timedelta
import pytz
import pandas as pd
import folium
from flask import Markup


def load_cities():
    """
    Load the dataframe with world cities.
    """
    return pd.read_csv("worldcities.csv", index_col=False)


def get_papa_time():
    """
    Get datetime object with current UTC date and 21:37 time.
    """
    now = datetime.now(tz=pytz.UTC)
    papatime = now.replace(hour=21, minute=37, second=0, microsecond=0)
    return papatime


def get_papa_meridian():
    """
    Get the meridian at which the time is 21:37.
    """
    now = datetime.now(tz=pytz.UTC)
    papa = get_papa_time()
    delta = papa - now
    angle = delta.total_seconds() / 240
    if papa - now < timedelta(hours=12):
        return round(angle, 2)
    else:
        return -round((360 - angle), 2)


def get_nearest_timezome():
    """
    Find major cities where 21:37 is approaching
    (within one hour).
    """
    df = pd.DataFrame({"timezone": pytz.common_timezones})
    df["time"] = df["timezone"].apply(lambda x: datetime.now(tz=pytz.timezone(x)))
    df["papa"] = df["time"].apply(lambda x: x.replace(hour=21, minute=37, second=0, microsecond=0))
    df["delta"] = df["papa"] - df["time"]
    df = df[(df["delta"] > timedelta(hours=0)) & (df["delta"] < timedelta(hours=1))]
    df["city"] = df["timezone"].apply(lambda x: str(x.split("/")[-1])).astype(object)
    places = load_cities().set_index("city")
    df = df.set_index("city")
    joint = df.join(places, how="inner").reset_index()
    joint = joint[joint["population"] >= 1000000]
    joint["time"] = joint["time"].apply(lambda x: x.strftime("%H:%M"))
    return joint[["city", "country", "lat", "lng", "time"]]


def get_places(meridian):
    """
    Get a dataframe of top 5 500k+ cities
    closest to the papa meridian.
    """
    df = load_cities()
    df["diff"] = (df["lng"] - meridian).abs()
    df = df[df["population"] >= 500000]
    return df.sort_values("diff").head()


def create_map(meridian):
    """
    Create HTML code for a Folium map with highlighted papa meridian
    and markers with closest places.
    """
    figure = folium.Figure(width=1200, height=600)
    my_map = folium.Map(zoom_start=5, tiles="stamentoner")
    my_map.add_to(figure)
    # folium.TileLayer("stamentoner").add_to(my_map)
    folium.PolyLine([[89.9, meridian], [-89.9, meridian]], color="yellow", weight=5).add_to(my_map)
    places = get_places(meridian)
    places["label"] = places.apply(lambda x:
                                   Markup(f"<b>{x['city']}</b><br>{x['country']}"),
                                   axis=1)
    places.apply(lambda x: folium.Marker(location=[x["lat"], x["lng"]],
                                         popup=folium.Popup(
                                             folium.IFrame(x["label"],
                                                           width=150, height=60)
                                         )).add_to(my_map),
                 axis=1)
    return figure._repr_html_()


if __name__ == "__main__":
    # papa_meridian = get_papa_meridian()
    # print(get_places(papa_meridian))
    print(get_nearest_timezome())
