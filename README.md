# Model Fit: Codex Skills for Model Selection

**Status: Public Preview · v0.2.2-preview**

[Chinese manual](README.zh-CN.md)

Model Fit is a collection of Codex skills for model selection and reasoning-effort advice. Before execution, it offers a short recommendation based on the options actually available to you. You choose the settings and confirm when to start. For work with distinct stages, it can reassess before each stage.

It is a selection adviser, not an automatic model-switching router.

## When to use it

Use Model Fit when a task involves enough judgment, uncertainty, or work that choosing a suitable configuration matters. It can help weigh the current configuration against other available choices without turning every task into a lengthy comparison.

For a trivial task or a clear follow-up with sufficient existing evidence, a separate selection step may add little value. Staging is optional, not the default.

## Install or update

Download a package from the [v0.2.2-preview pre-release](https://github.com/yuezjo/model-fit/releases/tag/v0.2.2-preview):

- **`model-fit-v0.2.2-preview.zip`**: the complete project, including all four skills, documentation, installer, maintained sources, tools, and tests.
- **`model-fit-v0.2.2-preview-skills.zip`**: all four standalone skill folders and the license, for manual installation.

There are no runtime dependencies. Extract the package and copy any complete skill folder into `~/.agents/skills/`. In the full package, the folders are under `skills/`; in the lightweight package, they are at the archive root. Keep `agents/`, `references/`, and `assets/` alongside each `SKILL.md`. Each entry can be installed independently.

For example: `~/.agents/skills/model-fit-goldilocks/SKILL.md`.

The optional installer in the **full package** requires Python 3.9+ with no additional packages. From the extracted project directory, preview the changes, then apply them:

```sh
python3 install.py
python3 install.py --apply
```

Use the same commands to update an installation. The installer backs up replaced files outside the skill scan directory and preserves private calibration. It does not change your host's model settings. For manual updates, back up the existing installation and preserve private calibration rather than replacing it with example data.

See [installation details](docs/INSTALL.md). Reload the client if an installed entry is not visible.

## One complete interaction

This is a format example, not a recorded model run.

**1. Invoke the skill with your task.**

```text
$model-fit-goldilocks Review the supplied report and make the requested comparison table.
```

**2. Read the recommendation.**

```text
Scope: Review the report and deliver the requested comparison table.
First choice: {available model} / {available effort} - Fits the judgment required.
Acceptance: Requested columns; conclusions traceable to the supplied evidence.
Reassess if: Missing evidence changes the scope.
Not started. Confirmation covers this whole task. Choose settings, then say "confirm start".
```

**3. Manually select model and effort in your client.** You may keep your current settings or choose differently from the recommendation. The skill does not switch them for you.

**4. Send a separate confirmation, without invoking the skill again.**

```text
confirm start
```

Another unambiguous instruction to execute also works. Selecting a model, saying "OK," asking why a configuration was recommended, or agreeing to save calibration does not itself authorize execution. An explicit skill invocation starts a fresh preflight and pauses again.

**5. Execution begins within the confirmed scope.** The assistant performs the task and checks the agreed acceptance criteria. In a staged entry, confirmation authorizes only the named current stage, not the entire project or the next stage.

## Choose an entry

Start with **`model-fit-goldilocks`**. Goldilocks is one entry's strategy, not the name of the full skill collection.

| Entry | Use it for |
| --- | --- |
| `model-fit-goldilocks` | A conservative recommendation for the whole task. The default starting point. |
| `model-fit-cheapskate` | A more budget-minded recommendation for the whole task. |
| `model-fit-goldilocks-staged` | Conservative advice with a separate recommendation and confirmation for each justified stage. |
| `model-fit-cheapskate-staged` | Budget-minded advice with the same stage-by-stage confirmation boundary. |

All four entries use confirmed available options, leave settings under your control, and require confirmation before execution. None guarantees the cheapest or best configuration.

## Preview status and feedback

Offline checks cover generated-file consistency, package integrity, and installer behavior. Current automated execution results are available in [GitHub Actions](https://github.com/yuezjo/model-fit/actions). See [validation scope](VALIDATION.md) for what those checks establish.

Actual selection quality, cross-model continuation, recovery behavior, and real-use consumption remain unverified. Written behavior scenarios and individual user feedback are not passing behavioral tests. Recommendations support your decision; they do not guarantee lower token use, allowance consumption, or cost.

This preview is packaged for local Codex skills. It does not promise universal platform support.

Report feedback through [Issues](https://github.com/yuezjo/model-fit/issues), including the version, client and environment, entry used, expected result, and actual result. Remove credentials, private calibration, personal conversations, and other sensitive information before sharing.

## License

[MIT](LICENSE). Copyright (c) 2026 yuezjo.
