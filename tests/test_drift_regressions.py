import unittest

import numpy as np
import pandas as pd

from src.drift import numeric_drift_table, population_stability_index


class TestDriftRegressions(unittest.TestCase):
    def test_constant_reference_detects_departure(self):
        self.assertEqual(population_stability_index([5] * 10, [5] * 10), 0)
        self.assertGreater(population_stability_index([5] * 10, [6] * 10), 0)
        self.assertGreater(population_stability_index([5] * 10, [4] * 10), 0)

    def test_binary_distribution_change_is_not_zero(self):
        self.assertGreater(population_stability_index([0, 1] * 10, [1] * 20), 0)

    def test_invalid_configuration_fails(self):
        for kwargs in ({"bins": 0}, {"eps": 0}, {"eps": np.nan}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                population_stability_index([0, 1], [0, 1], **kwargs)

    def test_no_numeric_features_returns_empty_typed_table(self):
        table = numeric_drift_table(pd.DataFrame({"name": ["a"]}), pd.DataFrame({"name": ["b"]}))
        self.assertTrue(table.empty)
        self.assertIn("psi", table.columns)
