"""Unit tests for the ForecastDataset abstraction.
    This file contains **39 Test Functions** across 11 categories. 
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
            "store_id": ["A"] * 10 + ["B"] * 10,
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
        series_id_col="store_id",
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

    with pytest.raises(ValueError, match="dataset is empty"):
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

    with pytest.raises(ValueError, match="required columns are missing"):
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

    with pytest.raises(ValueError, match="require column are missing"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D"
        )

def test_missing_series_id_column(single_series_data):
    """Reject a missing configured series identifier column."""

    with pytest.raises(ValueError, mathc="required columns are missing"):
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

    with pytest.raises(ValueError, match="Failed to convert the timestamp"):
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
        series_id_col="store_id"
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

def test_valid_daily_frequency(single_series_data):
    """Accept a complete daily series."""

    dataset = ForecastDataset(
        data=single_series_data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert dataset.frequency == "D"

def test_invalid_frequency(single_series_data):
    """Reject an invalid frequency alias"""

    with pytest.raises(ValueError, match="Invalid frequency"):
        ForecastDataset(
            data=single_series_data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="NOT_A_FREQUENCY",
        )

def test_missing_daily_period():
    """Reject a gap in otherwise daily series."""

    data = pd.DataFrame(
        {
            "timestamp": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-04",
            ],
            "sales": [10,20,40],
        }
    )

    with pytest.raises(ValueError, match="missing timestamp"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )

def test_inconsistent_frequency():
    """reject timestamps incosnsitent with the declared frequency."""

    data = pd.DataFrame(
        {
            "timestamp": [
                "2026-01-01 00:00:00",
                "2026-01-01 12:00:00",
                "2026-01-02 00:00:00",
            ],
            "sales": [10 ,20, 30],
        }
    )

    with pytest.raises(ValueError, match="inconsistent with frequency"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
        )

def test_missing_period_in_one_series():
    """Validate frequency independently for each series."""

    data = pd.DataFrame(
        {
            "series_id": ["A", "A", "A", "B", "B"],
            "timestamp": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
                "2026-01-01",
                "2026-01-03",
            ],
            "sales": [10, 20, 30, 100, 120],
        }
    )

    with pytest.raises(ValueError, match="series 'B'"):
        ForecastDataset(
            data=data,
            timestamp_col="timestamp",
            target_col="sales",
            frequency="D",
            series_id_col="series_id",
        )

# =======================================================================
# 8. Sorting
# =======================================================================

def test_single_series_is_sorted():
    """Verify timestamps are sorted chornologically."""

    data = pd.DataFrame(
        {
            "timestamp": [
                "2026-01-03",
                "2026-01-01",
                "2026-01-02",
            ],
            "sales": [30,10,20],
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert dataset.data["sales"].tolist() == [10,20,30]

def test_multi_series_is_sorted():
    """Verify sorting by series ID followed by timestamp."""

    data = pd.DataFrame(
        {
            "series_id": ["B", "A", "B", "A"],
            "timestamp": [
                "2026-01-02",
                "2026-01-02",
                "2026-01-01",
                "2026-01-01",
            ],
            "sales": [220, 120, 210, 110],
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
        series_id_col="series_id",
    )

    assert dataset.data["series_id"].tolist() == ["A", "A", "B", "B"]
    assert dataset.data["sales"].tolist() == [110, 120, 210, 220]

# =======================================================================
# 9. Public Methods
# =======================================================================

def test_get_target(single_dataset):
    """Verify target extraction."""

    target = single_dataset.get_target()

    assert isinstance(target, pd.Series)
    assert target.tolist() == [100, 120, 130, 150, 170, 160, 180, 200, 210, 220]

def test_get_series_ids(multi_dataset):
    """Verify unique series identifiers."""

    assert multi_dataset.get_series_ids() == ["A", "B"]

def test_get_series_ids_single_series(single_dataset):
    """verify no explicit identifiers for single-series data."""

    assert single_dataset.get_series_ids() == []

def test_get_series(multi_dataset):
    """Verify extraction of a single series."""

    series_a = multi_dataset.get_series("A")
    assert series_a["sales"].tolist() == [100, 120, 130, 150, 170, 160, 180, 200, 210, 220]

def test_get_series_invalid_identifier(multi_dataset):
    """Reject requests for unknown series."""

    with pytest.raises(ValueError, match="does not exist"):
        multi_dataset.get_series("UNKNOWN")

def test_get_series_without_identifiers(single_dataset):
    """Reject get_series when no series ID column is configured."""

    with pytest.raises(ValueError, match="requires a multi-series"):
        single_dataset.get_series("A")

def test_get_metadata(single_dataset):
    """Verify dataset metadata."""

    metadata = single_dataset.get_metadata()

    assert metadata["timestamp_col"] == "timestamp"
    assert metadata["target_col"] == "sales"
    assert metadata["frequency"] == "D"
    assert metadata["n_rows"] == 10
    assert metadata["n_series"] == 1
    assert metadata["is_multi_series"] is False

def test_len(single_dataset):
    """Verify the dataset length."""

    assert len(single_dataset) == 10

def test_repr(single_dataset):
    """Verify the dataset string representation."""

    representation = repr(single_dataset)

    assert "ForecastDataset" in representation
    assert "n_rows=10" in representation
    assert "frequency='D'" in representation 


# =======================================================================
# 10. Data Isolation
# =======================================================================

def test_input_dataframe_is_not_modified(single_series_data):
    """Verify construction does not mutate the input DataFrame. """

    original = single_series_data.copy(deep=True)

    ForecastDataset(
        data=single_series_data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    pd.testing.assert_frame_equal(single_series_data, original)


def test_data_property_returns_copy(single_dataset):
    """Verify callers cannot mutate internal data through .data."""

    external_data = single_dataset.data
    external_data.loc[0,"sales"] = 99999

    assert single_dataset.data.loc[0, "sales"] == 100

def test_get_target_returns_copy(single_dataset):
    """verify target extraction does not expose mutable internal state."""

    target = single_dataset.get_target()
    target.iloc[0] = 9999

    assert single_dataset.get_target().iloc[0] == 100

def test_get_series_return_copy(multi_dataset):
    """verify series extraction does not expose mutable internal state."""

    series_a = multi_dataset.get_series("A")
    series_a.loc[series_a.index[0], "sales"] = 99999

    assert multi_dataset.get_series("A")["sales"].iloc[0] == 100

# =======================================================================
# 11. Additional Edge Cases
# =======================================================================

def test_single_observation():
    """verify a single observation is accepted."""

    data = pd.DataFrame(
        {
            "timestamp": ["2026-01-01"],
            "sales": [100],  
        }
    )

    dataset = ForecastDataset(
        data=data,
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )

    assert dataset.n_rows == 1

def test_validate_can_be_called_again(single_dataset):
    """Verify explicit revalidation succeeds."""

    single_dataset.validate()

    assert single_dataset.n_rows == 10


def test_sort_returns_same_instance(single_dataset):
    """Verify sort() supports method chaining."""

    result = single_dataset.sort()

    assert result is single_dataset
