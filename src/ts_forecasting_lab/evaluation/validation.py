"""Structural validation of backtesting forecast records."""

from numbers import Integral
import pandas as pd

def validate_forecast_structure(
        forecasts: pd.DataFrame,
) -> None:
    """Validaet the structure of a single backtesting run."""
    
    required_columns= [
        "run_id",
        "model_id",
        "series_id",
        "fold_id",
        "horizon",
        "forecast_origin",
        "target_timestamp",
    ]

    missing = set(required_columns) - set(forecasts.columns)
    if missing:
        raise ValueError(
            f"Forecasts are missing required columns: {sorted(missing)}"
        )

    if forecasts.empty:
        raise ValueError("Cannot validate empty forecasts.")

    # Reject missing structural values.
    for column in required_columns:
        if forecasts[column].isna().any():
            raise ValueError(
                f"Missing values in {column}."
            )

    # Validate positive integer identifiers
    for column in ["fold_id", "horizon"]:
        valid = forecasts[column].map(
            lambda value: (
                isinstance(value, Integral)
                and not isinstance(value, bool)
                and value > 0
            )
        )
        if not vaid.all():
            raise ValueError(
                f"{column} must contain positive integers."
            )

    # Validate experiment identifiers
    for column in ["run_id", "model_id", "series_id"]:
        valid = forecasts[column].map(
            lambda value: (
                isinstance(value, str)
                and bool(value.strip())
            )
        )

        if not valid.all():
            raise ValueError(
                f"Invalid identifier in {column}."
            )
    # Evaluate only one run and one model at a time


    # Reject duplicate forecast observations
    forecast_key = [
        "run_id",
        "model_id",
        "series_id",
        "fold_id",
        "horizon",
    ]

    if forecasts.duplicated(subset=forecast_key).any():
        raise ValueError("Duplicate forecast records found.")
