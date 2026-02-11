#!/usr/bin/env python3
"""
One-click Vivarium dev launcher (macOS + Windows).

Starts/replaces:
- backend: uvicorn vivarium.runtime.swarm_api:app
- frontend: python -m vivarium.runtime.control_panel_app
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys
import time
from pathlib import Path


def _root_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _safe_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    try:
        return int(raw) if raw is not None else default
    except ValueError:
        return default


def _venv_python(root: Path) -> Path:
    if platform.system().lower().startswith("win"):
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def _ensure_venv(root: Path) -> Path:
    python_bin = _venv_python(root)
    if python_bin.exists():
        return python_bin
    creator = shutil_which(["python3", "python", "py"])
    if creator is None:
        raise RuntimeError("Python 3.11+ is required to create .venv")
    args = [creator, "-m", "venv", str(root / ".venv")]
    if Path(creator).name.lower() == "py":
        args = [creator, "-3", "-m", "venv", str(root / ".venv")]
    print("[launcher] creating virtual environment at .venv")
    subprocess.check_call(args, cwd=str(root))
    if not python_bin.exists():
        raise RuntimeError("failed to create .venv python executable")
    return python_bin


def shutil_which(candidates: list[str]) -> str | None:
    import shutil

    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    return None


def _list_listener_pids(port: int) -> list[int]:
    system = platform.system().lower()
    if system.startswith("win"):
        try:
            proc = subprocess.run(
                ["netstat", "-ano"],
                check=False,
                capture_output=True,
                text=True,
            )
            pids = set()
            for line in proc.stdout.splitlines():
                if "LISTENING" not in line.upper():
                    continue
                if f":{port}" not in line:
                    continue
                parts = re.split(r"\s+", line.strip())
                if parts:
                    try:
                        pids.add(int(parts[-1]))
                    except ValueError:
                        continue
            return sorted(pids)
        except Exception:
            return []
    try:
        proc = subprocess.run(
            ["lsof", "-tiTCP:%d" % port, "-sTCP:LISTEN"],
            check=False,
            capture_output=True,
            text=True,
        )
        pids = []
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                pids.append(int(line))
            except ValueError:
                continue
        return sorted(set(pids))
    except Exception:
        return []


def _stop_pid(pid: int, force: bool = False) -> None:
    system = platform.system().lower()
    if system.startswith("win"):
        args = ["taskkill", "/PID", str(pid), "/T"]
        if force:
            args.append("/F")
        subprocess.run(args, check=False, capture_output=True, text=True)
        return
    sig = signal.SIGKILL if force else signal.SIGTERM
    try:
        os.kill(pid, sig)
    except OSError:
        return


def _replace_port_listener(port: int) -> None:
    pids = _list_listener_pids(port)
    if not pids:
        return
    print(f"[launcher] stopping process(es) on port {port}: {', '.join(str(p) for p in pids)}")
    for pid in pids:
        _stop_pid(pid, force=False)
    time.sleep(1.0)
    survivors = _list_listener_pids(port)
    for pid in survivors:
        _stop_pid(pid, force=True)


def _requirements_signature(root: Path, python_bin: Path) -> str:
    hasher = hashlib.sha256()
    hasher.update(sys.version.encode("utf-8"))
    hasher.update(str(python_bin).encode("utf-8"))
    for name in ("requirements.txt", "requirements-groq.txt"):
        req = root / name
        if req.exists():
            hasher.update(name.encode("utf-8"))
            hasher.update(req.read_bytes())
    return hasher.hexdigest()


def _run_checked(args: list[str], cwd: Path) -> None:
    subprocess.check_call(args, cwd=str(cwd))


def _ensure_dependencies(root: Path, python_bin: Path) -> None:
    """
    Install/update dependencies once per requirements signature.
    """
    state_file = root / ".swarm" / "dev_install_state.json"
    signature = _requirements_signature(root, python_bin)
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    previous_sig = str(state.get("requirements_signature") or "")
    already_installed = bool(state.get("installed")) and previous_sig == signature
    force_reinstall = os.environ.get("VIVARIUM_FORCE_REINSTALL", "").strip().lower() in {"1", "true", "yes"}
    if already_installed and not force_reinstall:
        print("[launcher] dependencies already installed (cached state)")
        return

    print("[launcher] bootstrapping pip + requirements (first run or requirements changed)")
    _run_checked([str(python_bin), "-m", "ensurepip", "--upgrade"], root)
    _run_checked([str(python_bin), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], root)

    req_main = root / "requirements.txt"
    req_groq = root / "requirements-groq.txt"
    if req_main.exists():
        _run_checked([str(python_bin), "-m", "pip", "install", "-r", str(req_main)], root)
    if req_groq.exists():
        _run_checked([str(python_bin), "-m", "pip", "install", "-r", str(req_groq)], root)
    _run_checked([str(python_bin), "-m", "pip", "install", "pytest", "watchdog"], root)

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(
            {
                "installed": True,
                "requirements_signature": signature,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("[launcher] dependency bootstrap complete")


def main() -> int:
    root = _root_dir()
    api_port = _safe_int_env("VIVARIUM_API_PORT", 8420)
    ui_port = _safe_int_env("VIVARIUM_CONTROL_PANEL_PORT", 8421)
    log_dir = root / ".swarm" / "logs"
    pid_dir = root / ".swarm"
    log_dir.mkdir(parents=True, exist_ok=True)
    pid_dir.mkdir(parents=True, exist_ok=True)

    python_bin = _ensure_venv(root)
    _ensure_dependencies(root, python_bin)

    print("[launcher] replacing existing backend/frontend instances...")
    _replace_port_listener(api_port)
    _replace_port_listener(ui_port)

    api_log = log_dir / "api.log"
    ui_log = log_dir / "ui.log"

    print(f"[launcher] starting backend on :{api_port}")
    with open(api_log, "w", encoding="utf-8") as api_out:
        api_proc = subprocess.Popen(
            [
                str(python_bin),
                "-m",
                "uvicorn",
                "vivarium.runtime.swarm_api:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(api_port),
                "--reload",
            ],
            cwd=str(root),
            stdout=api_out,
            stderr=subprocess.STDOUT,
        )

    print(f"[launcher] starting frontend on :{ui_port}")
    with open(ui_log, "w", encoding="utf-8") as ui_out:
        ui_proc = subprocess.Popen(
            [str(python_bin), "-m", "vivarium.runtime.control_panel_app"],
            cwd=str(root),
            stdout=ui_out,
            stderr=subprocess.STDOUT,
        )

    (pid_dir / "dev_api.pid").write_text(str(api_proc.pid), encoding="ascii")
    (pid_dir / "dev_ui.pid").write_text(str(ui_proc.pid), encoding="ascii")

    print("")
    print("[launcher] Vivarium dev stack is up.")
    print(f"  API: http://127.0.0.1:{api_port}")
    print(f"  UI : http://127.0.0.1:{ui_port}")
    print("  Logs:")
    print(f"    {api_log}")
    print(f"    {ui_log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
