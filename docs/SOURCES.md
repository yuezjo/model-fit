# Implementation references

Documentation inspected on **2026-09-09**. These links support platform and cost concepts, not proof of any particular user's access or measured savings. Model Fit's confirmation rules, correction limit, profile format, and storage paths are project design decisions.

## S1 — Skill structure, discovery, and explicit invocation

OpenAI's skill documentation specifies `SKILL.md`, local skill directories, and `agents/openai.yaml`, including `policy.allow_implicit_invocation: false`. It currently recommends plugins for broader distribution. This preview provides local skill folders, not a published plugin.

```text
https://developers.openai.com/codex/skills/
https://learn.chatgpt.com/docs/build-skills
```

## S2 — Actual model and effort controls

The model documentation describes host-side model/effort selection and notes that available choices depend on client, sign-in, and rollout. The package therefore does not hardcode a live roster or claim to switch configuration.

```text
https://developers.openai.com/codex/models/
https://learn.chatgpt.com/docs/models
```

## S3 — Cost optimization

Request count, input/output volume, and model choice are distinct cost levers. The package's expected-total-usage comparison is a heuristic, not a provider billing formula.

```text
https://developers.openai.com/api/docs/guides/cost-optimization
```

## S4 — Usage and pricing

The current pricing documentation discusses usage controls, token/credit rates, and model-dependent consumption. No live prices or subscription conversion constants are copied into the runtime skills.

```text
https://developers.openai.com/codex/pricing/
https://learn.chatgpt.com/docs/pricing
```

## S5 — Planning and execution can use different models

The reasoning best-practices guide describes combining models for planning and defined execution. Its model-family examples are not adopted as a current model ranking or a fixed routing table.

```text
https://developers.openai.com/api/docs/guides/reasoning-best-practices
```

## S6 — Discovery is a host capability

Codex App Server documents `model/list` and supported effort metadata. That interface's existence is not proof that a plain skill can call it or that a generic catalog establishes all account entitlements. Model Fit contains no App Server adapter.

```text
https://developers.openai.com/codex/app-server/
https://learn.chatgpt.com/docs/app-server
```

Recheck applicable documentation before claiming compatibility with a new client or publishing a new release. Public documentation must not be used to fill gaps in a user's private availability evidence.


## S7 — Similar skills inspected for v0.2

Inspected on 2026-09-09. Concepts were independently adapted; no upstream implementation is vendored. Repository claims, stars, and test names are not adopted as proof of Model Fit behavior or savings.

```text
https://github.com/gitguffaw/codex-router
https://github.com/scottconverse/multi-model-routing-skill
https://github.com/scottconverse/multi-model-routing-skill/blob/main/install.py
https://raw.githubusercontent.com/scottconverse/multi-model-routing-skill/main/scripts/codex_models.sh
https://github.com/paulpas/agent-skill-router/blob/main/skills/agent/ai-model-selector/SKILL.md
https://github.com/lm-sys/RouteLLM
https://github.com/zscole/model-hierarchy-skill
https://raw.githubusercontent.com/zscole/model-hierarchy-skill/main/tests/test_classification.py
```

Codex Router documents live model/effort discovery. The multi-model-routing project separates local facts and protects them during updates; its model-cache helper is historical-cache evidence, not a portable entitlement detector. AI Model Selector separates capability constraints and cost, but its mandatory cross-provider matrix is not adopted. RouteLLM emphasizes quality/cost trade-offs and workload evaluation, not guaranteed savings for this skill.

## S8 — Speed modes are not reasoning effort

The current official pricing documentation states that applicable speed configurations can increase usage/credit consumption. Model Fit only gives a conditional reminder when the active setting, available alternative, and relevant premium are actually known. No multiplier or model-specific price is hardcoded into the runtime.

```text
https://developers.openai.com/codex/pricing/
https://learn.chatgpt.com/docs/pricing
```

## S9 — Discovery fields have bounded meanings

The App Server model-list section documents picker-visible filtering, supported reasoning effort metadata, and nextCursor pagination. Catalog defaults are not claimed to be the active thread setting, and a model catalog is not used as a remaining-quota meter. Discovery requires an existing authorized host interface; v0.2 still ships no bridge or server.

```text
https://developers.openai.com/codex/app-server/
https://learn.chatgpt.com/docs/app-server
```
