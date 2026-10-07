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
        target_col: str,
        frequency: str, 
        series_id_col: str | None = None, 
        validate: bool = True
    ) -> None:
        self._data = data.copy()

        self.timestamp_col = timestamp_col
        self.target_col = target_col
        self.frequency = frequency
        self.series_id_col = series_id_col

        if validate:
            self.validate()

        self.sort()

    @property
    def data(self) -> pd.DataFrame:
        """Return the underlying dataset as a pandas DataFrame."""
        return self._data.copy()


    @property
    def is_multi_series(self) -> bool:
        """Check if the dataset is a multi-series dataset."""
        return self.series_id_col is not None

    @property
    def n_rows(self) -> int:
        """Return the number of observations in the dataset."""
        return len(self._data)

    @property
    def n_series(self) -> int:
        """Return the number of unique series in the dataset."""
        if self.series_id_col is None:
            return 1

        return self._data[self.series_id_col].nunique()

    def validate(self) -> None:
        """
        Validate the dataset contract.

        Validation checks:

        - input data is a pandas DataFrame
        - dataset is not empty
        - required columns exist
        - timestamp column can be represented as datetime
        - timestamps do not contain missing values
        - target does not contain missing values
        - series identifiers do not contain missing values
        - timestamp keys are unique within each series (if multi-series)
        - declared frequency is valid
        - timestamps conform to the declared frequency 

        Raises
        ------
        TypeError
            If the input data is not a pandas DataFrame.

        ValueError
            If the dataset violates dataset contract rules, 
            such as non-unique timestamps within a series or 
            timestamps not conforming to the declared frequency, a ValueError will be raised.
        """

        self._validate_dataframe()
        self._validate_non_empty()
        self._validate_required_columns()
        self._convert_timestamp()
        self._validate_timestamps()
        self._validate_target()
        self._validate_series_id()
        self._validate_duplicates()
        self._validate_frequency()

    def sort(self) -> ForecastDataset:
        """
        Sort observations chronologically.

        Multi-Series datasets are sorted forst by series identifier and then by timestamp. 

        Returns
        -------
        ForecastDataset
            The current ForecastDataset instance with sorted data.
        """

        sort_columns: list[str] = []

        if self.series_id_col is not None:
            sort_columns.append(self.series_id_col)

        sort_columns.append(self.timestamp_col)

        self._data = (
            self._data
            .sort_values(by=sort_columns)
            .reset_index(drop=True) 
        )

        return self 

    def get_target(self) -> pd.Series:
        """
        Return the target Series.

        Returns
        -------
        pandas.Series
            Copy of the target column from the dataset.
        """ 

        return self._data[self.target_col].copy()

    def get_series_ids(self) -> list[Any]:
        """ 
        Return the unique series identifiers.

        For a single-series dataset, an empty list is returned because no explicit 
        series identifiers are present.

        Returns
        -------
        list[Any]
            Unique series identifiers. 
        """

        if self.series_id_col is None: 
            return []

        return self._data[self.series_id_col].drop_duplicates().sort_values().tolist()

    def get_series(self, series_id: Any) -> pd.DataFrame:
        """
        Return observations belonging to one time series. 

        Parameters
        ----------
        series_id:
            The identifier of the time series to retrieve.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing observations for the specified time series.

        Raises
        ------
        ValueError
            If the dataset has no series identifier column or 
            the requested identifier does not exist in the dataset.
        """ 

        if self.series_id_col is None:
            raise ValueError("The dataset has no series identifier column.")

        mask = self._data[self.series_id_col] == series_id

        if not mask.any():
            raise ValueError(f"Series identifier '{series_id}' does not exist in the dataset.")

        return self._data.loc[mask].copy()

    def get_metadata(self) -> dict[str, Any]:
        """
        Return basic metadata describing the dataset.

        Returns
        -------
        dict[str, Any]
            A dictionary containing metadata about the dataset, including:
            - number of rows
            - number of unique series
            - timestamp column name
            - target column name
            - frequency
            - series identifier column name (if applicable)
        """

        return {
            "timestamp_col": self.timestamp_col,
            "target_col": self.target_col,
            "series_id_col": self.series_id_col,
            "frequency": self.frequency,
            "n_rows": self.n_rows,
            "n_series": self.n_series,
            "is_multi_series": self.is_multi_series,
        }

    def _validate_dataframe(self) -> None:
        """Validate that the dataset contains observations."""

        if not isinstance(self._data, pd.DataFrame):
            raise TypeError("Input data must be a pandas DataFrame.")

    
    def _validate_non_empty(self) -> None:
        """Validate that the dataset is not empty."""

        if self._data.empty:
            raise ValueError("The dataset is empty. Please provide a non empty dataset.")

    def _validate_required_columns(self) -> None:
        """Validate that the required columns exist in the dataset."""
        
        required_columns = {self.timestamp_col, self.target_col}

        if self.series_id_col is not None:
            required_columns.add(self.series_id_col)

        missing_columns = required_columns - set(self._data.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))

            raise ValueError(
                f"The following required columns are missing from the dataset: {missing}"
            )

    def _convert_timestamp(self) -> None:
        """Convert the timestamp column to datetime format.""" 

        try:
            self._data[self.timestamp_col] = pd.to_datetime(
                self._data[self.timestamp_col],
                errors="raise"
            )
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Failed to convert the timestamp column '{self.timestamp_col}' to datetime. "
                f"Ensure that the column contains valid datetime values."
            ) from exc

    def _validate_timestamps(self) -> None:
        """Validate that the timestamp column does not contain missing values."""

        if self._data[self.timestamp_col].isna().any():
            raise ValueError(
                f"The timestamp column '{self.timestamp_col!r}' contains missing values."
                )

    def _validate_target(self) -> None:
        """Validate that the target column does not contain missing values."""
        
        if self._data[self.target_col].isna().any():
            raise ValueError(
                f"The target column '{self.target_col!r}' contains missing values."
            )



