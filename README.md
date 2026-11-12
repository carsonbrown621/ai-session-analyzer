# Claude Code Session Analyzer

![CI](https://github.com/carsonbrown621/ai-session-analyzer/actions/workflows/ci.yml/badge.svg)

Analyzes Claude Code session logs to:
- Measure token usage
- Detect wasteful agent patterns
- Recommend more efficient workflows

## **Status:** Early Development. ⚠️ v1 in progress. ⚠️

## v1 scope

1. **Read** a Claude Code session log (JSONL).
2. **Analyze** token usage and detect potentially wasteful patterns.
3. **Report** findings with rule-based recommendations via command line.

## Roadmap

- [ ] **v1: CLI analyzer.** Parser, token accounting, detection rules, text report, tests.

- [ ] **v2: AI coach.** The Claude API turns findings into tailored explanations
      and improved prompt suggestions.
  
- [ ] **v3: Evaluation and comparison.** Compare two sessions solving the same task;
      evaluate whether the coach's recommendations are accurate; recommend when to delegate work to subagents.

## Development

Requires [uv](https://docs.astral.sh/uv/). uv installs the pinned Python version automatically.

```powershell
uv sync                          # install dependencies into .venv
uv run session-analyzer --help   # run the CLI
uv run pytest                    # run tests
uv run ruff check .              # lint
uv run ruff format .             # format
```

## Planned Tech Stack

- v1: Python, uv, Pydantic, pytest, GitHub Actions CI, ruff
- v2: SQLite/SQL, Anthropic SDK, pandas
- v3: FastAPI, Streamlit, Docker + Compose, AWS Deployment, scikit-learn
