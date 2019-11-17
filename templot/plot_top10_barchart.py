"""
Plot Top 10 Barchart
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.cm as cm
from numpy import linspace


def plot_top10_barchart(
    year,
    df,
    values,
    year_var,
    color_var,
    names_var,
    title='',
    label='',
    ax=None,
    **kwargs,
):
    dff = (
        df[df[year_var] == year]
        .sort_values(by=values, ascending=True)
        .tail(10)
    )
    if ax is None:
        ax = plt.gca()
    ax.clear()
    ll = list(dict.fromkeys(df["Regions"]))
    if len(ll) < 8:
        colors = dict(zip(ll, [cm.Set2(x) for x in linspace(0, 0.87, len(ll))]))
    else:
        colors = dict(
            zip(
                ll,
                [cm.Set2(x) for x in linspace(0, 0.87, 8)]
                + [cm.Set3(x) for x in linspace(0.09, 1, len(ll) - 8)],
            )
        )
    bars = ax.barh(
        dff[names_var],
        dff[values],
        color=[colors[x] for x in dff[color_var]],
        alpha=0.73,
        edgecolor='#998D8F',
        linewidth=1.5,
        **kwargs,
    )
    dx = dff[values].max() / 200
    for i, (value, name) in enumerate(zip(dff[values], dff[names_var])):
        if len(name) > 0.43 * value / dx:
            name = name[: int(0.43 * value / dx)] + '..'
        ax.text(value - dx, i, name, size=16, ha='right', va='center')
        ax.text(
            value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center'
        )

        ax.text(
            0.97,
            0.4,
            year,
            transform=ax.transAxes,
            color='#FFECEF',
            size=46,
            ha='right',
            weight=800,
            path_effects=[
                path_effects.Stroke(linewidth=3, foreground='black'),
                path_effects.Normal(),
            ],
        )
    ax.text(0, 1.06, label, transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(
        0, 1.1, title, transform=ax.transAxes, size=24, weight=600, ha='left'
    )
    plt.box(False)
    regions = list(dict.fromkeys(dff[color_var][::-1]))
    lgd = ax.legend(bars, regions, loc=(0.82, 0.03))
    for i, j in enumerate(lgd.legendHandles):
        j.set_color([colors[x] for x in regions][i])
