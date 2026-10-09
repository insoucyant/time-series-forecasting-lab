"""Unit tests for the ForecastDataset abstraction."""

"""
#==========================================================
Run the Test
</> Bash
python -m pytest tests/data/test_dataset.py -v
Run the entire exisiting test suite:
python -m pytest tests/ -v
If you are using uv for dependency management, the equivalent is:
uv run pytest tests/data/test_dataset.py -v 
"""

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


# =======================================================================
# 2. Required Columns
# =======================================================================

def test_missing_timestamp_column():
    """Reject the datasets without the configured timestamp column."""

    data = pd.DataFrame({"sales": [10,20,30]})

    with pytest.raises(ValueError, match="missing required column"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )

def test_missing_target_column():
    """Reject dataset without the configured target column."""

    data = pd.DataFrame(
        {"timestamp": pd.date_range("2026-01-01", periods=3)}
    )

    with pytest.raises(ValueError, match="missing required column"):
        ForecastDataset(
            data=data,
            timestamp="col_timestamp",
            target_col="sales",
            frequency="D"
        )

def test_missing_series_id_column(single_series_id):
    """Reject a missing configured series identifier column."""

    with pytest.raises(ValueError, mathc="missing required column"):
        ForecastDataset(
            data=single_series_data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
            series_id_col="series_id",
        )



# =======================================================================
# 3. Timestamp Validation
# =======================================================================


def test_string_timestamps_are_converted():
    """Validate valid timestamp strings are coverted to datetime."""

    data = pd.DataFrame(
        {
            "timestamp": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "sales": [10,20,30],  
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert pd.api.types.is_datetime64_any_dtype(
        dataset.data["timestamp"]
    )

def test_invalid_timestamp():
    """Reject unparsebale timestamp."""

    data = pd.DataFrame(
        {
            "timestamp": ["2026-01-01", "invalid_date"],
            "sales": [10,20],
        }
    )

    with pytest.raises(ValueError, match="invalid timestamps"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D", 
        )

def test_missing_timestamp():
    """reject missing timestamp values."""

    data = pd.DataFrame(
        {
            "timestamp": [pd.Timestamp("2026-01-01"), pd.NaT],
            "sales": [10,20],
        }
    )

    with pytest.raises(ValueError, match="missing values"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )


# =======================================================================
# 4. Target Validation
# =======================================================================


def test_missing_target_value():
    """Reject missing target values."""

    data = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=3),
            "sales": [100, None, 120],
        }
    )

    with pytest.raises(ValueError, match="contains missing values"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )

def test_zero_target_is_valid():
    """Verify zero is acceptable as a valid target."""

    data = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=3),
            "sales": [0, 10, 0],
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert dataset.n_rows == 3

def test_negative_target_is_valid():
    """Verify negative targets are not automatically rejected."""

    data = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=3),
            "sales": [-10, 0, 20],
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert dataset.n_rows == 3

# =======================================================================
# 5. Series Identifier Validation
# ======================================================================= 

def test_missing_series_identifier():
    """Reject missing identifiers in multi-series datasets."""

    data = pd.DataFrame(
        {
            "series_id": ["A", None, "A"],
            "timestamp": pd.date_range("2026-01-01", periods=3),
            "sales": [10, 20, 30],
        }
    )

    with pytest.raises(ValueError, match="missing values"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
            series_id_col="series_id",
        )

def test_same_timestamp_across_series_is_valid(multi_series_data):
    """Allow different series to share timestamps."""

    dataset = ForecastDataset(
        data=multi_series_data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
        series_id_col="series_id"
    )

    assert dataset.n_series == 2


# =======================================================================
# 6. Duplicate Detection
# =======================================================================

def test_duplicate_timestamp_single_series():
    """Reject duplicate timestamps in a single series."""

    data = pd.DataFrame(
        {
            "timestamp": ["2026-01-01", "2026-01-01"],
            "sales": [10, 20],
        }
    )

    with pytest.raises(ValueError, match="duplicate timestamp"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )
def test_duplicate_timestamp_within_series():
    """Reject duplicate (series_id, timestamp) combinations."""

    data = pd.DataFrame(
        {
            "series_id": ["A", "A", "B"],
            "timestamp": [
                "2026-01-01",
                "2026-01-01",
                "2026-01-01",
            ],
            "sales": [10, 20, 30],  
        }
    )

    with pytest.raises(ValueError, match="duplicate timestamp"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
            series_id_col="series_id", 
        )


# =======================================================================
# 7. Frequency Validation
# =======================================================================




# =======================================================================
# 8. Sorting
# =======================================================================



# =======================================================================
# 9. Public Methods
# =======================================================================



# =======================================================================
# 10. Data Isolation
# =======================================================================





# =======================================================================
# 11. Additional Edge Cases
# =======================================================================
