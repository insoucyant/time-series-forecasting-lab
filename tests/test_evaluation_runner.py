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