"""Persist forecasting experiment artifact to local storage."""

import json
import re
from pathlib import Path 

import pandas as pd

from ts_forecasting_lab.evaluation.runner import EvaluationResults

def vaidate_identifier(identifier: str) -> None:
    """Ensure an identifier is safe to use as a directory name."""

    if not isinstance(identifier, str):
        raise ValueError("Identifier must be a string.")

    if not re.fullmatch(r"[A-Za-z0-9_-]", identifier):
        raise ValueError(f"Invalid identifer: {identifier!r}")
