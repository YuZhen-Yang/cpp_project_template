"""
Run once to install pre-commit hooks, then removes itself and the config file.
"""

import os
import subprocess
import sys


def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}", file=sys.stderr)
        sys.exit(result.returncode)


run("pip install pre-commit")
run("pre-commit install")

for path in [".pre-commit-config.yaml", __file__]:
    try:
        os.remove(path)
        print(f"Removed: {path}")
    except OSError as e:
        print(f"Warning: could not remove {path}: {e}", file=sys.stderr)