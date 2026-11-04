"""Command-line interface for session-analyzer."""

import argparse
import sys

from session_analyzer import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="session-analyzer",
        description=(
            "Analyze Claude Code session logs for token usage "
            "and wasteful agent patterns."
        ),
    )
    # action="version" prints the string and exits with code 0.
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return an exit code.

    Tests pass argv as a list so they can run the CLI in-process. When it
    is None (a real command-line run), fall back to sys.argv, minus the
    program name in sys.argv[0].
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    if not argv:
        # No subcommands exist yet, so show help instead of doing nothing.
        parser.print_help()
        return 0

    parser.parse_args(argv)
    return 0
