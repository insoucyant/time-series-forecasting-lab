"""
Deterministic chronological fold generation for backtesting.

This module generates fold boundaries only. It does not fit models, produce forecasts, 
or calculate evaluation metrics.
"""

from __future__ import annotations 

from dataclasses import dataclass 
from typing import Literal

import pandas as pd

from ts_forecasting_lab.data.dataset import ForecastDataset


@dataclass(frozen=True)
class BacktestConfig:
    """Configuration for complete-horizon, single-series temporal splits.
    
    All sizes are counts of observations on the dataset's validated frequency.
    ``gap`` excludes observations after the training cutoff. Horizon positions are measured from 
    the forecast origin, so the first evaluated position is ``gap + 1``. 
    """

    strategy: Literal["expanding", "sliding"]
    initial_train_size: int
    horizon: int
    step: int = 1
    gap: int = 0
    window_size: int | None = None

    def __post_init__(self) -> None:
        if self.strategy not in {"expanding", "sliding"}:
            raise ValueError("strategy must be 'expanding' or 'siliding'. ")
        for name in ("initial_train_size", "horizon", "step"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer.")
        if isinstance(self.gap, bool) or not isinstance(self.gap, int) or self.gap < 0:
            raise ValueError("gap must be a non-negative integer.")
        if self.strategy == "sliding":
            if (isinstance(self.window_size, bool)
                or not isinstance(self.window_size, int)
                or self.window_size <= 0):
                raise ValueError("sliding strategy requires positive window_size.")
            if self.window_size != self.initial_train_size:
                raise ValueError(
                    "For the initial sliding implementation, window_size must"
                    "equal to the initial_train_size."
                )
        elif self.window_size is not None:
            raise ValueError("window_size is only valid for sliding strategy.")



@dataclass(frozen=True) 
class BacktestFold:
    """Half-open positional slices and timestamp metadata for one fold."""

    fold_id: int 
    train_start: int
    train_end: int 
    test_start: int 
    test_end: int 
    forecast_origin: pd.Timestamp 
    target_timestamps: tuple[pd.Timestamp, ...]
    evaluated_horizons: tuple[int, ...]

    @property
    def train_slice(self) -> slice:
        return slice(self.train_start, self.train_end)

    @property
    def test_slice(self) -> slice:
        return slice(self.test_start, self.test_end)


def generate_folds(
        dataset: ForecastDataset,
        config: BacktestConfig,
) -> list[BacktestFold]:
    """Return chronological, non-leaking folds for a validated single series.
     The dataset must have a complete regular calendar, as enforced by 
     ``ForecastDataset.validate()``. Mult-series splitting and partial folds
     are intentionally deferred to later implementation stages.
    """

    if not isinstance(dataset, ForecastDataset):
        raise TypeError("dataset must be a ForecastDataset.")

    if not isinstance(config, BacktestConfig):
        raise TypeError("config must be a BacktestConfig.")

    if dataset.is_multi_series:
        raise NotImplementedError("Multi-series backtesting is not yet supported.")

    # Revalidate before using positional counts as frequency periods.
    dataset.validate()
    frame = dataset.data.sort_values(dataset.timestamp_col).reset_index(drop=True)
    timestamps = pd.DatetimeIndex(frame[dataset.timestamp_col])
    n = len(frame)
    if n < config.initial_train_size + config.gap + config.horizon:
        raise ValueError("Not enough observations for one complete backtesting fold.")

    folds: list[BacktestFold] = []
    train_end = config.initial_train_size
    while train_end + config.gap + config.horizon <= n:
        train_start = 0 if config.strategy == "expanding" else train_end - config.window_size
        test_start = train_end + config.gap
        test_end = test_start + config.horizon
        folds.append(
            BacktestFold( 
                fold_id = len(folds) + 1,
                train_start = train_start,
                train_end = train_end,
                test_start = test_start,
                test_end = test_end,
                forecast_origin=timestamps[train_end - 1],
                target_timestamps=tuple(timestamps[test_start:test_end]),
                evaluated_horizons=tuple(range(config.gap + 1, config.gap + config.horizon + 1)),
            )
        )
        train_end += config.step
    return folds 
    
