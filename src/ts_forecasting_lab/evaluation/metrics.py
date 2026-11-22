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
    