import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.metrics import mean_absolute_error

def test_mae_known_values():
    y_true = pd.Series([3, -0.5, 2, 7])
    y_pred = pd.Series([2.5, 0.0, 2, 8])
    expected_mae = 0.5

    assert mean_absolute_error(y_true, y_pred) == pytest.approx(expected_mae, rel=1e-9)

    