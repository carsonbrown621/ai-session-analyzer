# Claude Code Session Log Format

Reference for the parser. **Read this before changing the parser.**

> **Provenance:** written in 2026-11 from inspecting the *structure* (key names,
> value types, counts) of one real session recorded by Claude Code `2.1.318`.
> The format is undocumented by Anthropic and may change between versions.
> All examples below are synthetic.

## 1. Overview

- Location: `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`
  (`<encoded-cwd>` is the working directory with separators replaced by `-`,
  e.g. `C--Users-me-dev-project`).
- Format: JSONL. Each line is one JSON object (an "event") with a top-level
  `type` string.

## 2. Event types

| `type` | Purpose | Used by analyzer |
| --- | --- | --- |
| `assistant` | One content block of a model response, with token `usage` | **Yes** (tokens, tools, stop reasons) |
| `user` | A typed prompt or a tool result sent back to the model | **Yes** (turns, tool results) |
| `system` | Harness events; has a `subtype` (seen: `turn_duration`, `away_summary`) | **Yes** (turn timing) |
| `attachment` | Context attached to a turn | No |
| `mode`, `permission-mode` | Session mode / permission mode changes | No |
| `file-history-snapshot`, `file-history-delta` | Backups of edited files | No |
| `session-owner`, `atis-latch`, `last-prompt`, `ai-title`, `agent-name`, `tools-used`, `cost-state` | Session metadata | No |
| `api-request`, `api-request-shape`, `api-request-blob` | Request bookkeeping | No |

Any other `type` is treated as unknown: count it and skip it.

## 3. Envelope fields

`user`, `assistant`, `system` and `attachment` events share these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `uuid` | str | Unique per line |
| `parentUuid` | str \| null | Previous line in the conversation; `null` on the first |
| `sessionId` | str | Same for the whole file |
| `timestamp` | str | ISO 8601, UTC (`2026-01-01T12:00:00.000Z`) |
| `cwd` | str | Working directory |
| `version` | str | Claude Code version |
| `isSidechain` | bool | Subagent line (see Open questions) |

Metadata events (`mode`, `permission-mode`, ...) often have only `type`,
`sessionId` and one payload field.

## 4. `assistant` events

| Field | Type | Notes |
| --- | --- | --- |
| `requestId` | str | API request id (top level) |
| `message.id` | str | API response id: **the dedupe key** (§6) |
| `message.model` | str | e.g. `claude-opus-5-5` |
| `message.role` | str | `"assistant"` |
| `message.stop_reason` | str | Seen: `tool_use`, `end_turn` |
| `message.content` | list | Usually exactly **one** block per line |
| `message.usage` | dict | Token counts (§5) |

Content block types: `text`, `thinking`, `tool_use`
(`tool_use` has `id`, `name`, `input`).

## 5. `usage` → our four token categories

| Our category | `usage` field |
| --- | --- |
| Input | `input_tokens` |
| Output | `output_tokens` |
| Cache write | `cache_creation_input_tokens` |
| Cache read | `cache_read_input_tokens` |

Other fields exist and are ignored for v1: `cache_creation.ephemeral_5m_input_tokens`,
`cache_creation.ephemeral_1h_input_tokens`, `output_tokens_details.thinking_tokens`,
`server_tool_use.{web_search_requests,web_fetch_requests}`, `service_tier`,
`speed`, `inference_geo`, `iterations`, `fallback_credit`.

## 6. Gotcha: one response is split across several lines

Claude Code writes **one line per content block**. A response that thinks, then
calls a tool becomes two `assistant` lines. Both lines have the **same
`message.id` and `requestId`, and an identical `usage` object** (the usage of
the whole response, repeated):

```jsonl
{"type":"assistant","requestId":"req_a","message":{"id":"msg_a","content":[{"type":"thinking",...}],"usage":{"input_tokens":10,"output_tokens":100,...}}}
{"type":"assistant","requestId":"req_a","message":{"id":"msg_a","content":[{"type":"tool_use",...}],"usage":{"input_tokens":10,"output_tokens":100,...}}}
```

**Rule: count `usage` once per unique `message.id`, never once per line.**
In the inspected session, 52 `assistant` lines came from 22 responses, so
summing per line would have overcounted tokens by about 2.4×.

## 7. `user` events

- `message.content` is either:
  - a **string**: a prompt the user typed, or
  - a **list** of blocks: `text`, or `tool_result` (`tool_use_id`, `content`).
- `toolUseResult` (top level, optional) is a structured copy of the tool
  output: a dict or a string.

## 8. Parser robustness rules

From the project design rules:

- Invalid JSON → skip the line; record it in a bad-line count with line numbers.
- Unknown `type` → count it by type; skip it.
- Missing or wrong-typed fields the analyzer needs (e.g. `assistant` without
  `message.usage`) → skip the line and record its line number. Never crash.

## 9. Open questions

- **Subagents:** the inspected session had no `isSidechain: true` lines and no
  nested subagent log files. How subagent work is recorded is not yet verified.
- **Usage across split lines:** in all 17 split responses inspected, `usage`
  was identical on every line. If they ever differ, which line wins is undecided.

## 10. Fixture: `tests/fixtures/basic_session.jsonl`

A synthetic "happy path" session: 7 lines, no bad lines.

| Line | `type` | Notes |
| --- | --- | --- |
| 1 | `permission-mode` | Ignored event type |
| 2 | `user` | String content (prompt) |
| 3 | `assistant` | `msg_fixture_a`, `thinking` |
| 4 | `assistant` | `msg_fixture_a`, `tool_use` (split response, same usage) |
| 5 | `user` | List content, `tool_result` |
| 6 | `assistant` | `msg_fixture_b`, `text`, `end_turn` |
| 7 | `system` | `turn_duration` |

Expected token totals (deduplicated: 2 responses):

| | Input | Output | Cache write | Cache read |
| --- | --- | --- | --- | --- |
| `msg_fixture_a` | 10 | 100 | 1000 | 0 |
| `msg_fixture_b` | 20 | 200 | 0 | 1100 |
| **Total** | **30** | **300** | **1000** | **1100** |

A parser that forgets to deduplicate would report input 40, output 400 and
cache write 2000.
