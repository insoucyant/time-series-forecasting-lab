"""Unit test for chronological backtesting fold generation"""

import pandas as pd
import pytest 

from ts_forecasting_lab.backtesting.splitter import (
    BacktestConfig,
    generate_folds
)
from ts_forecasting_lab.data.dataset import ForecastDataset


def make_dataset(n: int = 20) -> ForecastDataset:
    return ForecastDataset(
        data = pd.DataFrame({
            "timestamp": pd.date_range("2026-01-01", periods=n, freq="D"),
            "sales": list(range(n)),
        }), 
        timestamp_col="timestamp",
        target_col="sales",
        frequency="D",
    )