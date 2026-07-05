"""
Configuration schema definitions.

This module defines the typed configuration objects used throughout
the Time Series Forecasting Lab.

A schema should only describe the structure of the configuration.

It should NOT:
- read YAML
- know where the YAML file is
- contain business logic
- initialize models

Its only responsibility is to answer:

"If a valid config.yaml is loaded,
what Python objects should it become?"


config.yaml --> reader.py --> schema.py --> settings.py --> Application
"""


from pydantic import BaseModel, Field
from pathlib import Path 

class ProjectConfig(BaseModel):
    """
    Project metadata.
    """
    name: str = Field(..., description="Name of the project.")
    version: str = Field(default="0.1.0", description="Current version of the project")
    description: str = Field(default="", description="Short description of the project.")


class PathsConfig(BaseModel):
    """ 
    Directory paths used throughout the project.
    """
    
    data_dir: Path = Field(..., description="Root directory contains all datasets.")
    raw_data_dir: Path = Field(..., description="Directory containing raw, unmodified datasets.")
    processed_data_dir: Path = Field(..., description="Directory containing processed data.")
    reports_dir: Path = Field(..., description="Directory for generated reports.")
    plots_dir: Path = Field(..., description="Directory for forecast plots and visualizations")
    models_dir: Path = Field(..., description="Directory where trained models are stored.")
    logs_dir: Path = Field(..., description="Directory containing application log files.")
    
class RuntimeConfig(BaseModel):
    """
    Runtime Configuration
    """
    
    environment: str = Field(default="local", description="Execution environment: local, dev, prod.")
    random_seed: int = Field(default=42, ge=0, description="Random seed used for reproducibility")
    log_level: str = Field(defauly="INFO", description="Logging Level")
    

class DataConfig(BaseModel):
    """
    Dataset Configuration
    """
    
    dataset_name: str = Field(..., description="Name of the dataset.")
    target_column: str = Field(..., description="Target Variable to Forecast")
    time_column: str = Field(..., description="Timestamp Column")
    id_column: str = Field(..., description="Unique identifier column for multiple time series.")
    frequency: str = Field(..., description="Time Series Frequency (D, W, M, H, etc.)")

class ForecastConfig(BaseModel):
    """ 
    Forecasting Configuration
    """
    
    horizon: int = Field(..., gt=0, description="Forecasting Horizon")
    validation_size: int = Field(..., ge=0, description="Number of observations reserved for validation")
    test_size: int = Field(..., ge=0, description="Number of observations reserved for testing.")
    seasonal_period: int = Field(..., gt=0, description="Seasonal Period of the Time Series")
# 6
class BacktestingConfig(BaseModel):
    """ 
    Backtesting Configuration
    """
    
    n_splits: int = Field(..., gt=0, description="Number of rolling backtesting splits")
    initial_train_size: int = Field(..., gt=0, description="Initial Training Window Size")
    step_size: int = Field(..., gt=0, description="Window Shift after each Backtesting Iteration.")
    expanding_window: bool = Field(default=True, description="Whether to use expanding Windows or Rolling Windows")
    

# 7
class ModelParametersConfig(BaseModel):
    """ 
    Model-specific Hyperparameters.
    Unknown fields are allowed becuase different forecasting models require different hyperparameters.
    """
    
    model_config = ConfigDict(extra="allow")
    

# 8
class ModelConfig(BaseModel):
    """
    Forecast Model Configuration
    """   
    name: str = Field(..., description="Name of the forecasting model.")
    category: str = Field(..., description="Model Category (baseline, statistical, ML, DL, transformer).")
    parame: ModelParametersConfig = Field(..., description="Model-specific hyperparameters")

# 9
class EvaluationConfig(BaseModel):
    """ 
    Forecast Evaluation Configuration
    """
    metrics: list[str] = Field(..., description="Evaluation metrics used for model comparison")
# 10
class TrackingConfig(BaseModel):
    """ 
    Experiment Tracking Configuration
    """
    enabled: bool = Field(default=False, description="Whether experiment tracking is enabled.")
    experiment_name: str = Field(..., description="Experiment name used by the tracking system")
    tracking_uri: str = Field(..., description="Tracking server URI or local tracking directory")
    
# 11
class Settings(BaseModel):
    """ 
    Root Application Configuration.
    
    This class aggregates all configuration sections into a single, validated configuration object.
    """
    
    project: ProjectConfig = Field(..., description="Project Configuration")
    path: PathsConfig = Field(..., description="Path Configuration")
    runtime: RuntimeConfig = Field(..., description="Runtime Configuration")
    data: DataConfig = Field(..., description="Dataset Configuration")
    forecast: ForecastConfig = Field(..., description="Forecasting Configuration")
    backtesting: BacktestingConfig = Field(..., description="Backtesting Configuration")
    model: ModelConfig = Field(..., desciption= "Model Configuration")
    evaluation: EvaluationConfig = Field(..., description="Evaluation Configuration")
    tracking: TrackingConfig = Field(..., desciption="Experiment Tracking Configuration")