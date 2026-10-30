"""
Single-series backtesting execution; evaluation metrics live elsewhere.
"""

from __future__ import annotations

from collections.abc import Callable
from uuid import uuid4 

import pandas as pd

from ts_forecasting_lab.backtesting.splitter import BacktestConfig, generate_folds
from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.base import BaseForecaster, ForecastResult


RESULT_COLUMNS = [
    "run_id", "model_id", "series_id", "fold_id", "forecast_origin", 
    "target_timestamp", "horizon", "y_true", "y_pred",
    "fit_status", "predict_status",
]