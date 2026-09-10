# Validation scope

## Offline checks

The repository includes deterministic checks for generated-file consistency, skill metadata and local references, synthetic availability data, package integrity, and installer behavior. These checks do not execute model-selection conversations.

The tools require Python 3.9+ and use the standard library. The CI workflow runs the checks on its configured operating-system and Python combinations. Consult the result for the relevant commit in [GitHub Actions](https://github.com/yuezjo/model-fit/actions); a workflow file is not itself a passing result.

Reproduction commands and fixture guidance are in [Testing](docs/TESTING.md).

## Not yet verified

- Actual selection quality for real tasks and the user's available configurations.
- Cross-model continuation and preservation of task context.
- Recovery behavior in real client and tool interactions.
- Real-use token, allowance, or cost savings.

The behavior scenarios in `tests/scenarios.json` remain marked `not_run`. Individual user feedback is not a controlled behavioral pass. Offline success does not change these limits.
