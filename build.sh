#!/usr/bin/env bash
set -e
echo "==> Python: $(python --version)"
echo "==> Pip: $(pip --version)"
pip install --upgrade pip
pip install -r requirements.txt
echo "==> Installed packages:"
pip list
