"""Fixtures compartidas para todos los tests"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mock_solar_dataframe():
    """DataFrame solar de prueba"""
    dates = pd.date_range(start="2020-01-01", periods=48, freq="M")
    ssn = np.sin(np.linspace(0, 4 * np.pi, 48)) * 50 + 100
    return pd.DataFrame(
        {
            "date": dates,
            "sunspot_number": ssn,
            "flare_activity": ssn * 0.1,
            "geomagnetic_storm": ssn * 0.5,
            "classification": ["high" if s > 100 else "low" for s in ssn],
        }
    )
