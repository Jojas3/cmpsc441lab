"""Run all tests for lab02."""

import sys
from pathlib import Path

import pytest


def main():
    """Run all lab02 tests using pytest."""
    tests_dir = Path(__file__).parent / "tests"
    return pytest.main([str(tests_dir), "-v"])


if __name__ == "__main__":
    sys.exit(main())
