"""Physics and mathematical primitives for swarm reasoning."""

from .math_utils import (
    cosine_similarity_dicts,
    cosine_similarity_vectors,
    euclidean_distance,
    exponential_decay,
    manhattan_distance,
    normalize_vector,
    sigmoid,
    softmax,
    weighted_average,
)

__all__ = [
    "cosine_similarity_vectors",
    "cosine_similarity_dicts",
    "euclidean_distance",
    "manhattan_distance",
    "normalize_vector",
    "weighted_average",
    "exponential_decay",
    "sigmoid",
    "softmax",
]

