"""Point forecast evaluation metrics."""

import pandas as pd

def mean_absolute_error(
        y_true: pd.Series,
        y_pred: pd.Series,
) -> float:
    """Calculate the Mean Absolute Error."""
    if len(y_true) != len(y_pred):
        raise ValueError(
            "Actual and predicted values must have the same length."
        )

    if len(y_true) == 0:
        raise ValueError("Cannot calculate MAE for empty series.")

    errors = y_true.to_numpy() - y_pred.to_numpy()
    mae = abs(errors).mean()
    return mae 

def mean_squared_error(
        y_true: pd.Series,
        y_pred: pd.Series,
) -> float:
    """Calculate the Mean Squared Error."""
    if len(y_true) != len(y_pred):
        raise ValueError("Actual and predicted values must have the same length.")

    if len(y_true) == 0:
        raise ValueError("Cannot calculate MSE for empty series.")

    errors = y_true.to_numpy() - y_pred.to_numpy()
    mse = float((errors ** 2).mean())
    return mse 

def root_mean_squared_error(
        y_true: pd.Series,
        y_pred: pd.Series,
) -> float:
    """Calculate the Root Mean Squared Error."""
    return mean_squared_error(y_true, y_pred) ** 0.5

def mean_bias(
        y_true: pd.Series,
        y_pred: pd.Series,
) -> float:
    """Calculate the Mean Forecast Bias (predicted minus actual)."""
    if len(y_true) != len(y_pred):
        raise ValueError("Actual and predicted values must have the same length.")

    if len(y_true) == 0:
        raise ValueError("Cannot calculate mean bias for empty series.")

    errors = y_pred.to_numpy() - y_true.to_numpy()
    bias = float(errors.mean())
    return bias
    