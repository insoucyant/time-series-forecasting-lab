import pandas as pd
import pytest 

from ts_forecasting_lab.data.dataset import ForecastDataset
from ts_forecasting_models.statistical.naive import SeasonalNaiveForecaster
from ts_forecasting_lab.backtesting.splitter import BacktestConfig 
from ts_forecasting_lab.backtesting.runner import run_backtest 
from ts_forecasting_lab.evaluation.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_bias, 
)


def test_backtesting_evaluation_integration():
    data = pd.DataFrame({
        "date": pd.date_range(start-"2026-01-01", periods=20, freq="D"),
        "sales": list(range(20)),
    })

    dataset = ForecastDataset(
        data=data,
        timestamp_col="date",
        target_col="sales",
        frequency="D",
    )

    config = BacktestConfig(
        strategy="expanding",
        initial_train_size=10,
        horizon=3,
        step=3,
        gap=0,
    )

    results = run_backtest(
        dataset=dataset,
        config=config,
        model_factory=lambda: SeasonalNaiveForecaster(season_length=1),
        run_id="integration_test",
    )

    assert len(results) == 9, "Expected 9 forecast observations for the given configuration."
    assert results["fold_id"].nunique() == 3, "Expected 3 folds for the given configuration."

    actual = results["y_true"]
    predicted = results["y_pred"]

    assert mean_absolute_error(actual, predicted) == pytest.approx(0.5, rel=1e-9)
    assert mean_squared_error(actual, predicted) == pytest.approx(0.375, rel=1e-9)
    assert root_mean_squared_error(actual, predicted) == pytest.approx(0.6123724356957945, rel=1e-9)
    assert mean_bias(actual, predicted) == pytest.approx(0.0, rel=1e-9)
