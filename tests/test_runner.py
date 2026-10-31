"""
    Tests for single-series backtesting execution and alignment.
"""

import pandas as pd
import pytest

from ts_forecasting_lab.backtesting.runner import run_backtest, RESULT_COLUMNS
from ts_forecasting_lab.backtesting.splitter import BacktestConfig
from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_lab.models.statistical.naive import SeasonalNaiveForecaster

def make_dataset(n=20):
    return ForecastDataset(
        pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=n, freq="D"),
                "sales": list(range(n))
            }
        ),
        timestamp_col="date", target_col="sales", frequency="D",
    )