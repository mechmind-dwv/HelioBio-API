"""Tests para el módulo de análisis avanzado"""

from datetime import datetime

import numpy as np
import pandas as pd
import pytest


class TestAdvancedAnalyzer:
    """Tests para el módulo de análisis"""

    @pytest.fixture
    def sample_solar_data(self):
        """Genera datos solares de prueba"""
        dates = pd.date_range(start="2020-01-01", periods=100, freq="ME")
        ssn = 50 + 30 * np.sin(2 * np.pi * np.arange(100) / (11.2 * 12))
        return pd.DataFrame({"date": dates, "sunspot_number": ssn})

    @pytest.fixture
    def sample_events(self):
        """Genera eventos de prueba"""
        return [
            {"start_date": "2020-03-01", "end_date": "2020-09-01", "death_count": 5000},
            {"start_date": "2022-01-01", "end_date": "2022-06-01", "death_count": 10000},
            {"start_date": "2024-03-01", "end_date": "2024-12-01", "death_count": 20000},
        ]

    def test_solar_data_generation(self, sample_solar_data):
        """Test que los datos solares de prueba son válidos"""
        assert len(sample_solar_data) == 100
        assert "date" in sample_solar_data.columns
        assert "sunspot_number" in sample_solar_data.columns
        assert sample_solar_data["sunspot_number"].min() >= 0

    def test_events_have_required_fields(self, sample_events):
        """Test que los eventos tienen campos requeridos"""
        for event in sample_events:
            assert "start_date" in event
            assert "end_date" in event
            assert "death_count" in event

    def test_correlation_basic(self, sample_solar_data):
        """Test de correlación básica"""
        from scipy import stats

        x = sample_solar_data["sunspot_number"].values
        y = np.sin(np.linspace(0, 4 * np.pi, len(x))) * 50 + 100
        corr, p_value = stats.pearsonr(x, y)
        assert -1.0 <= corr <= 1.0
        assert 0.0 <= p_value <= 1.0
