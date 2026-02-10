import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from vivarium.runtime.safety_gateway import SafetyGateway
from vivarium.runtime.safety_validator import SafeFileWriter


@pytest.mark.e2e
def test_safe_write_checkpoint_and_rollback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    file_path = tmp_path / "module.py"
    original = "def add(a, b):\n    return a + b\n"
    file_path.write_text(original, encoding="utf-8")

    gateway = SafetyGateway(tmp_path)
    passed, report = gateway.pre_execute_safety_check(
        "Refactor module to add a helper function."
    )

    assert passed is True
    assert report["passed"] is True

    writer = SafeFileWriter()
    updated = (
        "def add(a, b):\n"
        "    return a + b\n\n"
        "def sub(a, b):\n"
        "    return a - b\n"
    )

    result = writer.safe_write(file_path, updated)
    assert result.valid is True
    assert file_path.read_text(encoding="utf-8") == updated

    checkpoint = writer.checkpoint_manager.get_latest_checkpoint()
    assert checkpoint is not None

    success, restored = writer.checkpoint_manager.rollback(checkpoint)
    assert success is True
    assert str(file_path) in restored
    assert file_path.read_text(encoding="utf-8") == original
