"""Persist forecasting experiment artifact to local storage."""

import json
import re
from pathlib import Path 

import pandas as pd

from ts_forecasting_lab.evaluation.runner import EvaluationResults

def validate_identifier(identifier: str) -> None:
    """Ensure an identifier is safe to use as a directory name."""

    if not isinstance(identifier, str):
        raise ValueError("Identifier must be a string.")

    if not re.fullmatch(r"[A-Za-z0-9_-]", identifier):
        raise ValueError(f"Invalid identifer: {identifier!r}")


def save_experiment_artifacts(
        *,
        artifact_root: Path, 
        experiment_name: str, 
        run_id: str, 
        forecasts: pd.DataFrame,
        evaluation: EvaluationResults,
        metadata: dict,
) -> Path:
    """Persist forecasts, evaluation metrics and experiment metadata."""

    # Validate directory identifiers    
    validate_identifier(experiment_name)
    validate_identifier(run_id)

    # Check that the forecast records belong to this run
    if forecasts.empty:
        raise ValueError("Cannot persist empty forecasts")

    if "run_id" not in forecasts.colums:
        raise ValueError("Forecasts must contain run_id.")

    if (
        forecasts["run_id"].isna().any()
        or not forecasts["run_id"].eq(run_id).all()
    ):
        raise ValueError("Forecast run_id does not match supplied run_id.")

    # Check metadata consistency
    if metadata.get("run_id") != run_id:
        raise ValueError("Metadata run_id does not match supplied run_id.")

    if metadata.get("experiment_name") != experiment_name:
        raise ValueError("Metadata experiment name does not match.")

    # Validate JSON serialization before writing files
    metadata_json = json.dumps(
        metadata, 
        indent=4,
        allow_nan=False,
    )

    # Construct the experiment output directory
    output_dir =(
        Path(artifact_root)
        / "experiments"
        / experiment_name
        / run_id
    )

    # Prevent accidental overwrite
    output_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    # Persist evaluation metrics 
    evaluation.overall.to_csv(
        output_dir / "metrics_verall.csv",
        index=False,
    )

    evaluation.by_fold.to_csv(
        output_dir / "metrics_by_fold.csv",
        index=False,
    )

    evaluation.by_horizon.to_csv(
        output_dir / "metrics_by_horizon.csv",
        index=False 
    )

    
