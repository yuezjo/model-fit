# Testing

Run these commands from the project root with Python 3.9+:

```sh
python3 tools/build.py --check
python3 tools/check.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

No third-party packages are required. Installer tests use temporary directories, not personal skill settings.

## Maintained sources

Edit the shared instructions under `sources/`, then regenerate the four standalone entries:

```sh
python3 tools/build.py
```

Commit the maintained sources and generated outputs together. Do not edit generated skill files independently or relax checks to accommodate a failing release.

## Behavior fixtures

`tests/scenarios.json` defines intended conversation behavior. These definitions are not executed by the offline unit suite, and their status remains `not_run`.

For an actual behavior evaluation, record the exact commit, client, available model and effort, input sequence, observed response, and pass or failure against the stated expectations. Remove private information before sharing results. Do not infer selection quality, continuation reliability, or savings from package checks.

See [validation scope](../VALIDATION.md) and the actual [CI runs](https://github.com/yuezjo/model-fit/actions).
