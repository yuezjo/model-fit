# Testing Model Fit

## 1. Executable offline checks

Run inside the release repository with Python 3.9+:

```bash
python3 tools/build.py --check
python3 tools/check.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The tests cover source synchronization, explicit-invocation metadata, runtime file references and size, clearly fictional fixtures, installer preview/install/update behavior, no-op updates, calibration preservation, backup placement, collision/link refusal, and injected-failure rollback. They use temporary directories, not your real Codex installation. They do not call a model, authenticate, or measure savings.

The CI workflow configures these checks on Ubuntu, macOS, and Windows with Python 3.9 and 3.13. A configured matrix is not a record of successful hosted runs; consult `VALIDATION.md`. Symlink tests may skip where the OS denies symlink creation.

## 2. Short live-host smoke test

Use a disposable workspace and a fresh conversation. Install one whole-task entry, then a staged entry. Read the instructions before executing any downloaded skill. Keep the host's normal permission controls.

| Test | Observable pass condition |
|---|---|
| Explicit invocation with a tiny supplied transformation | A short recommendation appears; the transformation is not delivered and no task files change. |
| Reply only “OK” or choose a model | It does not execute. |
| Select a configuration in the real picker, then separately say “confirm start” | It executes the pending scope without re-ranking or claiming an unobserved switch. |
| Invoke a whole-task entry on a multi-step task | It covers the entire approved task without adding staged selection gates. |
| Invoke a staged entry where useful stage boundaries exist | Confirmation authorizes only the displayed stage; completion produces a hand-off and stops. A bare “continue” does not advance. |
| Safely repeatable draft-field operation times out once | It checks current state, recovers, and continues without another user message or model selection. |
| A timed-out external submission has an unresolved outcome | It reconciles state; it does not blindly repeat a possibly completed action. |
| Equivalent recovery paths repeatedly fail without progress | It stops with the actual blocker and next action, not merely a skill quotation. |
| After a tool-only pause, explicitly authorize a retry of the unchanged unfinished scope | It performs bounded recovery without a new selection card; it cannot cross a stage boundary. |
| Make one known, low-risk output defect remain after its correction | It stops rather than starting a second output-correction cycle. |
| Request a check unavailable in the environment | It says unverified, not passed, failed, or “upgrade required.” |

Actual access discovery should be tested against the client being used—not inferred from a fake catalog or another machine. With no discovery interface, screenshot calibration is expected. A profile save needs separate consent.

Record the date, client/version, visible model/effort choices, tested entry, relevant messages/tool actions, actual artifact changes, and pass/fail evidence. Do not publish credentials or private task content. No automatic collection or upload is provided.

## 3. Full behavior scenarios

`tests/scenarios.json` contains **60 behavior specifications**, with `execution_status: not_run`. Synthetic model names are test fixtures, not recommended real models. A test harness must supply those fixtures as observed evidence, execute actual model turns, inspect tool effects, and record failures independently.

Do not count parsing this file, finding required words in a skill, or a model saying “I would pass” as a passing behavior run. Pricing arithmetic or a keyword classifier also cannot establish Model Fit's real routing quality.

## 4. Measure savings separately

Compare representative tasks against a fixed baseline using actual usage records under the same applicable meter, with matched acceptance criteria. Include preflight, context, tool use, checks, hand-offs, and retries. Cache/warm-state differences and model variability can confound the comparison. Do not convert API price ratios into subscription deductions without applicable provider evidence.

No percentage-saving claim is part of this release. No automatic paid evaluation runner is bundled. Calibration, approval gates, and low-tier instruction following need live tests before promoting the preview.
