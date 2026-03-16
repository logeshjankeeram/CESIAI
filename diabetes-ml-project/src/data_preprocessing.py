"""Data loading and preprocessing utilities for the diabetes ML project.

This module centralizes data preparation logic so that notebooks remain
lightweight and focused on experimentation.
"""

from pathlib import Path
from typing import Tuple, List

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_raw_data(raw_dir: Path) -> pd.DataFrame:
    """Load the raw BRFSS 2015 diabetes dataset from the raw data directory.

    Parameters
    ----------
    raw_dir : Path
        Directory containing the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    csv_path = raw_dir / "diabetes_binary_health_indicators_BRFSS2015.csv"
    return pd.read_csv(csv_path)


def split_features_target(
    df: pd.DataFrame, target_col: str = "Diabetes_binary"
) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate explanatory variables (X) from the target variable (y).

    Parameters
    ----------
    df : pd.DataFrame
        Full dataset including the target column.
    target_col : str, optional
        Name of the target column, by default "Diabetes_binary".

    Returns
    -------
    Tuple[pd.DataFrame, pd.Series]
        X (features), y (target).
    """
    y = df[target_col].copy()
    X = df.drop(columns=[target_col]).copy()
    return X, y


def stratified_train_val_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    train_size: float = 0.7,
    val_size: float = 0.15,
    test_size: float = 0.15,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """Perform a stratified split into train, validation, and test sets.

    The function first splits off the training data, then splits the remaining
    data into validation and test sets, preserving class distribution.
    """
    assert abs(train_size + val_size + test_size - 1.0) < 1e-8, "Splits must sum to 1.0"

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=(1.0 - train_size),
        stratify=y,
        random_state=random_state,
    )

    # Proportion of temp that should go to test to respect global val/test sizes
    test_size_rel = test_size / (val_size + test_size)

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=test_size_rel,
        stratify=y_temp,
        random_state=random_state,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def fit_scaler_on_train(
    X_train: pd.DataFrame, numeric_cols: List[str]
) -> Tuple[StandardScaler, pd.DataFrame]:
    """Fit a StandardScaler on training data and return the fitted scaler and scaled train set.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training feature matrix.
    numeric_cols : list of str
        Columns to scale.

    Returns
    -------
    Tuple[StandardScaler, pd.DataFrame]
        Fitted scaler and transformed training set.
    """
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    return scaler, X_train_scaled


def apply_scaler(
    scaler: StandardScaler, X: pd.DataFrame, numeric_cols: List[str]
) -> pd.DataFrame:
    """Apply a fitted StandardScaler to a dataset.

    Parameters
    ----------
    scaler : StandardScaler
        Fitted scaler (trained on training data).
    X : pd.DataFrame
        Dataset to transform.
    numeric_cols : list of str
        Columns to scale.

    Returns
    -------
    pd.DataFrame
        Transformed dataset.
    """
    X_scaled = X.copy()
    X_scaled[numeric_cols] = scaler.transform(X[numeric_cols])
    return X_scaled


def save_processed_splits(
    processed_dir: Path,
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_val: pd.Series,
    y_test: pd.Series,
    target_col: str = "Diabetes_binary",
) -> None:
    """Save processed train/validation/test splits to CSV files.

    All files are written into the processed data directory.
    """
    processed_dir.mkdir(parents=True, exist_ok=True)

    X_train.to_csv(processed_dir / "X_train.csv", index=False)
    X_val.to_csv(processed_dir / "X_val.csv", index=False)
    X_test.to_csv(processed_dir / "X_test.csv", index=False)

    y_train.to_csv(processed_dir / "y_train.csv", index=False, header=[target_col])
    y_val.to_csv(processed_dir / "y_val.csv", index=False, header=[target_col])
    y_test.to_csv(processed_dir / "y_test.csv", index=False, header=[target_col])

