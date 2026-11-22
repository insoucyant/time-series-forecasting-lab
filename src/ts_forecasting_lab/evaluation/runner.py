"""Evaluate forecasts produced by the backtesting runner using various metrics."""

from dataclasses import dataclass
import pandas as pd

from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias,
)

@dataclass
class EvaluationResults:
    overall: pd.DataFrame
    by_fold: pd.DataFrame
    by_horizon: pd.DataFrame


def calculate_metrics(forecasts: pd.DataFrame) -> dict:
    """Calculate evaluation metrics for a set of forecast observations."""

    actual = forecasts["y_true"]
    predicted = forecasts["y_pred"]

    return {
        "mae": mean_absolute_error(actual, predicted),
        "mse": mean_squared_error(actual, predicted),
        "rmse": root_mean_squared_error(actual, predicted),
        "bias": mean_bias(actual, predicted),   
    }