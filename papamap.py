from datetime import datetime, timedelta
import pandas as pd
import folium


def get_papa_time():
    """
    Get datetime object with current UTC date and 21:37 time.
    """
    date = datetime.utcnow()
    return date.replace(hour=21, minute=37, second=0, microsecond=0)


def get_papa_meridian():
    """
    Get the meridian at which it is 21:37.
    """
    now = datetime.utcnow()
    papa = get_papa_time()
    delta = papa - now
    angle = delta.total_seconds() / 240
    if papa - now < timedelta(hours=12):
        return round(angle, 2)
    else:
        return -round((360 - angle), 2)


def get_places(meridian):
    df = pd.read_csv("worldcities.csv")
    df["diff"] = (df["lng"] - meridian).abs()
    df = df[df["population"] >= 500000]
    return df.sort_values("diff").head()


def create_map(meridian):
    my_map = folium.Map(zoom_start=5)
    folium.PolyLine([[89.9, meridian], [-89.9, meridian]], color="yellow", weight=3).add_to(my_map)
    places = get_places(meridian)
    places["label"] = places.apply(lambda x: f"{x['city']}, {x['country']}", axis=1)
    places.apply(lambda x: folium.Marker(location=[x["lat"], x["lng"]],
                                         popup=x["label"]).add_to(my_map),
                 axis=1)
    return my_map._repr_html_()


if __name__ == "__main__":
    papa_meridian = get_papa_meridian()
    print(get_places(papa_meridian))
