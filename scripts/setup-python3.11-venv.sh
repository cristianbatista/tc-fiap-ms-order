#!/usr/bin/env bash
# Create a virtualenv using Python 3.11 if available
set -euo pipefail

PYTHON_BIN=""

# Prefer explicit python3.11 binary
if command -v python3.11 >/dev/null 2>&1; then
  PYTHON_BIN=python3.11
elif command -v python3.11m >/dev/null 2>&1; then
  PYTHON_BIN=python3.11m
elif command -v python3 >/dev/null 2>&1; then
  # check version of python3
  VER=$("$(command -v python3)" -c 'import sys; print("%s.%s" % (sys.version_info.major, sys.version_info.minor))')
  if [[ "$VER" == "3.11"* ]]; then
    PYTHON_BIN=python3
  fi
fi

if [[ -z "$PYTHON_BIN" ]]; then
  echo "Python 3.11 not found on PATH."
  echo "Please install Python 3.11 (eg. using pyenv or your system package manager) and retry."
  exit 1
fi

echo "Using $PYTHON_BIN to create virtualenv .venv"

${PYTHON_BIN} -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
echo "Virtualenv .venv created with $(${PYTHON_BIN} -V 2>&1)"
echo "To activate: source .venv/bin/activate"
