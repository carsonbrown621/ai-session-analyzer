## Project
CLI tool that analyzes Claude Code session logs (JSONL) to measure token usage, detect wasteful agent patterns, and recommend better workflows. This is a learning + portfolio project: I'm building skills, not just code.

## Platform
Windows 11 + PowerShell. Give PowerShell-compatible commands; don't assume bash.

## Working Agreement
- Propose a plan and wait for my approval before writing code. Exception: trivial fixes (typos, lint, renames) — just do them and tell me what changed.
- One small, focused change at a time. Keep diffs easy to review.
- Briefly explain non-obvious code and Python idioms.
- Basic concepts: check `docs/concepts.md` before explaining one. If it's listed, don't re-explain it. After explaining a new one, add a one-line entry.
- Ask when requirements are unclear instead of guessing.
- Never commit or push. I review and commit myself.
- Don't add dependencies without asking.
- If there's a more standard industry approach than what I asked for, say so and explain the trade-off before implementing.
- After each completed GitHub issue, ask me 1-2 questions about the code we just wrote (what a function does, why a design choice was made) before moving on.

## Tech Stack
Python 3.12+, uv, Pydantic v2, pytest, ruff. CLI built with argparse (stdlib).

## Commands
- Install deps: `uv sync`
- Run the CLI: `uv run session-analyzer --help`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Design Rules
- All metrics and findings are computed deterministically from the log. No estimated or invented numbers.
- v1 reports token counts only. No dollar costs.
- Track input, output, cache-write, and cache-read tokens separately.
- The parser must handle unknown event types and missing fields without crashing. Skip bad lines and report them as a count plus line numbers.
- Log format reference: `docs/log-format.md` (to be written once we inspect a real log). Once it exists, read it before changing the parser.

## Data Safety
- Never commit real session logs. Tests use synthetic fixtures in `tests/fixtures/` only.
- Don't read anything under `~/.claude` unless I ask. When I explicitly ask, you may run `session-analyzer` on real logs there, but never copy real log contents into the repo.

## Definition of Done
- `uv run pytest` passes
- `uv run ruff check .` and `uv run ruff format --check .` are clean
- New behavior has tests
- README updated if anything user-visible changed
