#!/usr/bin/env python3
"""Build four self-contained skill folders from one maintained rule set.

Python 3.9+; standard library only. Does not install skills or touch user settings.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = (
    ("goldilocks", "whole-task", "Goldilocks", "Conservative model advice; confirm before execution"),
    ("cheapskate", "whole-task", "Cheapskate", "Budget-minded model advice; confirm before execution"),
    ("goldilocks", "staged", "Goldilocks · Staged", "Conservative model advice with stage-by-stage approval"),
    ("cheapskate", "staged", "Cheapskate · Staged", "Budget-minded model advice with stage-by-stage approval"),
)


def read_source(relative: str) -> str:
    return (ROOT / "sources" / relative).read_text(encoding="utf-8").strip()


def render_outputs() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    template = read_source("skill.template.md")
    for strategy, workflow, title, short_description in VARIANTS:
        name = f"model-fit-{strategy}" + ("-staged" if workflow == "staged" else "")
        scope = "the current stage of a justified staged workflow" if workflow == "staged" else "the whole submitted task"
        policy = "Conservative" if strategy == "goldilocks" else "Budget-minded"
        description = (
            f"Explicit model-selection preflight only. {policy} advice for {scope}; "
            "recommend available model/effort choices, then pause for confirmation."
        )
        values = {
            "NAME_YAML": json.dumps(name),
            "DESCRIPTION_YAML": json.dumps(description),
            "TITLE": f"Model Fit · {title}",
            "STRATEGY": read_source(f"strategies/{strategy}.md"),
            "WORKFLOW": read_source(f"workflows/{workflow}.md"),
            "CARD_RULES": ("Precede the card with the brief stage proposal; confirmation authorizes ONLY the named current stage." if workflow == "staged" else "State that confirmation covers the whole submitted task."),
            "COMPLETION": read_source(f"workflows/{workflow}-completion.md").replace("{{NAME}}", name),
        }
        text = template
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        if re.search(r"\{\{[A-Z_]+\}\}", text):
            raise ValueError(f"Unresolved template marker in {name}")
        base = Path("skills") / name
        outputs[base / "SKILL.md"] = text + "\n"
        prompt = f"Use ${name} to assess this task, recommend an available configuration, and stop before execution."
        outputs[base / "agents" / "openai.yaml"] = (
            "interface:\n"
            f"  display_name: {json.dumps('Model Fit · ' + title, ensure_ascii=False)}\n"
            f"  short_description: {json.dumps(short_description)}\n"
            f"  default_prompt: {json.dumps(prompt)}\n"
            "policy:\n"
            "  allow_implicit_invocation: false\n"
        )
        outputs[base / "references" / "availability.md"] = read_source("availability.md") + "\n"
        outputs[base / "assets" / "availability.example.json"] = read_source("availability.example.json") + "\n"
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale/missing generated files without writing")
    args = parser.parse_args()
    outputs = render_outputs()
    stale = []
    for relative, expected in outputs.items():
        destination = ROOT / relative
        if args.check:
            if not destination.is_file() or destination.read_text(encoding="utf-8") != expected:
                stale.append(str(relative))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(expected, encoding="utf-8")
    if stale:
        print("Generated files differ; run python3 tools/build.py:")
        print("\n".join(stale))
        return 1
    print(f"{'Verified' if args.check else 'Built'} {len(outputs)} files across {len(VARIANTS)} skill folders.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Build failed: {exc}") from exc
