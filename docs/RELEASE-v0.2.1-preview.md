# v0.2.1-preview — Public Preview

## English

Model Fit provides short model-and-reasoning-effort advice based on the choices actually available in the user's current client and account. The user selects settings manually and confirms before execution. It is a selection adviser, not an automatic router.

Start with `$model-fit-goldilocks`. The other entries are `$model-fit-cheapskate`, `$model-fit-goldilocks-staged`, and `$model-fit-cheapskate-staged`. Staged confirmation authorizes only the displayed current stage.

This Public Preview packages the confirmed Goldilocks naming revision of **0.2.1-preview**. Publication preparation updates documentation and release materials, without changing runtime instructions, installer behavior, or model-selection policies. See the [English README](../README.md) for a complete example and the [migration notes](RENAME-GOLDILOCKS.md) for older-name installations.

### Installation

- `model-fit-v0.2.1-preview-goldilocks.zip`: full repository. Extract it, enter `model-fit`, run `python3 install.py` to preview, then `python3 install.py --apply` to install/update. The optional installer requires Python 3.9+.
- `model-fit-v0.2.1-preview-goldilocks-skills.zip`: four complete standalone skill folders plus the release license. Copy the desired folders to `~/.agents/skills/`, preserving supporting files. No runtime dependencies are required.

### Preview evidence and limits

Build consistency, package integrity, and 33 offline tests passed on macOS 27.0 (arm64), Python 3.9.6, with no skips. Historical Linux/Python 3.13.5 results are recorded separately. See [VALIDATION.md](../VALIDATION.md).

All 60 model-behavior scenarios remain unexecuted. Actual selection quality, cross-model continuation, confirmation/recovery behavior, and real usage consumption remain unverified. An earlier real-use report is not a passing test of the resulting fix. Recommendations do not guarantee fewer tokens, lower allowance use, or reduced fees. Compatibility targets local Codex, not every platform. Check the repository's Actions tab for actual hosted CI status.

Report the version, entry, environment, expected and actual behavior, and a minimal reproduction in Issues. Remove sensitive data before sharing.

License: [MIT](../LICENSE). Copyright (c) 2026 yuezjo. Both attachments include the license.

## 中文

Model Fit 根据用户当前客户端与账号实际可用的配置，提供简短的模型和推理档位建议。用户手动选择并确认后才执行。它是选档顾问，不是自动路由器。

默认使用 `$model-fit-goldilocks`。其余入口为 `$model-fit-cheapskate`、`$model-fit-goldilocks-staged`、`$model-fit-cheapskate-staged`；分段版的确认只授权当前展示的阶段。

本次 Public Preview 发布已确认的 **0.2.1-preview** Goldilocks 更名版。发布准备只整理文档与发布材料，不改变运行指令、安装器行为或选档策略。完整示例见[中文 README](../README.zh-CN.md)，旧名安装的更换方式见[迁移说明](RENAME-GOLDILOCKS.md)。

### 安装

- `model-fit-v0.2.1-preview-goldilocks.zip`：完整项目。解压进入 `model-fit`，先运行 `python3 install.py` 预览，再运行 `python3 install.py --apply` 安装或更新。可选安装器需要 Python 3.9+。
- `model-fit-v0.2.1-preview-goldilocks-skills.zip`：四个完整独立 skill 文件夹及本次发布的许可证。将需要的文件夹复制到 `~/.agents/skills/`，保留支持文件。没有运行时依赖。

### 预览证据与限制

本次在 macOS 27.0（arm64）、Python 3.9.6 下，构建一致性、包检查和 33 项离线测试均通过，无跳过。历史 Linux/Python 3.13.5 结果单独保留，详见 [VALIDATION.md](../VALIDATION.md)。

60 个模型行为场景仍未运行。实际选档质量、跨模型接续、确认与恢复行为，以及真实使用消耗尚未验证。此前真实使用反馈不等于相应修复已通过测试。建议不保证减少 token、额度或费用；兼容目标为本地 Codex，不承诺所有平台通用。线上 CI 的实际状态请查看仓库 Actions 页面。

反馈时请在 Issues 提供版本、入口、环境、预期与实际表现及最小复现，并移除敏感信息。

许可证：[MIT](../LICENSE)。Copyright (c) 2026 yuezjo。两个附件均包含许可证。
