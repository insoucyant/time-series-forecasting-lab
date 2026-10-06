""" Core dataset abstraction for the forecasting platform."""


from __future__ import annotations

from typing import Any

import pandas as pd

class ForecastDataset:
    """
    Standard dataset representation used by the forecasting platform.

    Forecast dataset provides a consistent and validated interface between raw time-series data
    and downstream platfrom components such as feature engineering, forecasting model, 
    backtesting, and evaluation. 

    The initial implementation supports both single-series and multi-series forecasting datasets.

    Parameters
    ----------
    data:
        Input time-series data.

    timestamp_col:
        Name of the column containing timestamps.

    target_col:
        Name of the column containing target values.

    frequency:
        Frequency of the time-series data. Pandas compatible frequency string
        (e.g., 'D' for daily, 'H' for hourly, 'h' for hourly, 'W' for weekly, or 'MS' for monthly)
    
    series_id_col:
        Name of the column containing series identifiers. 
        This is optional and can be None for single-series datasets.

    validate:
        Whether to validate the input data upon initialization. If True, the dataset will be validated
        for consistency and correctness. If False, validation will be skipped.
    """

    def __init__(
        self, 
        data: pd.DataFrame,
        timestamp_col: str,
        taregt_col: str,
        frequency: str, 
        series_id_col: str | None = None, 
        validate: bool = True
    ) -> None: