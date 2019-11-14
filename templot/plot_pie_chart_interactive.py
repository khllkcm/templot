"""
Plots an Interactive pie chart.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_pie_chart_interactive(df, col, year, year1, sticker):

    """
    Plots an interactive pie chart of sticker by col.

    :param df: data
    :param col: column of df (omitting the year)
    :param year: the first year
    :param year1: the second year
    :param sticker: column of df (the individuals in the pie chart)
    :return: Plotly figure

    One example of this simple graph:

    .. raw:: html

        <iframe src="example_ipchar.html" height="620px" width="100%"></iframe>

    """

    test = list(set(df[sticker]))
    d1 = {key: 0 for key in test}
    d = {key: 0 for key in test}
    label, label1 = col + str(year), col + str(year1)
    for i in range(df.shape[0]):
        d[df.loc[i, sticker]] += df.loc[i, label]
        d1[df.loc[i, sticker]] += df.loc[i, label1]
    labels = list(d.keys())
    values = list(d.values())
    labels1 = list(d1.keys())
    values1 = list(d1.values())
    fig = make_subplots(
        rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]]
    )
    fig.add_trace(go.Pie(labels=labels, values=values, name=year), 1, 1)
    fig.add_trace(go.Pie(labels=labels1, values=values1, name=year1), 1, 2)
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="Le pourcentage de "
        + col.lower()
        + " de différentes régions dans 2 années consécutives",
        annotations=[
            dict(text=year, x=0.18, y=0.5, font_size=20, showarrow=False),
            dict(text=year1, x=0.82, y=0.5, font_size=20, showarrow=False),
        ],
    )
    return fig
