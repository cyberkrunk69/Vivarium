"""
Mathematical utility functions for the swarm system.
Consolidates duplicate math operations across modules.
"""

import math
import numpy as np
from typing import Dict, Any, Union

try:
    from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def cosine_similarity_vectors(vec1: Union[np.ndarray, list], vec2: Union[np.ndarray, list]) -> float:
    """
    Compute cosine similarity between two dense vectors.

    Args:
        vec1: First vector (numpy array or list)
        vec2: Second vector (numpy array or list)

    Returns:
        Float cosine similarity score between -1 and 1
    """
    if SKLEARN_AVAILABLE:
        # Use sklearn for efficiency with sparse matrices
        vec1_arr = np.array(vec1).reshape(1, -1)
        vec2_arr = np.array(vec2).reshape(1, -1)
        return float(sklearn_cosine_similarity(vec1_arr, vec2_arr)[0][0])

    # Fallback: Manual computation
    vec1_arr = np.array(vec1).flatten()
    vec2_arr = np.array(vec2).flatten()

    if len(vec1_arr) != len(vec2_arr):
        raise ValueError("Vectors must have the same length")

    dot_product = np.dot(vec1_arr, vec2_arr)
    norm1 = np.linalg.norm(vec1_arr)
    norm2 = np.linalg.norm(vec2_arr)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def cosine_similarity_dicts(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """
    Compute cosine similarity between two sparse vectors represented as dictionaries.
    Vectors are dicts mapping terms to TF/embedding scores.

    Args:
        vec1: First vector as term->score mapping
        vec2: Second vector as term->score mapping

    Returns:
        Float cosine similarity score between 0 and 1
    """
    if not vec1 or not vec2:
        return 0.0

    # Get intersection of terms
    common_terms = set(vec1.keys()) & set(vec2.keys())

    # Dot product of vectors (only for common terms)
    dot_product = sum(vec1.get(term, 0.0) * vec2.get(term, 0.0) for term in common_terms)

    # Magnitudes
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot_product / (mag1 * mag2)


def euclidean_distance(vec1: Union[np.ndarray, list], vec2: Union[np.ndarray, list]) -> float:
    """
    Compute Euclidean distance between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Euclidean distance
    """
    vec1_arr = np.array(vec1)
    vec2_arr = np.array(vec2)

    if len(vec1_arr) != len(vec2_arr):
        raise ValueError("Vectors must have the same length")

    return float(np.linalg.norm(vec1_arr - vec2_arr))


def manhattan_distance(vec1: Union[np.ndarray, list], vec2: Union[np.ndarray, list]) -> float:
    """
    Compute Manhattan (L1) distance between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Manhattan distance
    """
    vec1_arr = np.array(vec1)
    vec2_arr = np.array(vec2)

    if len(vec1_arr) != len(vec2_arr):
        raise ValueError("Vectors must have the same length")

    return float(np.sum(np.abs(vec1_arr - vec2_arr)))


def normalize_vector(vec: Union[np.ndarray, list]) -> np.ndarray:
    """
    Normalize a vector to unit length.

    Args:
        vec: Input vector

    Returns:
        Normalized vector as numpy array
    """
    vec_arr = np.array(vec)
    norm = np.linalg.norm(vec_arr)

    if norm == 0:
        return vec_arr

    return vec_arr / norm


def weighted_average(values: list, weights: list) -> float:
    """
    Compute weighted average of values.

    Args:
        values: List of values to average
        weights: List of weights (same length as values)

    Returns:
        Weighted average
    """
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length")

    if not values:
        return 0.0

    total_weight = sum(weights)
    if total_weight == 0:
        return sum(values) / len(values)  # Unweighted average if all weights are 0

    return sum(v * w for v, w in zip(values, weights)) / total_weight


def exponential_decay(base_value: float, decay_rate: float, time_units: float) -> float:
    """
    Apply exponential decay to a value.

    Args:
        base_value: Initial value
        decay_rate: Decay rate (e.g., 0.995 for 0.5% decay per unit)
        time_units: Number of time units elapsed

    Returns:
        Decayed value
    """
    return base_value * (decay_rate ** time_units)


def sigmoid(x: float) -> float:
    """
    Sigmoid activation function.

    Args:
        x: Input value

    Returns:
        Sigmoid output between 0 and 1
    """
    return 1.0 / (1.0 + math.exp(-x))


def softmax(values: list) -> list:
    """
    Apply softmax function to a list of values.

    Args:
        values: List of input values

    Returns:
        List of softmax probabilities
    """
    if not values:
        return []

    # Subtract max for numerical stability
    max_val = max(values)
    exp_values = [math.exp(v - max_val) for v in values]
    sum_exp = sum(exp_values)

    return [exp_val / sum_exp for exp_val in exp_values]