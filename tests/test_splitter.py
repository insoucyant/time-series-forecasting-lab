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

def test_half_open_slices_select_expected_rows():
    ds = make_dataset()
    fold = generate_folds(ds, BacktestConfig("expanding", 10, 3))[0]
    frame = ds.data
    assert frame.iloc[fold.train_slice]["sales"].tolist() == list(range(10))
    assert frame.iloc[fold.test_slice]["sales"].tolist() == [10, 11, 12]

def test_no_temporal_overlap():
    folds = generate_folds(make_dataset(), BacktestConfig("expanding", 8, 4, step=2))
    assert all(f.train_end <= f.test_start for f in folds)
    assert all(f.forecast_origin < f.target_timestamps[0] for f in folds)

def test_partial_final_fold_is_not_generated():
    folds = generate_folds(make_dataset(15), BacktestConfig("expanding", 10, 4, step=2))
    assert len(folds) == 1
    assert folds[0].test_end == 14

def test_exactly_one_fold():
    assert len(generate_folds(make_dataset(13), BacktestConfig("expanding", 10, 3))) == 1

def test_insufficient_observations():
    with pytest.raises(ValueError, match="Not enough observations"):
        generate_folds(make_dataset(12), BacktestConfig("expanding", 10, 3))

@pytest.mark.parametrize("kwargs", [
    {"initial_train_size": 0}, {"horizon": 0}, {"step": 0},
    {"gap": -1}, {"initial_train_size": True}
])
def test_invalid_numeric_configuration(kwargs):
    args = {"strategy": "expanding", "initial_train_size": 10, "horizon": 3}
    args.update(kwargs)
    with pytest.raises(ValueError):
        BacktestConfig(**args)

def test_invalid_strategy():
    with pytest.raises(ValueError, match="strategy"):
        BacktestConfig("unknown", 10, 3)

def test_sliding_requires_window_size():
    with pytest.raises(ValueError, match="window_size"):
        BacktestConfig("sliding", 10, 3)

def test_sliding_window_must_equal_initial_train_size():
    with pytest.raises(ValueError, match="equal initial train size"):
        BacktestConfig("sliding", 10, 3, window_size=8)

def test_expanding_rejects_window_size():
    with pytest.raises(ValueError, match="only valid"):
        BacktestConfig("expanding", 10, 3, window_size=10)


def test_multi_series_is_explicitly_unsupported():
    frame = pd.DataFrame({
        "timestamp": list(pd.date_range("2026-01-01", periods=12, freq="D")) * 2,
        "sales": list(range(12)) * 2,
        "store_id": ["A"] * 12 + ["B"] * 12,
    })
    dataset = ForecastDataset(frame, "timestamp", "sales", "D", "store_id")
    with pytest.raises(NotImplementedError, match="Multi-series"):
        generate_folds(dataset, BacktestConfig("expanding", 8, 3))


def test_reproducible_fold_generation():
    ds = make_dataset()
    config = BacktestConfig("expanding", 10, 3, step=2)
    assert generate_folds(ds, config) == generate_folds(ds, config)


