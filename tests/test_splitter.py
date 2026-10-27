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

def test_expanding_window_boundaries():
    folds = generate_folds(
        make_dataset(), BacktestConfig("expanding", initial_train_size=10, horizon=3, step=3)
    )
    assert [(f.train_start, f.train_end, f.test_start, f.test_end) for f in folds] == [
        (0, 10, 10, 13), (0, 13, 13, 16), (0, 16, 16, 19)
    ]
    assert [f.fold_id for f in folds] == [1, 2, 3]

def test_sliding_window_boundaries():
    fold = generate_folds(
        make_dataset(), BacktestConfig("sliding", 10, 3, step=3, window_size=10)
    )
    assert [(f.train_start, f.train_end) for f in folds] == [
        (0,13), (3,13), (6,16)
    ]

def test_gap_and_horizon_convention():
    fold = generate_folds(make_dataset(), BacktestConfig("expanding", 10, 3, gap=2))[0]
    assert (fold.train_end, fold.test_start, fold.test_end) == (10, 12, 15)
    assert fold.evaluated_horizons == (3, 4, 5)
    assert fold.forecast_origin == pd.Timestamp("2026-01-10")
    assert fold.target_timestamps[0] == pd.Timestamp("2026-01-13")