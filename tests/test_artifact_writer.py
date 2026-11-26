"""Tests for experiment artifact persistence."""

import jason
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

    