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

def factory():
    return SeasonalNaiveForecaster(season_length=1)

def test_result_contract_and_fold_count():
    result = run_backtest(
        make_dataset(), 
        BacktestConfig("expanding", 10, 3, step=3),
        factory,
        run_id="demo"
    )
    assert list(result.columns) == RESULT_COLUMNS
    assert len(result) == 9
    assert result.fold_id.tolist() == [1] * 3 + [2] * 3 + [3] * 3
    assert result.run_id.eq("demo").all()
    assert result.fit_status.eq("success").all()