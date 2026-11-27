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

def test_save_experiment_artifacts(
        tmp_path,
        sample_forecasts,
        sample_evaluation,
        sample_metadata,
):
    output_dir = save_experiment_artifacts(
        artifact_root=tmp_path,
        experiment_name="experiment_01",
        run_id="run_01",
        forecasts=sample_forecasts,
        evaluation=sample_evaluation,
        metadata=sample_metadata,
    )

    expected_dir = (
        tmp_path
        / "experiments"
        / "experiment_01"
        / "run_01"
    )

    assert output_dir == expected_dir
    assert output_dir.is_dir()

    expected_files = {
        "forecasts.csv",
        "metrics_overall.csv",
        "metrics_by_fold.csv",
        "metrics_by_horizon.csv",
        "metadata.json",
    }

    actual_files = {
        file.name for file in output_dir.iterdir()
    }

    assert actual_files == expected_files



def test_saved_artifact_contents(
        tmp_path,
        sample_forecasts,
        sample_evaluation,
        sample_metadata,
):
    output_dir = save_experiment_artifacts(
        artifact_root=tmp_path,
        experiment_name="experiment_01",
        run_id="run_01",
        forecasts=sample_forecasts,
        evaluation=sample_evaluation,
        metadata=sample_metadata,
    )

    # Verify forecast records
    saved_forecasts = pd.read_csv(
        output_dir / "forecasts.csv"
    )

    pd.testing.assert_frame_equal(
        saved_forecasts,
        sample_forecasts,
    )

    # Verify all evaluation tables
    for filename, expected in [
        ("metrics_overall.csv", sample_evaluation.overall),
        ("metrics_by_fold.csv", sample_evaluation.by_fold),
        ("metrics_by_horizon.csv", sample_evaluation.by_horizon),
    ]:
        saved_metrics = pd.read_csv(output_dir / filename)

        pd.testing.assert_frame_equal(
            saved_metrics,
            expected,
        )

    # Verify metadata
    saved_metadata = json.loads(
        (output_dir / "metadata.json").read_text(
            encoding="utf-8"
        )
    )

    assert saved_metadata == sample_metadata


    def test_duplicate_run_id_rejected(
            tmp_path,
            sample_forecasts,
            sample_evaluation,
            sample_metadata,
    ):
        kwargs = {
            "artifact_root": tmp_path,
            "experiment_name": "experiment_01",
            "run_id": "run_01",
            "forecasts": sample_forecasts,
            "evaluation": sample_evaluation,
            "metadata": sample_metadata,
        }

        # First execution should succeed 
        output_dir = save_experiment_artifacts(**kwargs)

        # Capture original artifact contents
        original_files = {
            file.name: file.read_bytes()
            for file in output_dir.iterdir()
        }

        # Second execution should fail
        with pytest.raises(FileExistsError):
            save_experiment_artifacts(**kwargs)

        # Verify that original artifacts remain unchanged
        current_files = {
            file.name: file.read_bytes()
            for file in output_dir.iterdir()
        }

        assert current_files == original_files


@pytest.mark.parametrize(
    "scenarion_expected_error",
    [
        ("empty", "Cannot persist empty forecasts"),
        ("missing_run_id", "Forecasts must contain run_id"),
        ("incorrect_run_id", "Forecast run_id does not match"),
        ("mixed_run_ids", "Forecast run_id does not match"),
        ("null_run_id", "Foreast run_id does not match"),
    ],
)
def test_invalid_forecasts_rejectd(
    tmp_path,
    sample_forecasts,
    sample_evaluation,
    sample_metadata,
    scenario,
    expected_error,
):
    forecasts = sample_forecasts.copy()

    if scenario == "empty":
        forecasts = forecasts.iloc[0:0]

    elif scenario == "missing_run_id":
        forecasts = forecasts.drop(columns=["run_id"])

    elif scenario == "incorrect_run_id":
        forecasts["run_id"] = "wrong_run"

    elif scenario == "null_run_id":
        forecasts.loc[0, "run_id"] = None 

    with pytest.raises(ValueError, match=expected_error):
        save_experiment_artifacts(
            artifact_root=tmp_path,
            experiment_name="experiment_01",
            run_id="run_01",
            forecasts=forecasts,
            evaluation=sample_evaluation,
            metadata=sample_metadata,
        ) 

    assert not (tmp_path / "experiments").exists()



@pytest.mark.parametrize(
    "field, invalid_value, expected_error",
    [
        (
            "run_id",
            "wrong_run",
            "Metadata run_id does not match",
        ),
        (
            "experiment_name",
            "wrong_experiment",
            "Metadata experiment name does not match",
        ),
    ],
)
def test_inconsistent_metadata_rejected(
    tmp_path,
    sample_forecasts,
    sample_evaluation,
    sample_metadata,
    field,
    invalid_value,
    expected_error,
):
    metadata = sample_metadata.copy()
    metadata[field] = invalid_value

    with pytest.raises(ValueError, match=expected_error):
        save_experiment_artifacts(
            artifact_root=tmp_path,
            experiment_name="experiment_01",
            run_id="run_01",
            forecasts=sample_forecasts,
            evaluation=sample_evaluation,
            metadata=metadata,
        )

    assert not (tmp_path / "experiments").exists()