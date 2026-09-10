"""Offline filesystem tests; these do not run Codex or any model."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.source = self.base / 'release'
        shutil.copytree(ROOT / 'skills', self.source / 'skills')
        self.target = self.base / 'user' / '.agents' / 'skills'
        self.name = install.NAMES[0]

    def plan(self, names=None):
        return install.make_plan(self.source, self.target, names or [self.name])

    def initial_install(self):
        install.apply_plan(self.plan())
        return self.target / self.name

    def old_install(self):
        dest = self.initial_install()
        skill = dest / 'SKILL.md'
        skill.write_text(skill.read_text(encoding='utf-8') + '\nOld local release.\n', encoding='utf-8')
        return dest

    def test_preview_writes_nothing(self):
        plan = self.plan()
        self.assertEqual(plan[0].action, 'install')
        self.assertFalse(self.target.parent.exists())

    def test_install_one_complete_folder(self):
        dest = self.initial_install()
        for relative in install.PAYLOAD:
            self.assertEqual((dest / relative).read_bytes(), (self.source / 'skills' / self.name / relative).read_bytes())
        self.assertEqual([p.name for p in self.target.iterdir()], [self.name])

    def test_install_all_four(self):
        install.apply_plan(self.plan(install.NAMES))
        self.assertEqual({p.name for p in self.target.iterdir()}, set(install.NAMES))

    def test_identical_install_is_noop(self):
        self.initial_install()
        plan = self.plan()
        self.assertEqual(plan[0].action, 'keep')
        self.assertIsNone(install.apply_plan(plan))
        self.assertFalse((self.target.parent / 'model-fit-backups').exists())

    def test_upgrade_backup_is_outside_scan_root(self):
        dest = self.old_install()
        old = (dest / 'SKILL.md').read_bytes()
        backup = install.apply_plan(self.plan())
        self.assertIsNotNone(backup)
        self.assertNotIn(self.target, backup.parents)
        self.assertEqual((backup / self.name / 'SKILL.md').read_bytes(), old)
        self.assertEqual((dest / 'SKILL.md').read_bytes(), (self.source / 'skills' / self.name / 'SKILL.md').read_bytes())

    def test_extra_user_files_are_preserved(self):
        dest = self.old_install()
        (dest / 'personal-note.txt').write_text('keep me', encoding='utf-8')
        backup = install.apply_plan(self.plan())
        self.assertEqual((dest / 'personal-note.txt').read_text(encoding='utf-8'), 'keep me')
        self.assertTrue((backup / self.name / 'personal-note.txt').is_file())

    def test_private_calibration_untouched(self):
        profile = self.base / 'user' / '.config' / 'model-fit' / 'availability.json'
        profile.parent.mkdir(parents=True)
        data = b'{"synthetic-test-only": true}\n'
        profile.write_bytes(data)
        self.old_install()
        install.apply_plan(self.plan())
        self.assertEqual(profile.read_bytes(), data)

    def test_unrelated_collision_refused(self):
        dest = self.target / self.name
        dest.mkdir(parents=True)
        (dest / 'important.txt').write_text('keep', encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan()
        self.assertEqual((dest / 'important.txt').read_text(encoding='utf-8'), 'keep')

    def test_wrong_skill_name_refused(self):
        dest = self.initial_install()
        (dest / 'SKILL.md').write_text('---\nname: "other"\n---\n', encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_git_checkout_refused(self):
        dest = self.initial_install()
        (dest / '.git').mkdir()
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_git_worktree_file_refused(self):
        dest = self.initial_install()
        (dest / '.git').write_text('gitdir: elsewhere', encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_source_target_overlap_refused(self):
        with self.assertRaises(install.InstallError):
            install.make_plan(self.source, self.source / 'skills', [self.name])

    def test_non_directory_target_refused(self):
        self.target.parent.mkdir(parents=True)
        self.target.write_text('not a directory', encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_unknown_name_refused(self):
        with self.assertRaises(install.InstallError):
            self.plan(['../../other'])

    def test_selection_deduplicated(self):
        self.assertEqual(len(self.plan([self.name, self.name])), 1)

    def test_source_missing_file_refused(self):
        (self.source / 'skills' / self.name / 'references/availability.md').unlink()
        with self.assertRaises(install.InstallError):
            self.plan()
        self.assertFalse(self.target.exists())

    def test_implicit_invocation_change_refused(self):
        ui = self.source / 'skills' / self.name / 'agents/openai.yaml'
        ui.write_text(ui.read_text(encoding='utf-8').replace('false', 'true'), encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_payload_directory_conflict_refused(self):
        dest = self.initial_install()
        (dest / 'references/availability.md').unlink()
        (dest / 'references/availability.md').mkdir()
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_all_targets_validated_before_any_apply(self):
        bad = self.target / install.NAMES[1]
        bad.mkdir(parents=True)
        (bad / 'do-not-touch').write_text('x', encoding='utf-8')
        with self.assertRaises(install.InstallError):
            self.plan(install.NAMES)
        self.assertFalse((self.target / self.name).exists())

    def test_update_failure_rolls_back_old_content(self):
        dest = self.old_install()
        before = (dest / 'SKILL.md').read_bytes()
        original = os.replace
        def fail_staged_once(src, dst):
            if '.model-fit-stage-' in str(src):
                raise OSError('synthetic replacement failure')
            return original(src, dst)
        with mock.patch.object(install.os, 'replace', side_effect=fail_staged_once):
            with self.assertRaisesRegex(install.InstallError, 'were restored'):
                install.apply_plan(self.plan())
        self.assertEqual((dest / 'SKILL.md').read_bytes(), before)
        self.assertFalse(list(self.target.parent.glob('.model-fit-stage-*')))

    def test_batch_failure_removes_new_partial_install(self):
        original = os.replace
        count = [0]
        def fail_second(src, dst):
            if '.model-fit-stage-' in str(src):
                count[0] += 1
                if count[0] == 2:
                    raise OSError('synthetic second install failure')
            return original(src, dst)
        with mock.patch.object(install.os, 'replace', side_effect=fail_second):
            with self.assertRaises(install.InstallError):
                install.apply_plan(self.plan(install.NAMES[:2]))
        self.assertFalse(self.target.exists())

    def make_symlink(self, target, link):
        try:
            link.symlink_to(target, target_is_directory=Path(target).is_dir())
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable in this test environment')

    def test_symlink_target_refused(self):
        elsewhere = self.base / 'elsewhere'
        elsewhere.mkdir()
        self.target.parent.mkdir(parents=True)
        self.make_symlink(elsewhere, self.target)
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_source_symlink_refused(self):
        src = self.source / 'skills' / self.name / 'SKILL.md'
        elsewhere = self.base / 'replacement.md'
        elsewhere.write_bytes(src.read_bytes())
        src.unlink()
        self.make_symlink(elsewhere, src)
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_symlink_inside_existing_skill_refused(self):
        dest = self.old_install()
        elsewhere = self.base / 'private.txt'
        elsewhere.write_text('do not read', encoding='utf-8')
        self.make_symlink(elsewhere, dest / 'link.txt')
        with self.assertRaises(install.InstallError):
            self.plan()

    def test_backup_symlink_refused(self):
        self.old_install()
        elsewhere = self.base / 'elsewhere'
        elsewhere.mkdir()
        self.make_symlink(elsewhere, self.target.parent / 'model-fit-backups')
        with self.assertRaises(install.InstallError):
            install.apply_plan(self.plan())
        self.assertFalse(list(elsewhere.iterdir()))

    def test_cli_preview_does_not_install(self):
        result = subprocess.run([sys.executable, str(ROOT / 'install.py'), '--target', str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Preview only', result.stdout)
        self.assertFalse(self.target.exists())

    def test_cli_install_selected_skill(self):
        result = subprocess.run([sys.executable, str(ROOT / 'install.py'), '--apply', '--target', str(self.target), '--skill', self.name], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / self.name / 'SKILL.md').is_file())
        self.assertEqual(len(list(self.target.iterdir())), 1)

if __name__ == '__main__':
    unittest.main()
