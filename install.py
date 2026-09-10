#!/usr/bin/env python3
"""Preview or install local Codex skill folders; no network or host-config edits.

Python 3.9+ standard library. The default run is read-only; --apply opts into
installation. Existing skill folders are backed up OUTSIDE the skill scan root.
The user's private Model Fit calibration is never opened or overwritten.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path(__file__).resolve().parent
NAMES = (
    'model-fit-goldilocks',
    'model-fit-cheapskate',
    'model-fit-goldilocks-staged',
    'model-fit-cheapskate-staged',
)
PAYLOAD = (
    'SKILL.md',
    'agents/openai.yaml',
    'references/availability.md',
    'assets/availability.example.json',
)


class InstallError(Exception):
    """A safe-to-display installation validation or rollback error."""


@dataclass(frozen=True)
class PlannedSkill:
    name: str
    source: Path
    destination: Path
    action: str


def below(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def check_tree(path: Path) -> None:
    """Refuse links and non-regular payloads instead of following them."""
    if path.is_symlink() or not path.is_dir():
        raise InstallError(f'Expected an ordinary skill directory: {path}')
    if (path / '.git').exists() or (path / '.git').is_symlink():
        raise InstallError(f'Refusing to modify a Git checkout: {path}')
    for child in path.rglob('*'):
        if child.is_symlink():
            raise InstallError(f'Refusing to follow a symlink inside a skill: {child}')
        if not child.is_file() and not child.is_dir():
            raise InstallError(f'Unsupported filesystem object: {child}')


def skill_name(path: Path) -> Optional[str]:
    """Read only the narrow name field needed to recognize an earlier install."""
    skill = path / 'SKILL.md'
    if not skill.is_file() or skill.is_symlink():
        return None
    try:
        text = skill.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return None
    if not text.startswith('---\n'):
        return None
    header = text.split('---\n', 2)
    if len(header) < 3:
        return None
    for line in header[1].splitlines():
        if line.startswith('name:'):
            value = line.split(':', 1)[1].strip()
            if value.startswith('"'):
                try:
                    parsed = json.loads(value)
                    return parsed if isinstance(parsed, str) else None
                except ValueError:
                    return None
            return value.strip("'")
    return None


def make_plan(source_root: Path, target: Path, names: Iterable[str]) -> list[PlannedSkill]:
    """Validate every selected source/destination before making any changes."""
    source_root = source_root.expanduser().resolve()
    target = target.expanduser().absolute()
    # Check every existing component before resolve() could hide a symlink.
    for component in (target, *target.parents):
        if component.is_symlink():
            raise InstallError(f'Symlinked install path; use manual installation: {component}')
    target = target.resolve()
    if target.exists() and not target.is_dir():
        raise InstallError(f'Target is not a directory: {target}')
    if below(target, source_root) or below(source_root, target):
        raise InstallError('The install target and the release source must not overlap.')
    selected = list(dict.fromkeys(names))
    if not selected or any(name not in NAMES for name in selected):
        raise InstallError('Choose one or more of the four Model Fit skill names.')
    plan = []
    for name in selected:
        source = source_root / 'skills' / name
        destination = target / name
        check_tree(source)
        if skill_name(source) != name:
            raise InstallError(f'Source skill name does not match: {source}')
        for relative in PAYLOAD:
            if not (source / relative).is_file():
                raise InstallError(f'Missing release file: {source / relative}')
        ui = (source / 'agents/openai.yaml').read_text(encoding='utf-8')
        if '\npolicy:\n  allow_implicit_invocation: false\n' not in ui:
            raise InstallError(f'Explicit-only invocation policy is missing: {source}')
        action = 'install'
        if destination.exists() or destination.is_symlink():
            check_tree(destination)
            if skill_name(destination) != name:
                raise InstallError(f'Existing folder is not the matching Model Fit skill: {destination}')
            for relative in PAYLOAD:
                path = destination / relative
                if path.exists() and not path.is_file():
                    raise InstallError(f'File/directory conflict in existing install: {path}')
            action = 'keep' if all(
                (destination / relative).is_file()
                and (destination / relative).read_bytes() == (source / relative).read_bytes()
                for relative in PAYLOAD
            ) else 'update'
        plan.append(PlannedSkill(name, source, destination, action))
    return plan


def apply_plan(plan: list[PlannedSkill]) -> Optional[Path]:
    """Stage, back up and replace as a batch; roll back ordinary write failures.

The operation is local filesystem work, not an OS crash-proof transaction.
Call make_plan immediately before this function; do not mutate destinations
concurrently. Existing extra files are kept; changed release files are replaced.
"""
    changed = [item for item in plan if item.action != 'keep']
    if not changed:
        return None
    target = changed[0].destination.parent
    if any(item.destination.parent != target for item in changed):
        raise InstallError('All selected skills must use the same installation directory.')
    parent = target.parent
    backup_base = parent / 'model-fit-backups'
    if backup_base.is_symlink() or (backup_base.exists() and not backup_base.is_dir()):
        raise InstallError(f'Unsafe backup destination: {backup_base}')
    parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix='.model-fit-stage-', dir=str(parent)))
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = backup_base / f'{timestamp}-{uuid.uuid4().hex[:8]}'
    moved_old: list[PlannedSkill] = []
    installed: list[PlannedSkill] = []
    made_target = not target.exists()
    try:
        # Build complete replacements before touching the active folders.
        for item in changed:
            staged = stage_root / item.name
            if item.action == 'update':
                shutil.copytree(item.destination, staged)
            else:
                staged.mkdir()
            for relative in PAYLOAD:
                dest = staged / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item.source / relative, dest)
        target.mkdir(parents=True, exist_ok=True)
        if any(item.action == 'update' for item in changed):
            backup.mkdir(parents=True, exist_ok=False)
        for item in changed:
            if item.action == 'update':
                os.replace(item.destination, backup / item.name)
                moved_old.append(item)
        for item in changed:
            os.replace(stage_root / item.name, item.destination)
            installed.append(item)
    except Exception as exc:
        failures = []
        for item in reversed(installed):
            try:
                shutil.rmtree(item.destination)
            except OSError as rollback_exc:
                failures.append(str(rollback_exc))
        for item in reversed(moved_old):
            try:
                os.replace(backup / item.name, item.destination)
            except OSError as rollback_exc:
                failures.append(str(rollback_exc))
        if made_target and target.exists():
            try:
                target.rmdir()
            except OSError:
                pass
        if failures:
            raise InstallError(f'Install failed: {exc}. Rollback incomplete; preserve backups at {backup}. Details: {failures}') from exc
        raise InstallError(f'Install failed; prior skill folders were restored: {exc}') from exc
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)
        if backup.exists():
            try:
                backup.rmdir()  # Only removes an empty backup after rollback.
            except OSError:
                pass
    return backup if moved_old else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Install/update; without this flag only preview')
    parser.add_argument('--target', type=Path, default=Path.home() / '.agents' / 'skills', help='Skill directory (default: ~/.agents/skills)')
    parser.add_argument('--skill', action='append', choices=NAMES, help='Install only this skill; repeat to select several')
    args = parser.parse_args()
    try:
        plan = make_plan(ROOT, args.target, args.skill or NAMES)
        for item in plan:
            print(f'{item.action.upper():6} {item.destination}')
        if not args.apply:
            print('Preview only. No files changed. Add --apply to install these choices.')
            return 0
        backup = apply_plan(plan)
        if backup:
            print(f'Previous versions backed up outside the skill scan directory: {backup}')
        print('Done. No host model settings or private calibration were changed.')
        print('If a skill is not visible, restart the client. Client behavior is not verified by installation.')
        return 0
    except (InstallError, OSError, UnicodeError) as exc:
        print(f'Installation stopped: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
