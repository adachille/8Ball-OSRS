import pytest
import numpy as np
from extractors_technical_indicators import ExtractorTechnicalIndicators

class TestExtractorTechnicalIndicators: 
    def test_simple_moving_average(self):
        extractor_ti = ExtractorTechnicalIndicators()
        test_prices = np.array([10, 20, 30, 40, 50])
        expected_smas = np.array([np.nan, np.nan, np.nan, 30.0, 40.0])
        actual_smas = extractor_ti.simple_moving_average(test_prices, 3)
        assert type(actual_smas) == np.ndarray
        np.testing.assert_equal(actual_smas, expected_smas)

    def test_exponential_moving_average(self):
        extractor_ti = ExtractorTechnicalIndicators()
        test_prices = np.array([10, 20, 30, 40, 50])
        expected_emas = np.array([np.nan, np.nan, np.nan, 30.0, 40.0])
        actual_emas = extractor_ti.exponential_moving_average(test_prices, 3, 0.5)
        assert type(actual_emas) == np.ndarray
        np.testing.assert_equal(actual_emas, expected_emas)

        # Test that the default weighting = 2 / (n + 1) = 0.5
        actual_emas = extractor_ti.exponential_moving_average(test_prices, 3)  
        np.testing.assert_equal(actual_emas, expected_emas)