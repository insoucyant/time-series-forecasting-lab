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

@pytest.fixture
def multi_series_data() -> pd.DataFrame:
    """Fixture for a multi time series dataset."""

    return pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2020-01-01", periods=10, freq="D").tolist() * 2,
            "store_id": [1] * 10 + [2] * 10,
            "sales": [100, 120, 130, 150, 170, 160, 180, 200, 210, 220] + 
                     [90, 110, 120, 140, 160, 150, 170, 190, 200, 210], 
        }
    )

@pytest.fixture
def single_dataset(single_series_data: pd.DataFrame) -> ForecastDataset:
    """Create a validated singles-series ForecastDataset."""

    return ForecastDataset(
        data=single_series_data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

@pytest.fixture
def multi_dataset(multi_series_data: pd.DataFrame) -> ForecastDataset:
    """Create a validated multi-series ForecastDataset."""

    return ForecastDataset(
        data=multi_series_data,
        timestamp_col="timestamp",
        target_col="sales", 
        frequency="D",
        series_id_col="series_id",
    )