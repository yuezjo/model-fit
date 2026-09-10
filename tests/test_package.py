"""Deterministic release tests, NOT model behavior tests."""
from __future__ import annotations
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build import render_outputs
from check import check_package

class PackageTests(unittest.TestCase):
    def test_generated_files_match(self):
        for rel, expected in render_outputs().items():
            self.assertEqual((ROOT / rel).read_text(encoding='utf-8'), expected)

    def test_release_integrity(self):
        self.assertEqual(check_package(ROOT), [])

    def test_behavior_registry_does_not_claim_pass(self):
        suite = json.loads((ROOT / 'tests/scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(suite['execution_status'], 'not_run')
        self.assertEqual(len({s['id'] for s in suite['scenarios']}), len(suite['scenarios']))

    def test_runtime_size_budget(self):
        for skill in (ROOT / 'skills').glob('*/SKILL.md'):
            self.assertLessEqual(len(skill.read_text(encoding='utf-8').split()), 950)

    def test_rejects_mutated_releases(self):
        mutations = {
            'implicit': ('skills/model-fit-goldilocks/agents/openai.yaml', lambda x: x.replace('false', 'true')),
            'wrong-name': ('skills/model-fit-goldilocks/SKILL.md', lambda x: x.replace('name: "model-fit-goldilocks"', 'name: "wrong-name"')),
            'unmarked-example': ('skills/model-fit-goldilocks/assets/availability.example.json', lambda x: x.replace('"example_only": true', '"example_only": false')),
            'reference': ('skills/model-fit-goldilocks/SKILL.md', lambda x: x.replace('(references/availability.md)', '(references/missing.md)')),
        }
        for label, (rel, mutate) in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                candidate = Path(temp) / 'candidate'
                shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git'))
                p = candidate / rel
                p.write_text(mutate(p.read_text(encoding='utf-8')), encoding='utf-8')
                self.assertTrue(check_package(candidate))

    def test_no_private_profile_in_release(self):
        for p in ROOT.rglob('*'):
            if p.is_file():
                self.assertNotIn(p.name, {'availability.json', 'auth.json', '.env'})

if __name__ == '__main__':
    unittest.main()
