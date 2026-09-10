# Changelog

## Public Preview publication preparation — 2026-09-10

- Retain `0.2.1-preview` and the four Goldilocks/Cheapskate entries. Runtime instructions, maintained policy sources, installer behavior, tools, and tests are unchanged from the supplied Goldilocks package.
- Organize complete English and Chinese README pages, installation/download guidance, feedback instructions, and bilingual release notes.
- Record new local offline checks separately from historical results and unexecuted model-behavior definitions.
- Prepare a GitHub pre-release with full-source and standalone-skills attachments. The owner approved public publication under MIT with copyright attribution to yuezjo; this preparation entry is not a publication-success record.

## Naming-only revision of 0.2.1-preview — Goldilocks

- Rename `model-fit-doitright` to `model-fit-goldilocks`, and `model-fit-doitright-staged` to `model-fit-goldilocks-staged`.
- Keep both `cheapskate` entries, all policies, and `VERSION` unchanged. Synchronize folders, metadata, display titles, source/build/installer identifiers, example calls, and test references.
- Document manual retirement of old-name installed folders; do not silently remove an installation or add legacy aliases. [Migration notes](docs/RENAME-GOLDILOCKS.md)
- The records below describe earlier changes. See [validation](VALIDATION.md) for checks of this naming-only package.

## 0.2.1-preview — 2026-09-09

### Fixed
- Separate bounded tool recovery from correction of completed output: safe local recovery no longer requires another user message or model recommendation, and does not consume the one-output-correction allowance.
- Remove unknown cause alone as a stop trigger; pause for persistent blockage, unresolved risky action outcomes, scope/authorization expansion, serious risk, or still-failing output correction.
- Reconcile action state before repetition and skip actions already completed. Never use recovery to bypass permissions or reset the same blocker indefinitely.
- Permit an explicitly requested retry of the same unfinished tool-blocked task/stage without new selection; preserve initial confirmation and next-stage gates.
- Explain the practical blocker and next action, rather than quoting skill policy by default.

### Validation
- Added 8 behavior specifications (60 total), including a safely recoverable field timeout, ambiguous external submission, persistent blockage, same-scope resume, and a stage-boundary negative case. None has yet run against a live model.
- This targeted patch responds to an anonymized user-reported v0.2 failure. The screenshot is evidence of the older experience, not proof of v0.2.1 behavior or of the timeout's underlying cause.

## 0.2.0-preview — 2026-09-09

### Added
- Optional standard-library installer: preview by default, backed-up updates, preserving private calibration and local additions, refusing unsafe destinations, and rollback tests.
- Conditional one-line warning for a known active premium-speed setting; speed is not conflated with reasoning effort.
- Executable offline regression tests and a maintainer CI workflow; expanded model-behavior specification from 36 to 52 cases (not executed).

### Improved
- Capability/access gates before consumption comparison; keeping a sufficient current setting and lowering effort within the same model are explicit options.
- Lightweight follow-up assessment, no extra lookup for clear tasks, no artificial scores or probabilities, no forced alternative.
- Availability evidence distinguishes current client/account picker results from public catalogs, historical caches, partial pagination, and another client's settings.
- First calibration accepts a useful partial list; v1 private profiles remain compatible.
- Stage hand-offs retain binding decisions, output references, and actual check status without claiming to clear context.
- Runtime instructions remain below their new 950-word review threshold; no fixed model or price table.
- English and Chinese entry instructions now lead with a default choice and the two-message workflow.

### Unchanged
Four entry names, explicit invocation only, manual model selection, mandatory separate execution confirmation, scope-bound stage approval, common acceptance standards, and the one-local-correction ceiling.

### Not added
Automatic delegation, cross-provider routing, live account reader/bridge, benchmark polling, mandatory scoring forms, telemetry, pricing calculators, and guaranteed savings. Live host/LLM behavior and savings remain unverified. License selection and publication are pending.

## 0.1.0-preview — 2026-09-09

Initial four-entry instruction-only package with private calibration conventions, explicit confirmation, optional staged workflows, shared generation sources, package checks, and 36 unexecuted behavior scenarios.
