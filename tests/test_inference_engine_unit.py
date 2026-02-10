import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime.inference_engine import estimate_complexity, get_engine_type_from_env, EngineType


def test_estimate_complexity_base_score():
    request = "add docs"
    assert estimate_complexity(request) == 0


def test_estimate_complexity_keywords():
    request = "optimize algorithm async pipeline"
    assert estimate_complexity(request) == 8


def test_estimate_complexity_length_bonus():
    request = "word " * 170
    assert len(request) > 800
    assert estimate_complexity(request) == 22


def test_get_engine_type_from_env(monkeypatch):
    monkeypatch.setenv("INFERENCE_ENGINE", "GROQ")
    assert get_engine_type_from_env() == EngineType.GROQ

    monkeypatch.setenv("INFERENCE_ENGINE", "")
    assert get_engine_type_from_env() == EngineType.AUTO
