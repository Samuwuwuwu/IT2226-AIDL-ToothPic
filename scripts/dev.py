"""Start both local dev servers and stop their child process trees on exit."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "services" / "api"
WEB_ROOT = ROOT / "apps" / "web"
API_PYTHON = API_ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def check_port(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            raise RuntimeError(f"Port {port} already in use. Close that app manually.")


def pipe_lines(name: str, process: subprocess.Popen[str]) -> None:
    assert process.stdout is not None
    for line in process.stdout:
        print(f"[{name}] {line.rstrip()}", flush=True)


def stop_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            check=False,
        )
    else:
        os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def main() -> int:
    if not API_PYTHON.is_file():
        print("[FAIL] API venv missing. Run setup-dev.bat first.")
        return 1
    if not (WEB_ROOT / "node_modules").is_dir():
        print("[FAIL] Web dependencies missing. Run setup-dev.bat first.")
        return 1
    try:
        for port in (8000, 5173):
            check_port(port)
    except RuntimeError as exc:
        print(f"[FAIL] {exc}")
        return 1

    kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True,
        "bufsize": 1,
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True

    children: list[tuple[str, subprocess.Popen[str]]] = []
    try:
        api = subprocess.Popen(
            [
                str(API_PYTHON), "-m", "uvicorn", "app.main:app",
                "--app-dir", str(API_ROOT), "--reload",
                "--reload-dir", str(API_ROOT / "app"),
                "--host", "127.0.0.1", "--port", "8000",
            ],
            cwd=ROOT, **kwargs,
        )
        children.append(("API", api))
        npm = "npm.cmd" if os.name == "nt" else "npm"
        web = subprocess.Popen([npm, "run", "dev"], cwd=WEB_ROOT, **kwargs)
        children.append(("WEB", web))

        for name, child in children:
            threading.Thread(
                target=pipe_lines, args=(name, child), daemon=True,
            ).start()

        print("[OK] API http://127.0.0.1:8000/api/v1/health")
        print("[OK] WEB http://localhost:5173")
        print("[INFO] Ctrl+C to stop both.")
        while all(p.poll() is None for _, p in children):
            time.sleep(0.3)
        for name, p in children:
            if p.poll() is not None:
                print(f"[INFO] {name} exited ({p.returncode}); stopping servers.")
        return 1
    except KeyboardInterrupt:
        print("\n[INFO] Stopping development servers...")
        return 0
    finally:
        for _, p in reversed(children):
            stop_tree(p)


if __name__ == "__main__":
    sys.exit(main())
