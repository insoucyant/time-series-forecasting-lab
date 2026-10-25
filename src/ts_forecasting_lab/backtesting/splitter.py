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

    startegy: Literal["expanding", "sliding"]
    initial_train_size: int
    horizon: int
    step: int = 1
    gap: int = 0
    window_size: int | None = None

    def __post_init__(self) -> None:
        if self.startegy not in {"expanding", "sliding"}:
            raise ValueError("strategy must be 'expanding' or 'siliding'. ")
        for name in ("initial_train_size", "horizon", "step"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer.")
        if isinstance(self.gap, bool) or not isinstance(self.gap, int) or self.gap < 0:
            raise ValueError("gap must be a non-negative integer.")
        if self.startegy == "sliding":
            