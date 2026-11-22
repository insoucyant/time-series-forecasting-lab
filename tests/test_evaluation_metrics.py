import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias,
)
    



def test_mae_known_values():
    y_true = pd.Series([3, -0.5, 2, 7])
    y_pred = pd.Series([2.5, 0.0, 2, 8])
    expected_mae = 0.5

    assert mean_absolute_error(y_true, y_pred) == pytest.approx(expected_mae, rel=1e-9)

def test_mae_perfect_prediction():
    y_true = pd.Series([1, 2, 3])
    y_pred = pd.Series([1, 2, 3])
    expected_mae = 0.0

    assert mean_absolute_error(y_true, y_pred) == pytest.approx(expected_mae, rel=1e-9)


def test_mae_rejects_different_lengths():
    y_true = pd.Series([1, 2, 3])
    y_pred = pd.Series([1, 2, 3, 4])
    with pytest.raises(ValueError, match="Actual and predicted values must have the same length."):
        mean_absolute_error(y_true, y_pred)

def test_mae_rejects_empty_series():
    y_true = pd.Series([])
    y_pred = pd.Series([])
    with pytest.raises(ValueError, match="Cannot calculate MAE for empty series."):
        mean_absolute_error(y_true, y_pred)



def test_mse_known_values():
    y_true = pd.Series([3, -0.5, 2, 7])
    y_pred = pd.Series([2.5, 0.0, 2, 8])
    expected_mse = 0.375
    assert mean_squared_error(y_true, y_pred) == pytest.approx(expected_mse, rel=1e-9)
