"""Tests for the reusuable forecasting evaluation runner."""

import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.runner import evaluate_forecasts

@pytest.fixture
def valid_forecasts():
    """Three folds, each containing three forecast horizons."""
    rows = []
    for fold_id, actuals, prediction in [
        (1, [10, 11, 12], 9),
        (2, [13, 14, 15], 12),
        (3, [16, 17, 18], 15), 
    ]:
        for horizon, actual in enumerate(actuals, start=1):
            rows.append({
                "fold_id": fold_id,
                "horizon": horizon, 
                "y_true": actual,
                "y_pred": prediction, 
                "fit_status": "success",
                "predict_status": "success",
            })
    return pd.DataFrame(rows)

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
    with pytest.raises(ValueError, match="Missing required columns"):
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

