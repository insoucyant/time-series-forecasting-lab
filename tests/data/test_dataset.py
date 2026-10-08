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

# =======================================================================
# 1. Initialization
# =======================================================================

def test_single_series_initialization(single_dataset):
    """Verify single-series initialization."""

    assert isinstance(single_dataset, ForecastDataset)
    assert single_dataset.n_rows == 10
    assert single_dataset.n_series == 1
    assert single_dataset.is_multi_series is False

def test_multi_series_initialization(multi_dataset):
    """Verify multi-series initialization"""

    assert isinstance(multi_dataset, ForecastDataset)
    assert multi_dataset.n_rows == 20
    assert multi_dataset.n_series == 2
    assert multi_dataset.is_multi_series is True

def test_empty_dataframe():
    """Reject an empty dataset."""

    data = pd.DataFrame(columns=["timestamp", "sales"])

    with pytest.raises(ValueError, match="empty DataFrame"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )

        
