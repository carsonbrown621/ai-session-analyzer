"""Analyze Claude Code session logs."""

from importlib.metadata import version

# Read the version from the installed package metadata so pyproject.toml
# stays the single source of truth.
__version__ = version("session-analyzer")
