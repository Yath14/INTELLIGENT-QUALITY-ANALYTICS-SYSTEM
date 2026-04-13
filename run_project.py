import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / ".venv"
if not VENV_DIR.exists():
    VENV_DIR = BASE_DIR / "venv"
PYTHON = VENV_DIR / "Scripts" / "python.exe"

if not PYTHON.exists():
    raise FileNotFoundError(
        "Virtual environment was not found. Create one with `python -m venv .venv` or `python -m venv venv` "
        "in the project root, then install requirements with `python -m pip install -r requirements.txt`."
    )

CREATIONFLAGS = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0


def wait_for_url(url: str, timeout: int = 30) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(1)
    return False


def launch_process(command: list[str]) -> subprocess.Popen:
    return subprocess.Popen(
        [str(PYTHON)] + command,
        cwd=str(BASE_DIR),
        creationflags=CREATIONFLAGS,
    )


def main() -> int:
    backend = launch_process(["-m", "uvicorn", "main:app", "--port", "8000"])
    try:
        print("Starting FastAPI backend...")
        if not wait_for_url("http://127.0.0.1:8000/docs", timeout=30):
            backend.terminate()
            raise RuntimeError("FastAPI backend did not become available within 30 seconds.")

        print("Backend ready at http://127.0.0.1:8000")
        print("Launching Streamlit UI...")

        ui_process = launch_process(["-m", "streamlit", "run", "ui.py"])
        return ui_process.wait()
    finally:
        if backend.poll() is None:
            backend.terminate()
            backend.wait(timeout=10)
        print("Backend process terminated.")


if __name__ == "__main__":
    raise SystemExit(main())
