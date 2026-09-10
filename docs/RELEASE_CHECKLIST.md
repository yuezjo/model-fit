# Release checklist

1. Confirm the intended version, four entry names, and scope of the release. Keep English and Chinese user manuals consistent.
2. Run the build-consistency check, package check, and offline unit suite described in [Testing](TESTING.md). Record actual outcomes; do not treat written scenarios as executed behavior tests.
3. Review the files and commits to be published. Exclude credentials, private calibration, personal conversations, local paths, backups, and unrelated material. Preserve the license and required third-party notices.
4. Commit the exact release files. Create a new version tag at that commit; do not overwrite an existing tag or force-push history.
5. Package only committed files. Name the full archive `model-fit-v<VERSION>.zip` and the lightweight archive `model-fit-v<VERSION>-skills.zip`. The lightweight archive contains the four complete skill folders and `LICENSE` at its root.
6. Prepare English release notes linking both user manuals. Upload both archives to a draft, mark the release as a pre-release, then publish it.
7. Check the remote tag, source files, manuals, release state, and downloadable archive contents. Report the actual CI status and unresolved limitations.
8. Remove superseded releases or assets only when authorized, and only after the replacement is available. Preserve Git history and existing tags.
