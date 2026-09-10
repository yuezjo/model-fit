# v0.2.1 — 恢复工具，不为小卡顿增加确认 / Recover tools without needless approval

## 用户可见的变化

已确认执行后，普通工具卡顿先在原授权内做简短、安全的恢复；成功就继续。通常为同一阻塞尝试一两次有意义的重试或已允许的等价路径，不把每次检查都机械算作一次失败，也不靠换路径不断重置预算。原因暂不清楚，本身不构成停工理由。

**执行前确认仍然保留。**恢复仅在已获准范围内，不扩大权限，不跨过分段结束的关卡。预判仍然只读，不因这个补丁提前执行任务。

## 这次改了什么

1. **工具恢复与交付修正分开。**读取失败、输入超时等可安全恢复的小故障，不占用交付结果未通过验收后的那一次修正。
2. **先确认动作结果，再决定重试。**能看到目标结果已经完成，就继续，不重做。发送、提交等动作结果不明时，只有能够确认结果或确保安全重复才继续，否则暂停；不把超时当作“没有发生”。
3. **真正受阻才问用户。**短暂恢复后仍无进展、需要扩大范围/授权、出现新的重大风险，或交付修正仍不通过才暂停。原本就缺少的用户资料仍需询问，不能为了不暂停而编造。
4. **暂停说实际问题。**说明观察到的失败、当前状态、所需下一步；用户主动问规则时再解释规则。工具暂停后，明确的继续/重试可授权同一未完成范围内的新一轮有限恢复，不必重新选档。

普通版和分段版、稳妥和省量策略共用这项恢复规则；不增加新开关、新入口或用户配置。更新方式与 v0.2 相同。

## Why this patch

The previous stop clause coupled an unexplained operational failure to a whole-task pause. A user report showed a draft-field timeout, a policy-based stop, and success after the user requested another attempt. The cause of the timeout and the full tool trace are unknown; this is not a controlled reproduction. The policy was nonetheless missing a clear path for bounded, safe operational recovery.

The patch changes the common execution section, not the model-selection logic. It retains the existing limit for correction of completed output, and it does not permit replaying uncertain external actions or pushing past authorization boundaries.

The usual one-or-two recovery attempts are a design guideline, not a billing estimate, a universal optimum, or a count of every read/check tool call. The same persistent blocker remains the same blocker across equivalent paths.

## Regression evidence

The behavioral regression definitions are `MF-53`–`MF-60` in [scenarios.json](../tests/scenarios.json). The field-reporting example is generalized; no private screenshots, account identifiers, or user profile details are shipped.

File consistency and installer regression results are in [VALIDATION.md](../VALIDATION.md). These checks do not establish live-model compliance. The updated timeout/recovery behavior still needs a real-client or tool-fixture trial.

## Technical references

- [OpenAI's Codex prompting reference](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/openai-docs/references/prompting-guide.md): current guidance notes that unclear or conflicting skill instructions can trigger early pauses. We apply a targeted execution-rule change, not a blanket instruction to ignore confirmations.
- [AWS: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/): transient retries can help, but unknown outcomes and duplicate side effects require reconciliation or safe repeatability.

References inspected 2026-09-09. These support design principles, not a claim that Model Fit's retry policy has passed live evaluation.
