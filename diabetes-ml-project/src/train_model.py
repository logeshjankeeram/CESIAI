"""Training utilities for the diabetes prediction models."""

from pathlib import Path
from typing import Tuple

import numpy as np
import tensorflow as tf


def train_neural_network(
    model: tf.keras.Model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    batch_size: int = 256,
    epochs: int = 20,
) -> tf.keras.callbacks.History:
    """Train a neural network on training data with validation monitoring.

    Parameters
    ----------
    model : tf.keras.Model
        Compiled Keras model.
    X_train, y_train : np.ndarray
        Training features and labels.
    X_val, y_val : np.ndarray
        Validation features and labels.
    batch_size : int, optional
        Mini-batch size, by default 256.
    epochs : int, optional
        Number of training epochs, by default 20.

    Returns
    -------
    tf.keras.callbacks.History
        Training history object.
    """
    callbacks: Tuple[tf.keras.callbacks.Callback, ...] = (
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
        ),
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        batch_size=batch_size,
        epochs=epochs,
        callbacks=list(callbacks),
        verbose=1,
    )
    return history


def save_model(model: tf.keras.Model, models_dir: Path, model_name: str = "baseline_mlp") -> Path:
    """Save a trained Keras model to the models directory.

    The model is saved in the TensorFlow SavedModel format.
    """
    models_dir.mkdir(parents=True, exist_ok=True)
    save_path = models_dir / model_name
    model.save(save_path)
    return save_path

