"""Model architectures for the diabetes prediction project.

This module defines baseline neural network architectures that can be reused
across experiments (e.g., in training scripts and notebooks).
"""

from typing import Optional

import tensorflow as tf
from tensorflow.keras import layers, models


def build_baseline_mlp(
    input_dim: int,
    hidden_units: Optional[list[int]] = None,
    dropout_rate: float = 0.0,
) -> tf.keras.Model:
    """Create a simple baseline feed-forward neural network for binary classification.

    Parameters
    ----------
    input_dim : int
        Number of input features.
    hidden_units : list of int, optional
        Sizes of hidden layers, by default [64, 32].
    dropout_rate : float, optional
        Dropout rate applied after each hidden layer, by default 0.0 (no dropout).

    Returns
    -------
    tf.keras.Model
        Compiled Keras model with sigmoid output for P(diabetes=1).
    """
    if hidden_units is None:
        hidden_units = [64, 32]

    inputs = layers.Input(shape=(input_dim,))
    x = inputs
    for units in hidden_units:
        x = layers.Dense(units, activation="relu")(x)
        if dropout_rate > 0.0:
            x = layers.Dropout(dropout_rate)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="baseline_mlp")
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model

