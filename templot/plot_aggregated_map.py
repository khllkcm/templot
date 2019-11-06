"""
Simple plotting function.
"""

import numpy as np
import folium
import json
import pkg_resources
import os

DATA_PATH = pkg_resources.resource_filename('templot', 'data')


def plot_aggregated_map(
    df, var="Quantite2017", group="Regions", agr="average", log="auto"
):

    """
    Plots a map of aggregated values of y by group.

    :param df: data
    :param var: y
    :param group: group variable name
    :param agr: aggregation method
    :return: folium map

    One example of this simple graph:

    .. raw:: html

        <iframe src="examples/out.html" height="600px" width="100%"></iframe>

    """

    aggregates = {
        "average": df.groupby(group)[var].mean(),
        "median": df.groupby(group)[var].median(),
        "max": df.groupby(group)[var].max(),
        "min": df.groupby(group)[var].min(),
        "count": df.groupby(group)[var].count().astype("float"),
    }

    map_data = aggregates[agr]

    if log == "true":
        log_transform = True
    elif log == "false":
        log_transform = False
    else:
        log_transform = np.sqrt(map_data.var()) > 100

    if group == "Regions":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'regions.geojson')).read()
        )

    if group == "Departements":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'departements.geojson')).read()
        )

    if group == "Communes":
        geojson = json.loads(
            open(os.path.join(DATA_PATH, 'communes.geojson')).read()
        )

    for feat in geojson["features"]:
        if feat["properties"]["nom"] in map_data:
            feat["properties"]["data"] = map_data[feat["properties"]["nom"]]
        else:
            feat["properties"]["data"] = 0

    m = folium.Map(tiles="CartoDB positron", zoom_start=2)
    choropleth = folium.Choropleth(
        geo_data=geojson,
        data=np.log(map_data) if log_transform else map_data,
        fill_color="BuPu",
        key_on="feature.properties.nom",
        highlight=True,
        bins=9,
    ).add_to(m)

    choropleth.color_scale.caption = (
        f'{"log" if log_transform else ""} {agr} {var}'
    )

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=["nom", "data"],
            labels=False,
            sticky=False,
            aliases=[
                '<div style="background-color: lightyellow; color: black; padding: 3px; border: 2px solid black; border-radius: 3px;">'
                + item
                + "</div>"
                for item in ["nom", "data"]
            ],
            style="font-family: sans serif;",
            localize=True,
        )
    )

    m.fit_bounds(m.get_bounds())
    return m
