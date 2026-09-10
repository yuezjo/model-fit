#!/usr/bin/env python3
"""Check package integrity; this does NOT run model behavior evaluations.

The metadata check accepts the intentionally narrow YAML shape produced by build.py.
Python 3.9+; standard library only; no network or writes to personal settings.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from build import ROOT, VARIANTS, render_outputs


def check_package(root: Path) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    expected_outputs = render_outputs()
    for relative, expected in expected_outputs.items():
        path = root / relative
        require(path.is_file(), f"Missing generated file: {relative}")
        if path.is_file():
            require(path.read_text(encoding="utf-8") == expected, f"Stale or altered generated file: {relative}")

    expected_names = {
        f"model-fit-{strategy}" + ("-staged" if workflow == "staged" else "")
        for strategy, workflow, _, _ in VARIANTS
    }
    actual_names = {p.name for p in (root / "skills").iterdir() if p.is_dir()} if (root / "skills").is_dir() else set()
    require(actual_names == expected_names, "Skill folder set does not match the four variants")

    for name in sorted(expected_names):
        base = root / "skills" / name
        skill = base / "SKILL.md"
        if not skill.is_file():
            continue
        text = skill.read_text(encoding="utf-8")
        parts = text.split("---\n", 2)
        require(len(parts) == 3 and parts[0] == "", f"Invalid frontmatter delimiters: {name}")
        if len(parts) == 3:
            try:
                metadata = {k: json.loads(v.strip()) for k, v in (line.split(":", 1) for line in parts[1].splitlines() if line.strip())}
                require(metadata.get("name") == name, f"Name mismatch: {name}")
                require(set(metadata) == {"name", "description"}, f"Unexpected frontmatter keys: {name}")
                require(isinstance(metadata.get("description"), str) and bool(metadata["description"]), f"Missing description: {name}")
                require(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)) and len(name) <= 64, f"Invalid skill name: {name}")
            except (ValueError, TypeError, KeyError) as exc:
                errors.append(f"Invalid generated metadata in {name}: {exc}")
        require(len(text.split()) <= 950, f"Root instructions exceed the release's 950-word review threshold: {name}")
        require(not re.search(r"\{\{[A-Z_]+\}\}", text), f"Unexpanded build marker: {name}")
        require(not re.search(r"\bgpt-\d|\bAstra\b", text), f"Hardcoded real-model roster in runtime policy: {name}")

        ui = base / "agents" / "openai.yaml"
        if ui.is_file():
            ui_text = ui.read_text(encoding="utf-8")
            require("\npolicy:\n  allow_implicit_invocation: false\n" in ui_text, f"Implicit invocation is not disabled: {name}")
            require(f"${name}" in ui_text, f"Default prompt does not invoke its own skill: {name}")
            for line in ui_text.splitlines():
                if line.strip().startswith(("display_name:", "short_description:", "default_prompt:")):
                    try:
                        value = json.loads(line.split(":", 1)[1].strip())
                        require(isinstance(value, str) and bool(value), f"Invalid UI scalar: {name}")
                        if line.strip().startswith("short_description:"):
                            require(25 <= len(value) <= 64, f"UI summary length outside review range: {name}")
                    except ValueError:
                        errors.append(f"Invalid quoted UI scalar: {name}")

        for document in base.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                destination = (document.parent / target.split("#", 1)[0]).resolve()
                require(destination.is_file(), f"Broken skill-local link: {document.relative_to(root)} -> {target}")
                require(base.resolve() in destination.parents, f"External runtime dependency: {document.relative_to(root)} -> {target}")
        example = base / "assets" / "availability.example.json"
        if example.is_file():
            try:
                data = json.loads(example.read_text(encoding="utf-8"))
                require(data.get("schema_version") == 1 and data.get("example_only") is True, f"Unmarked example profile: {name}")
                for profile in data.get("profiles", []):
                    require(profile.get("coverage") in {"partial", "complete"}, f"Invalid example coverage: {name}")
                    require(profile.get("cost_basis") in {"unknown", "subscription_allowance", "api_billing"}, f"Invalid cost basis: {name}")
                    seen = set()
                    for cfg in profile["configurations"]:
                        require(isinstance(cfg.get("model"), str) and cfg["model"].startswith("Example "), f"Non-synthetic example model: {name}")
                        require(cfg.get("effort") is None or isinstance(cfg["effort"], str), f"Invalid example effort: {name}")
                        require(cfg.get("status") in {"available", "temporarily_unavailable"}, f"Invalid example status: {name}")
                        pair = (cfg.get("model"), cfg.get("effort"))
                        require(pair not in seen, f"Duplicate example combination: {name}")
                        seen.add(pair)
            except (ValueError, KeyError, TypeError) as exc:
                errors.append(f"Invalid example in {name}: {exc}")

    scenario_file = root / "tests" / "scenarios.json"
    if scenario_file.is_file():
        try:
            suite = json.loads(scenario_file.read_text(encoding="utf-8"))
            require(suite.get("execution_status") == "not_run", "Scenario specification must not claim execution results")
            ids = []
            for case in suite["scenarios"]:
                ids.append(case["id"])
                require(set(case["variants"]).issubset(expected_names) and bool(case["variants"]), f"Bad variants: {case['id']}")
                require(bool(case["messages"]) and bool(case["expected"]) and bool(case["forbidden"]), f"Incomplete scenario: {case['id']}")
            require(len(ids) >= 24 and len(ids) == len(set(ids)), "Missing or duplicate behavior scenario IDs")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"Invalid scenario registry: {exc}")
    else:
        errors.append("Missing behavior scenario specification")

    for relative in ("README.md", "README.zh-CN.md", "docs/TESTING.md", "docs/SOURCES.md", "docs/RELEASE_CHECKLIST.md", ".gitignore"):
        require((root / relative).is_file(), f"Missing documentation: {relative}")
    for path in root.rglob("*"):
        if path.is_file():
            require(path.name not in {"availability.json", "auth.json", ".env"} and not path.name.endswith(".local.json"), f"Potential private config in release: {path.relative_to(root)}")
    for filename in ("build.py", "check.py"):
        try:
            compile((root / "tools" / filename).read_text(encoding="utf-8"), filename, "exec")
        except SyntaxError as exc:
            errors.append(f"Python syntax error: {exc}")
    return errors


def main() -> int:
    errors = check_package(ROOT)
    if errors:
        print("PACKAGE CHECK FAILED\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    cases = json.loads((ROOT / "tests/scenarios.json").read_text(encoding="utf-8"))["scenarios"]
    print(f"PASS: four standalone skill folders, generated synchronization, metadata, references, example data, and {len(cases)} scenario definitions.")
    print("Behavior scenarios: NOT RUN. Host installation, model-switch continuation, and savings: NOT VERIFIED.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as exc:
        sys.exit(f"Package check could not complete: {exc}")
