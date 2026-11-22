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


