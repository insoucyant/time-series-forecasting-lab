"""Unit tests for structural validation of forecast records."""

import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.validation import (
    validate_forecast_structure,
)

@pytest.fixture
def valid_forecasts():
    return pd.DataFrame({
        "run_id": ["run_01"] * 4,
        "model_id": ["naive"] * 4,
        "series_id": ["series_01"] * 4,
        "fold_id": [1, 1, 2, 2],
        "horizon": [1, 2, 1, 2],
        "forecast_origin": pd.to_datetime([
            "2026-01-10",
            "2026-01-10",
            "2026-01-11",
            "2026-01-11",
        ]),
        "target_timestamp": pd.to_datetime([
            "2026-01-11",
            "2026-01-12",
            "2026-01-12",
            "2026-01-13",
        ]) 
    })

def test_valid_forecast_structure(valid_forecasts):
    validate_forecast_structure(valid_forecasts)

def test_missing_required_column(valid_forecasts):
    invalid = valid_forecasts.drop(columns=["run_id"])

    with pytest.raises(ValueError, match="missing required columns"):
        validate_forecast_structure(invalid)

def test_empty_forecasts(valid_forecasts):
    invalid = valid_forecasts.iloc[0:0]

    with pytest.raises(ValueError, match="empty"):
        validate_forecast_structure(invalid)

@pytest.mark.parametrize(
    "column",
    ["fold_id", "horizon"],
)
@pytest.mark.parametrize(
    "value",
    [0, -1, 1.5, "2", True]
)
def test_invalid_positive_integer(
    valid_forecasts, column, value
):
    invalid = valid_forecasts.copy()
    invalid[column] = invalid[column].astype(object)
    invalid.loc[0, column] = value

    with pytest.raises(ValueError, match="positive integers"):
        validate_forecast_structure(invalid)

@pytest.mark.parametrize(
    "columns",
    [
        "run_id",
        "model_id",
        "series_id",
        "fold_id",
        "horizon",
        "forecast_origin",
        "target_timestamp",
    ],
)
def test_missing_structural_value(valid_forecasts, column):
    invalid = valid_forecasts.copy()
    invalid[column] = invalid[column].astype(object)
    invalid.loc[0, column] = None

    with pytest.raises(ValueError, match="Missing values"):
        validate_forecast_structure(invalid)

        



