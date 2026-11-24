"""Tests for the reusuable forecasting evaluation runner."""

import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.runner import evaluate_forecasts

@pytest.fixture
def valid_forecasts():
    return pd.DataFrame({
        "run_id": ["run_01"] * 9,
        "model_id": ["naive"] * 9,
        "series_id": ["series_01"] * 9,
        "fold_id": [1, 1, 1, 2, 2, 2, 3, 3, 3],
        "horizon": [1, 2, 3, 1, 2, 3, 1, 2, 3],
        "forecast_origin": pd.to_datetime(
            ["2026-01-10"] * 3
            + ["2026-01-13"] * 3
            + ["2026-01-16"] * 3
        ),
        "target_timestamp": pd.date_range(
            "2026-01-11", periods=9, freq="D"
        ),
        "y_true": [10, 11, 12, 13, 14, 15, 16, 17, 18],
        "y_pred": [9, 9, 9, 12, 12, 12, 15, 15, 15],
        "fit_status": ["success"] * 9,
        "predict_status": ["success"] * 9,
    })

def test_overall_metrics(valid_forecasts):
    result = evaluate_forecasts(valid_forecasts)
    assert len(result.overall) == 1
    metrics = result.overall.iloc[0]
    assert metrics["mae"] == pytest.approx(2.0)
    assert metrics["mse"] == pytest.approx(14/3)
    assert metrics["rmse"] == pytest.approx((14 / 3)**0.5)
    assert metrics["bias"] == pytest.approx(-2.0)

def test_metrics_by_fold(valid_forecasts):
    result = evaluate_forecasts(valid_forecasts)
    by_fold = result.by_fold.set_index("fold_id")
    assert set(by_fold.index) == {1, 2, 3}
    for fold_id in (1, 2, 3):
        assert by_fold.loc[fold_id, "mae"] == pytest.approx(2.0)
        assert by_fold.loc[fold_id, "bias"] == pytest.approx(-2.0)


def test_metrics_by_horizon(valid_forecasts):
    result = evaluate_forecasts(valid_forecasts)
    by_horizon = result.by_horizon.set_index("horizon")
    assert set(by_horizon.index) == {1, 2, 3}
    for horizon in (1, 2, 3):
        assert by_horizon.loc[horizon, "mae"] == pytest.approx(horizon)
        assert by_horizon.loc[horizon, "mse"] == pytest.approx(horizon ** 2)
        assert by_horizon.loc[horizon, "bias"] == pytest.approx(-horizon)

def test_missing_required_column(valid_forecasts):
    invalid = valid_forecasts.drop(columns=["y_pred"])
    with pytest.raises(ValueError, match="missing required columns"):
        evaluate_forecasts(invalid)

def test_empty_forecasts(valid_forecasts):
    with pytest.raises(ValueError, match="empty"):
        evaluate_forecasts(valid_forecasts.iloc[0:0])

@pytest.mark.parametrize("status_column", ["fit_status", "predict_status"])
def test_unsuccessful_model_runs(valid_forecasts, status_column):
    invalid = valid_forecasts.copy()
    invalid.loc[0, status_column] = "failed"
    with pytest.raises(ValueError, match="unsuccessful"):
        evaluate_forecasts(invalid)

@pytest.mark.parametrize("value_column", ["y_true", "y_pred"])
def test_missing_forecast_values(valid_forecasts, value_column):
    invalid = valid_forecasts.copy()
    invalid.loc[0, value_column] = float("nan")
    with pytest.raises(ValueError, match="missing"):
        evaluate_forecasts(invalid)