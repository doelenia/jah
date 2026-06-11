#!/usr/bin/env python3
"""Compatibility shim — use system/release/scripts/init_jah.py."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

_TARGET = Path(__file__).resolve().parents[1] / "release" / "scripts" / "init_jah.py"
sys.argv[0] = str(_TARGET)
runpy.run_path(str(_TARGET), run_name="__main__")
