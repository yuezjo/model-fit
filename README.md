# Model Fit

**Status: Public Preview · v0.2.1-preview**

Short model-and-reasoning-effort advice before execution, based on the choices actually available in your current client and account. You select the settings and confirm; when useful, staged entries reassess before each stage.

Model Fit is a selection adviser, not an automatic model-switching router.

[完整中文说明](README.zh-CN.md) · [Release and downloads](https://github.com/yuezjo/model-fit/releases/tag/v0.2.1-preview)

## What it does

Describe a task with **`$model-fit-goldilocks`**, the recommended starting point. It checks required capabilities, recommends a suitable available model/effort combination, and pauses before execution. Keeping your current setting or lowering effort on the same model can be the recommendation. Alternatives appear only when useful.

You make the final choice. After a separate confirmation, the agent carries out the agreed task and reports what it actually checked. Model Fit supplies workflow instructions; it does not change client settings or enforce a system-level execution lock.

## When it is worth using

Use it when you have meaningful model/effort choices and want help matching them to a task's judgment, risk, and verification needs. It can also help when a larger task has clearly different stages worth reassessing separately.

For a tiny, obvious task, the extra assessment may cost more than it saves. With one fixed configuration, there is no selectable saving. The workflow is not limited to coding, but this package targets **local Codex skill installation**, not universal platform compatibility.

## Install or update

Choose an attachment from the [v0.2.1-preview pre-release](https://github.com/yuezjo/model-fit/releases/tag/v0.2.1-preview):

- **`model-fit-v0.2.1-preview-goldilocks.zip`**: complete repository, including documentation, installer, maintained sources, tools, and tests.
- **`model-fit-v0.2.1-preview-goldilocks-skills.zip`**: four standalone skill folders and the release license, for manual installation.

There are no runtime dependencies. Extract the package and copy any complete skill folder to `~/.agents/skills/`. In the full package the folders are under `skills/`; in the lightweight package they are at the archive root. Keep `agents/`, `references/`, and `assets/` alongside each `SKILL.md`. Each entry can be installed independently.

For example: `~/.agents/skills/model-fit-goldilocks/SKILL.md`.

The optional installer in the **full package** needs Python 3.9+ with no additional packages. From the extracted `model-fit` directory:

```bash
python3 install.py          # Preview only; changes nothing
python3 install.py --apply  # Install or update all four entries
```

Matching old folders are backed up outside the scanned skills directory; extra local files are preserved. The installer leaves private calibration and host model settings alone. It refuses unrelated folders, Git checkouts, symlinked paths, and file/directory conflicts. For manual updates, first back up the old folder outside the scan directory.

If entries do not appear, restart the client. Older-name installations should follow the [Goldilocks migration instructions](docs/RENAME-GOLDILOCKS.md). See [installation details](docs/INSTALL.md) for individual entries, project-local installation, restore, and removal.

## One complete use example

This is a **format example, not an executed test**. Braced model/effort names are placeholders, not a real availability list.

**1. Invoke the skill with your task.**

```text
$model-fit-goldilocks Review the supplied report and make the requested comparison table.
```

**2. Read the recommendation.**

```text
Scope: Review the report and deliver the requested comparison table.
First choice: {available model} · {available effort} — Fits the judgment required.
Acceptance: Requested columns; conclusions traceable to the supplied evidence.
Reassess if: Missing evidence changes the scope.
Not started. Confirmation covers this whole task. Choose settings, then say "确认开始".
```

**3. Manually select model and effort in your client.** You may keep your current settings or choose differently from the recommendation. The skill does not switch them for you.

**4. Send a separate confirmation, without the skill name.**

```text
确认开始
```

`confirm start` or another unambiguous execution instruction also works. Choosing a model, saying "OK," asking a question, or allowing a calibration save does not approve execution. Invoking `$model-fit-...` again starts another assessment and pause.

**5. The agent executes the agreed task.** In this example, it prepares the comparison table, checks the requested columns and evidence links, and reports the result and any checks it could not perform. This describes the intended workflow, not evidence of a live test.

### Available choices and private calibration

When the current client reliably exposes available model/effort pairs, the skill uses them. Otherwise, provide a picker screenshot or copied options; a confirmed subset is enough. A public model list, local cache, or another client's configuration does not establish access here.

With explicit permission and filesystem access, choices can be saved privately for all four entries. Account, client, or availability changes may require a refresh. Existing v0.1 profiles remain compatible. No credentials or task content are saved. No discovery bridge, background service, or paid probing call is bundled. See the [availability rules](skills/model-fit-goldilocks/references/availability.md).

## Choose an entry

Start with **`$model-fit-goldilocks`**. All four keep the same acceptance standard.

| Entry | Approach | A confirmation authorizes |
|---|---|---|
| `$model-fit-goldilocks` | Conservative selection with a well-supported expectation of completing the task | The whole submitted task |
| `$model-fit-cheapskate` | A plausible lower-consumption attempt for low-risk, reversible, readily checkable work | The whole submitted task |
| `$model-fit-goldilocks-staged` | Conservative selection for each worthwhile stage | Only the displayed current stage |
| `$model-fit-cheapskate-staged` | More aggressive selection where a stage's risk permits | Only the displayed current stage |

The entries may recommend the same setting. Ordinary entries do not propose staged switching. Staged entries use one stage when splitting is not worthwhile.

For staged work, confirmation accepts the displayed plan but authorizes **only the current stage**. After completing it, the agent provides a hand-off and the next invocation, then stops. Invoke that next stage and confirm again to begin it; a bare "continue" does not advance a completed stage. A hand-off does not clear chat history.

## Preview status

- **Recorded offline checks:** the supplied Goldilocks package records 33 passing tests on Linux/Python 3.13.5. This publication preparation independently ran the build check, package check, and all 33 offline tests on macOS 27.0 (arm64)/Python 3.9.6, with no skips. These test files and installer behavior, not live model behavior.
- **Not yet verified:** actual selection quality, confirmation and recovery behavior across model switches, staged continuation, and real usage consumption. All 60 model-behavior scenarios are definitions marked `not_run`. One earlier real-use report motivated the recovery change; it does not prove the change passed behavior testing. GitHub Actions configuration is not evidence of a successful hosted run.
- **Your decision:** recommendations do not guarantee fewer tokens, lower allowance use, reduced fees, or a fixed savings percentage. Assessment, context, checks, hand-offs, and rework also consume resources.

See [VALIDATION.md](VALIDATION.md) for current and historical evidence, environments, and unverified items. This publication preserves the supplied v0.2.1-preview runtime instructions, installer behavior, and selection policies.

## Feedback

Open an [issue](https://github.com/yuezjo/model-fit/issues) with the version and entry used, client/environment and relevant model/effort options, expected result, actual result, and a minimal reproduction. Include performed checks when helpful. Remove credentials, private calibration, account details, private task content, and sensitive screenshots before sharing.

## Maintenance and references

Normal use does not require the maintenance tools. See the [testing guide](docs/TESTING.md), [release checklist](docs/RELEASE_CHECKLIST.md), [changelog](CHANGELOG.md), and [implementation references and design acknowledgments](docs/SOURCES.md). Maintained `sources/`, generated `skills/`, tools, and tests remain included.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 yuezjo.
