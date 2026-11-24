import numpy as np
import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.runner import evaluate_forecasts

@pytest.fixture
def valid_forecasts():
    return pd.DataFrame({
        "fold_id": [1, 1, 1]
        "horizon": [1, 2, 3]
        "y_true": [10.0, 11.0, 12.0],
        "y_pred": [9.0, 9.0, 9.0]
        "fit_status": ["success"] * 3
        "predict_status": ["success"] * 3
    })

