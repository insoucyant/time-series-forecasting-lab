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
