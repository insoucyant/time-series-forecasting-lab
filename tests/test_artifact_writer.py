"""Tests for experiment artifact persistence."""

import json
import pandas as pd
import pytest 

from ts_forecasting_lab.evaluation.runner import EvaluationResults
from ts_forecasting_lab.tracking.artifact_writer import (
    validate_identifier,
    save_experiment_artifacts,
)

@pytest.mark.parametrize(
    "identifier",
    [
        "experiment_01",
        "run-123",
        "ABC",
        "abc",
        "123",
        "run_01-test",
        "035c903036e541fb833f221aec650230",
    ],
)
def test_valid_identifier(identifier):
    validate_identifier(identifier)

@pytest.mark.parametrize(
    "identifier",
    [
        "",
        " ",
        "../outside",
        "..",
        "experiment/test",
        "experiment\\test",
        "experiment 01",
        "experiment.01",
        "C:\\temp",
        None,
        123,
    ],
)
def test_invalid_identifier(identifier):
    with pytest.raises(ValueError):
        validate_identifier(identifier)




@pytest.fixture
def sample_forecasts():
    return pd.DataFrame(
        {
            "run_id": ["run_01"] * 3, 
            "model_id": ["seasonal_naive"] * 3,
            "series_id": ["series_01"] * 3, 
            "fold_id": [1, 1, 1],
            "forecast_origin": ["2026-01-01"] * 3, 
            "target_timestamp": [
                "2026-01-11",
                "2026-01-12",
                "2026-01-13",
            ],
            "horizon": [1, 2, 3],
            "y_true": [10.0, 11.0, 12.0],
            "y_pred": [9.0, 9.0, 9.0],
            "fit_status": ["success"] * 3,
            "predict_status": ["success"] * 3,
        }
    )


@pytest.fixture
def sample_evaluation():
    return EvaluationResults(
        overall=pd.DataFrame(
            {
                "mae": [2.0],
                "mse": [14 / 3],
                "rmse": [(14 / 3) ** 0.5],
                "bias": [-2.0],
            }
        ),
        by_fold=pd.DataFrame(
            {
                "fold_id": [1],
                "mae": [2.0],
            }
        ),
        by_horizon=pd.DataFrame(
            {
                "horizon": [1, 2, 3],
                "mae": [1.0, 2.0, 3.0]
            }
        ),
    )

@pytest.fixture
def sample_metadata():
    return {
        "experiment_name": "experiment_01",
        "run_id": "run_01",
        "model": {
            "model_id": "seasonal_naive",
            "parameters": {
                "seasonal_length": 1,
            },
        },
    }