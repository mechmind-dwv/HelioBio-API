"""Tests para el módulo de obtención de datos"""

from datetime import datetime

import pytest

from app.core.data_fetcher import SolarDataFetcher
from app.models.solar import SolarCyclePhase


class TestSolarDataFetcher:
    """Tests para SolarDataFetcher"""

    def test_fetcher_initialization(self):
        """Test que el fetcher se inicializa correctamente"""
        fetcher = SolarDataFetcher()
        assert fetcher.session is None
        assert hasattr(fetcher, "_get_cache_path")

    def test_determine_solar_cycle_phase_minimum(self):
        """Test fase mínima del ciclo (SSN muy bajo)"""
        fetcher = SolarDataFetcher()
        date = datetime(2020, 1, 15)
        phase = fetcher._determine_solar_cycle_phase(date, 5)
        assert phase == SolarCyclePhase.MINIMUM

    def test_determine_solar_cycle_phase_ascending(self):
        """Test fase ascendente (SSN moderado-bajo)"""
        fetcher = SolarDataFetcher()
        date = datetime(2022, 6, 15)
        phase = fetcher._determine_solar_cycle_phase(date, 45)
        assert phase in (SolarCyclePhase.ASCENDING, SolarCyclePhase.MAXIMUM)

    def test_determine_solar_cycle_phase_maximum(self):
        """Test fase máxima (SSN muy alto)"""
        fetcher = SolarDataFetcher()
        date = datetime(2024, 3, 15)
        phase = fetcher._determine_solar_cycle_phase(date, 150)
        assert phase == SolarCyclePhase.MAXIMUM
