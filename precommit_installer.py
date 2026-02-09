import subprocess
import sys

def main():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pre-commit"])
    subprocess.check_call(["pre-commit", "install"])
    print("Pre‑commit hooks installed.")