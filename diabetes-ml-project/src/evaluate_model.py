"""Model evaluation utilities for the diabetes prediction project."""

from typing import Dict, Tuple

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)


def compute_core_metrics(
    y_true: np.ndarray, y_pred_labels: np.ndarray, y_pred_proba: np.ndarray
) -> Dict[str, float]:
    """Compute core evaluation metrics for binary classification.

    Parameters
    ----------
    y_true : np.ndarray
        Ground-truth labels (0/1).
    y_pred_labels : np.ndarray
        Predicted class labels (0/1).
    y_pred_proba : np.ndarray
        Predicted probabilities for the positive class.

    Returns
    -------
    dict
        Dictionary with accuracy and ROC AUC.
    """
    acc = accuracy_score(y_true, y_pred_labels)
    roc_auc = roc_auc_score(y_true, y_pred_proba)
    return {"accuracy": acc, "roc_auc": roc_auc}


def compute_confusion(y_true: np.ndarray, y_pred_labels: np.ndarray) -> np.ndarray:
    """Return the confusion matrix for predicted vs true labels."""
    return confusion_matrix(y_true, y_pred_labels)


def text_classification_report(
    y_true: np.ndarray, y_pred_labels: np.ndarray
) -> str:
    """Generate a text classification report (precision/recall/F1)."""
    return classification_report(y_true, y_pred_labels)

