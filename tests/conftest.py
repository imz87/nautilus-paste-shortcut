"""Pytest path configuration.

Prepends src/ to sys.path so that core_logic can be imported
without requiring PYTHONPATH overrides.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
