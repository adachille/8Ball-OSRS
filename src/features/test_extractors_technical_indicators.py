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
    
    def test_std_dev(self):
        extractor_ti = ExtractorTechnicalIndicators()
        test_prices = np.array([10, 20, 30, 40, 50])
        expected_std = np.std(test_prices)
        actual_std = extractor_ti.std_dev(test_prices)

        assert type(actual_std) == np.float64
        np.testing.assert_equal(actual_std, expected_std)
    
    def test_bollinger_bands(self):
        extractor_ti = ExtractorTechnicalIndicators()
        test_prices = np.array([10, 20, 30, 40, 50])
        std_dev = np.std(test_prices)
        expected_smas = np.array([np.nan, np.nan, np.nan, 30.0, 40.0])
        expected_lbb = np.array([np.nan, np.nan, np.nan, 30.0 - 2*std_dev, 40.0 - 2*std_dev])
        expected_ubb = np.array([np.nan, np.nan, np.nan, 30.0 + 2*std_dev, 40.0 + 2*std_dev])
        actual_lbb, actual_smas, actual_ubb = extractor_ti.bollinger_bands(test_prices, 3)

        assert type(actual_lbb) == np.ndarray
        np.testing.assert_equal(actual_lbb, expected_lbb)
        assert type(actual_smas) == np.ndarray
        np.testing.assert_equal(actual_smas, expected_smas)
        assert type(actual_ubb) == np.ndarray
        np.testing.assert_equal(actual_ubb, expected_ubb)