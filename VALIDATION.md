# Validation record — v0.2.1-preview Public Preview

## Publication preparation — 2026-09-10

Source: the complete supplied `model-fit-v0.2.1-preview-goldilocks.zip`, containing 48 files and `VERSION` equal to `0.2.1-preview`. It contains no `.git` directory or commit history. A separate local publication repository imports no unrelated project history.

Source archive SHA-256:

```text
8583d020f2901ba45e2f59d928db3ecc5e619ac7fe9bba879c504e11aeeafa97
```

Environment: **macOS 27.0, arm64, Python 3.9.6**. These commands were independently run on the extracted supplied source during publication preparation:

| Command | Actual result |
|---|---|
| `python3 tools/build.py --check` | PASS: 16 generated files across four entries match maintained sources. |
| `python3 tools/check.py` | PASS: package integrity and structure of 60 behavior definitions. |
| `python3 -m unittest discover -s tests -p 'test_*.py' -v` | PASS: 33 tests, no failures or skips. |

The [publication-check transcript](docs/PUBLIC-PREVIEW-CHECKS.txt) records commands, environment, results, and additional release-candidate checks. Publication preparation preserves `VERSION`, `skills/`, `sources/`, `install.py`, `tools/`, and `tests/` byte-for-byte against this source. Only publication documentation, evidence, and repository metadata are eligible to change.

**Not verified:** all 60 live model-behavior scenarios, actual selection quality, cross-model continuation, real-client confirmation/recovery/stage behavior, and token, allowance, or fee savings. One earlier field report motivated the recovery patch; it is not proof that the patch works. There is no evidence here of an ongoing live evaluation.

The CI matrix targets Ubuntu, macOS, and Windows with Python 3.9 and 3.13. Its presence does not establish a hosted pass. This record describes local preparation, not successful publication or an Actions run. The owner approved public publication under the MIT License with copyright attribution to yuezjo before the release commit was created. The approved [license](LICENSE) is included in both release attachments.

## Historical record: Goldilocks naming revision

The record below and its [original offline transcript](docs/OFFLINE-TEST-RESULTS.txt) are preserved from the supplied archive. They describe the earlier Linux package-building session, not this macOS run. Historical statements about publication, installation, and licensing apply to that session.

**Naming-only revision.** `VERSION` remains `0.2.1-preview`. The supplied original v0.2.1 archive is the comparison source; no prior or later behavior version was substituted.

Environment: artifact-building Linux container, Python **3.13.5**. These checks did not install anything on the user's device, publish to GitHub, or call a model.

## Checks completed for the renamed package

| Check | Result |
|---|---|
| Original-archive runtime comparison | PASS — all **16 runtime files** match the original after only `doitright` → `goldilocks` and `Do It Right` → `Goldilocks` substitutions, including mapped directory names. |
| Policy and code preservation | PASS — **16 source/code/test/version files** also match after name-only substitutions. Strategy and shared workflow contents are unchanged. No automatic migration or retry changes were added. |
| Unchanged entries | PASS — both `cheapskate` folders are byte-for-byte identical to the original v0.2.1 files. |
| Deterministic generation / package checker | PASS — four folders, 16 generated files, metadata, references, synthetic fixtures, and scenario-registry shape agree. |
| Executable offline regression suite | PASS — all **33 tests**, no skips. These cover installer/filesystem and package behavior, not LLM behavior. |
| Metadata / UI parsing | PASS — four frontmatters and four UI files independently parsed with PyYAML; invocation names match their folders and implicit invocation remains disabled. |
| Runtime name/reference audit | PASS — no old names in runtime folders, maintained sources, build/install identifiers or test references. Old names remain only where documentation explains the rename or migration. |
| Standalone folder checks | PASS — each skill copied in isolation; its local runtime references stay inside that folder. This does not test client discovery. |
| Original-v0.2.1 manual migration | PASS in a temporary installation — follow the documented backup-and-install procedure; exactly four new-name/current entries remain active, previous folders and local additions are preserved, and synthetic private calibration is unchanged. A repeated installer preview is a no-op. The installer itself does not retire old-name folders. |
| Documentation links | PASS — local Markdown links resolve, with template links validated in their generated locations. |
| Final ZIP re-extraction | PASS — full archive re-extracted; generation check, package check and all 33 offline tests rerun. Skill-only archive checked byte-for-byte against its matching full-package files. |

Commands:

```bash
python3 tools/build.py --check
python3 tools/check.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The [offline transcript](docs/OFFLINE-TEST-RESULTS.txt) records this renamed package's regression run. Original-archive comparisons, YAML parsing, isolated reference checks and the documented manual-migration simulation were additional local checks.

Original supplied archive SHA-256:

```text
52cd3fc2075dc1e143b9fbe3606881cc3c45069c4d2fa13fd530e5343a88795d
```

## Runtime instruction sizes

Whitespace-delimited words and UTF-8 bytes, **not** token counts or billing measurements. The title replacement accounts for the word-count change; policy text is unchanged.

| Entry | Words | Bytes |
|---|---:|---:|
| `model-fit-cheapskate` | 855 | 6237 |
| `model-fit-cheapskate-staged` | 947 | 6890 |
| `model-fit-goldilocks` | 845 | 6180 |
| `model-fit-goldilocks-staged` | 937 | 6833 |

## Not verified

**All 60 live model-behavior scenarios remain NOT RUN.** Only their structure and renamed entry references were checked. This naming-only change does not establish reliable model selection, safe tool recovery, confirmation gates across model switches, stage/correction boundaries, or actual allowance savings in a client.

The earlier screenshots motivated the v0.2.1 recovery patch; they are not evidence that this renamed package passed a live recovery test. See the [v0.2.1 fix](docs/FIX-v0.2.1.md) and [live test guide](docs/TESTING.md).

No GitHub publication, hosted CI execution, license selection or deployment to the user's device is claimed. This remains a **local-trial preview**, not a runtime-validated stable release. Follow the [rename notes](docs/RENAME-GOLDILOCKS.md) when retiring old-name installed folders.
