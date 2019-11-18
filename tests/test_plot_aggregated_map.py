"""
Unit tests for ``plot_aggregated_map``.
"""
import unittest
from templot import plot_aggregated_map, download_irep, add_regions
import os
import pandas as pd
from unittest import TestCase


class TestPlotAggregatedMap(unittest.TestCase):
    "Tests for submodule plot_aggregated_map"
    filepath = os.path.join('.', 'df_test.csv')

    if not os.path.exists(filepath):
        download_irep(filepath)
        df = pd.read_csv(filepath)
        df = add_regions(
            df, "LLX", "LLY", add=["regions", "departements", "communes"]
        )
        df.to_csv(filepath, index=False)

    df = pd.read_csv(filepath)

    def test_bad_df(self):
        with self.assertRaises(TypeError):
            df = []
            plot_aggregated_map(df)

    def test_bad_vars(self):
        with self.assertRaises(TypeError):
            plot_aggregated_map(
                self.df, vars="Quantite2017", group="Regions", agr="average"
            )

    def test_bad_group(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                vars=["Quantite2017"],
                group="Departement",
                agr="average",
            )

    def test_performance(self):
        with self.assertWarns(UserWarning):
            plot_aggregated_map(
                self.df,
                vars=["Quantite2017"],
                group="Departements",
                agr="average",
            )

    def test_bad_agr(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                vars=["Quantite2017"],
                group="Departements",
                agr="averag",
            )

    def test_bad_height(self):
        with self.assertRaises(TypeError):
            plot_aggregated_map(
                self.df,
                vars=["Quantite2017"],
                group="Regions",
                agr="average",
                height="-1",
            )

    params = [
        [["Quantite2016", "Quantite2017"], "Regions", "average", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "median", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "min", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "max", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "count", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "average", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "median", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "min", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "max", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "count", 200],
    ]

    def test_combinations(self):
        for vars, group, agr, height in self.params:
            with self.subTest():
                try:
                    plot_aggregated_map(self.df, vars, group, agr, height)
                except Exception as e:
                    raise (e)


if __name__ == '__main__':
    unittest.main()