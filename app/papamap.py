from datetime import datetime
from datetime import timedelta

import folium
import pandas as pd
import pytz


def load_cities():
    """
    Load the dataframe with world cities.
    """
    return pd.read_csv("app/worldcities.csv", index_col=False)


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
    df["papa"] = df["time"].apply(
        lambda x: x.replace(hour=21, minute=37, second=0, microsecond=0)
    )
    df["delta"] = df.apply(
        lambda x: min(abs(x["papa"] - x["time"]), abs(x["time"] - x["papa"])), axis=1
    )
    df = df[(df["delta"] > timedelta(hours=0)) & (df["delta"] < timedelta(hours=1))]
    df = df[df["time"] < (df["papa"] + timedelta(minutes=1))]
    df["time"] = df["time"].apply(lambda x: x.strftime("%H:%M:%S"))
    df["timezone"] = (
        df["timezone"]
        .apply(lambda x: x.replace("_", " "))
        .apply(
            lambda x: f"{x.split('/')[-1]} ({x.split('/')[0]})"
            if len(x.split("/")) > 1
            else x
        )
    )
    return df[["timezone", "time"]]


def get_places(meridian):
    """
    Get a dataframe of top 5 500k+ cities
    closest to the papa meridian.
    """
    df = load_cities()
    df["diff"] = df["lng"].apply(lambda x: min(abs(x - meridian), abs(meridian - x)))
    diff = 0.25
    while df[df["diff"] <= diff].shape[0] == 0:
        diff = diff * 2
    df = df[df["diff"] <= diff]
    pop = 100000
    while df[df["population"] >= pop].shape[0] == 0 and pop > 1:
        pop = pop / 10
    df = df[df["population"] >= pop]
    return df.sort_values("diff").head(10)


def create_map(meridian):
    """
    Create HTML code for a Folium map with highlighted papa meridian
    and markers with the closest places.
    """
    figure = folium.Figure(width=1200, height=600)
    my_map = folium.Map(
        min_zoom=1,
        location=[0, meridian],
        zoom_start=2,
        tiles="OpenStreetMap",
    )
    my_map.add_to(figure)
    folium.PolyLine(
        [[89.9, meridian], [-89.9, meridian]], color="yellow", weight=5
    ).add_to(my_map)
    places = get_places(meridian)
    if places.shape[0] > 0:
        places["label"] = places.apply(
            lambda x: f"<span style='font-family: Arial; line-height: 1.5rem;'>"
            f"<b>{x['city']}</b><br>{x['country']}<br>"
            f"<span style='text-decoration: underline;'>Odległość:</span> "
            f"{round(x['diff'] * 240)} sekund<br>"
            f"<span style='text-decoration: underline;'>Liczba ludności:</span> "
            f"{'{:,.0f}'.format(x['population']).replace(',', ' ')}"
            f"</span>",
            axis=1,
        )
        places.apply(
            lambda x: folium.Marker(
                location=[x["lat"], x["lng"]],
                popup=folium.Popup(folium.IFrame(x["label"], width=240, height=120)),
                icon=folium.features.CustomIcon(
                    "app/static/papaj.png", icon_size=(40, 50)
                ),
            ).add_to(my_map),
            axis=1,
        )
    return figure._repr_html_()
