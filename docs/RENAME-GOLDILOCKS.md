# Goldilocks rename — v0.2.1-preview

This is a **naming-only revision** of v0.2.1-preview, not a behavior update. The version remains `0.2.1-preview`; archive filenames include `goldilocks` to distinguish this package from the earlier names.

| Previous invocation | Current invocation |
|---|---|
| `$model-fit-doitright` | `$model-fit-goldilocks` |
| `$model-fit-cheapskate` | `$model-fit-cheapskate` |
| `$model-fit-doitright-staged` | `$model-fit-goldilocks-staged` |
| `$model-fit-cheapskate-staged` | `$model-fit-cheapskate-staged` |

Only names and their references changed: skill folders, metadata, display titles, example invocations, stage hand-off invocations, strategy-source filename, installer choices, generation mappings, and test references. Selection policies, confirmation gates, stage boundaries, availability calibration, and the v0.2.1 recovery/correction rules are unchanged. No compatibility-alias skills were added.

## Already installed with the previous names?

Before installing this package, move the complete `model-fit-doitright` and `model-fit-doitright-staged` folders **outside every scanned skills directory** as backups. For the standard local layout, a separate folder under `~/.agents/model-fit-backups/` is suitable; do not leave the backups inside `~/.agents/skills/`.

Then install the desired new folders normally, by copying the complete folders or using the installer preview followed by `--apply`. The installer only updates matching names: **it does not automatically migrate or remove the two differently named old folders**. The two `cheapskate` folders from v0.2.1 are byte-for-byte unchanged and may stay in place. Private availability calibration does not need to be reset.

Preserve any personal additions in the backups. Copy additional personal files into the corresponding new folder only as needed; do not overwrite its four bundled runtime files with the old versions. Review edits made inside old runtime files separately. Do not merely rename an installed folder: its metadata and invocation references also need the new package.

Verify the chosen new entries are visible and no old-name entries remain in the relevant install locations. Existing conversations may still contain old instructions; reload the new skill or use a fresh conversation. No installation on your device has been performed by creating this archive.

## 中文：已有旧名版本时怎么更换？

这次只更名，仍是 **v0.2.1-preview**，没有修改选档、确认、分段或安全重试规则。

先把旧的 `model-fit-doitright` 和 `model-fit-doitright-staged` **完整文件夹移到 skills 扫描目录之外备份**，再正常安装新包。标准本地目录可以把备份放在 `~/.agents/model-fit-backups/` 下的独立文件夹中，不要留在 `~/.agents/skills/` 内。

**安装器不会自动迁移或删除这两个旧名文件夹。**两个 `cheapskate` 的 v0.2.1 文件完全不变，可以保留；私人可用模型校准也不需要重做。已有个人附加文件先保存在备份里，再按需移入对应的新文件夹，别用旧版自带文件覆盖新版。只改安装文件夹名还不够，里面的名称和引用也要使用新包。

最后确认所选新入口已出现、旧入口不再被加载。旧对话可能仍保留旧指令，使用时重新加载新 skill 或新开对话。本包没有替你操作设备上的实际安装。
