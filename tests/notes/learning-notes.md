# Concepts

## Personal Learning Log: concepts I learned or refreshed on while building this project. 
DOES NOT CONTAIN ANY ACTUAL PROJECT DOCUMENTATION.

One-line notes on concepts already explained, so they aren't re-explained.

- **Diff**: the set of changes reviewed before a commit. Small, single-topic diffs are easier to review, debug, and revert.
- **CI (Continuous Integration)**: on every push/PR, a fresh cloud machine installs the project and runs lint + tests, marking the commit pass/fail.
- **CI matrix**: runs the same CI job once per value of a setting (here, Python 3.12 and 3.14) to check every version you claim to support.
- **Pydantic**: validates raw data (dicts/JSON) against a typed model class, converting types, filling defaults, and raising `ValidationError` on bad input.
- **src layout**: package code lives in `src/<package>/`, so tests import the installed package rather than accidentally importing loose files from the repo root.
- **Console-script entry point**: `[project.scripts]` in `pyproject.toml` maps a command name (`session-analyzer`) to a function (`session_analyzer.cli:main`); installing the package creates that command.
- **Lockfile (`uv.lock`)**: records the exact resolved version of every dependency so every install (local and CI) gets identical packages.
- **Dunder names (`__x__`)**: "double underscore" names are Python-reserved conventions (`__init__.py`, `__version__`, `__name__`); tools and the language look for them by exact name.
- **`argparse`**: stdlib module that defines a CLI's arguments, parses `sys.argv`, and auto-generates `--help` and usage errors.
- **`sys`**: stdlib module for interpreter-level things; here `sys.argv` (the command-line words) and exit codes.
- **Positional vs. optional arguments**: positional = required, identified by position (`session-analyzer log.jsonl`); optional = named flags with a dash (`--format json`).
- **`importlib.metadata.version()`**: reads an installed package's version at runtime, so the version number only lives in `pyproject.toml`.
