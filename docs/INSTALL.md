# Installation and safe updates

Target: local Codex skill discovery. See [official references](SOURCES.md). A correctly copied folder does not prove model behavior in a live client.

**Changing from the previous `doitright` names?** Follow the [naming-only migration](RENAME-GOLDILOCKS.md) first. The unchanged installer matches folder names; it does not automatically retire differently named old entries.

## Manual

Copy any complete folder under `skills/` to `~/.agents/skills/`, or to `<project>/.agents/skills/` for a repository-local install. Do not copy only `SKILL.md`. Avoid installing the same name in multiple overlapping locations.

For updates, back up the old folder somewhere outside `.agents/skills/` before replacing release files. The optional installer below handles this for ordinary, non-symlinked local installations.

## Optional installer

Python 3.9+ standard library; no pip packages, network, host-config editing, or model calls.

```bash
python3 install.py
python3 install.py --apply
```

The first command previews. The second installs all four or updates existing matching folders. An identical install is left alone. Narrow the selection or target only when needed:

```bash
python3 install.py --apply --skill model-fit-goldilocks
python3 install.py --apply --target /absolute/project/.agents/skills
```

Existing release files are replaced; extra local files are preserved. Backups go under `<target-parent>/model-fit-backups/<timestamp-id>/`, not inside the scanned skill directory. The exact successful backup path is printed. Private calibration outside the install is never opened or changed.

The installer validates all selected destinations first. It stages replacement folders, backs up matching old folders, and attempts rollback on ordinary write failures. This is not a power-loss-safe transaction; do not edit the folders concurrently. If rollback cannot finish, preserve the reported backup directory and inspect it before retrying.

It refuses unknown skill names, unrelated existing directories, Git checkouts/worktrees, symlinked paths, and file/directory conflicts. Symlink users should manage their installation manually. It does not auto-detect or install into other clients, remove old backups, write credentials, or add a server.

## Restore or remove

Stop using the affected skill. Move its current folder aside, outside the scan root, then copy the matching backed-up folder into the original location. Do not leave both versions under scanned skill paths. Backups are not activated automatically.

To remove a locally copied skill, delete only its `model-fit-...` folder after preserving any personal additions. Calibration is separate and remains unless you explicitly remove it. There is no bundled destructive uninstall command.
