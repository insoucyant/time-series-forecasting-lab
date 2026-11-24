import numpy as np
import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.runner import evaluate_forecasts

@pytest.fixture
def valid_forecasts():
    return pd.DataFrame({
        "fold_id": [1, 1, 1],
        "horizon": [1, 2, 3],
        "y_true": [10.0, 11.0, 12.0],
        "y_pred": [9.0, 9.0, 9.0],
        "fit_status": ["success"] * 3,
        "predict_status": ["success"] * 3,
    })

@pytest.mark.parametrize("column", ["y_true", "y_pred"])
@pytest.mark.parametrize("invalid", [np.inf, -np.inf])
def test_rejects_infinite_forecast_values(valid_forecasts, column, invalid):
    forecasts = valid_forecasts.copy()
    forecasts.loc[0, column] = invalid

    with pytest.raises(ValueError, match="non-finite"):
        evaluate_forecasts(forecasts)

@pytest.mark.parametrize("column", ["y_true", "y_pred"])
def test_rejects_non_numeric_forecast_values(valid_forecasts, column):
    forecasts = valid_forecasts.copy()
    forecasts[column] = forecasts[column].astype(object)
    forecasts.loc[0, column] = "not-a-number"

    with pytest.raises(ValueError, match="numeric"):
        evaluate_forecasts(forecasts)

def test_valid_forecasts_still_evaluate(valid_forecasts):
    evaluation = evaluate_forecasts(valid_forecasts)
    assert evaluation.overall.loc[0, "mae"] == pytest.approx(2.0)