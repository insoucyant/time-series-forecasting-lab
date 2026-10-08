"""Unit tests for the ForecastDataset abstraction."""

import pandas as pd
import pytest 

from ts_forecasting_lab.data.dataset import ForecastDataset 

#===========================================================
# Fixtures
#===========================================================

@pytest.fixture
def single_series_data() -> pd.DataFrame:
    """Fixture for a single time series dataset."""

    return pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=10, freq="D"),
            "sales": [100, 120, 130, 150, 170, 160, 180, 200, 210, 220],
        }
    )