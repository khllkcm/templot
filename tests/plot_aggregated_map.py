"""
Unit tests for ``plot_aggregated_map``.
"""
import unittest
from templot import plot_aggregated_map


class TestPlotAggregatedMap(unittest.TestCase):
    "Tests for submodule plot_aggregated_map"

    def test_empty(self):
        with self.assertRaises(AttributeError):
            df = []
            plot_aggregated_map(df)


if __name__ == '__main__':
    unittest.main()
