# Release checklist

## Public Preview publication preparation

For this v0.2.1-preview Goldilocks publication, preserve the supplied product files. Do not edit maintained policies or regenerate changed runtime instructions. The general product-maintenance checklist below is separate from this documentation-only publication.

- [x] Locate the full Goldilocks source and record its archive hash.
- [x] Run build consistency, package integrity, and all 33 offline tests on macOS/Python 3.9.6; no skips.
- [x] Prepare matching English and Chinese README pages and bilingual release notes.
- [x] Complete candidate content, privacy, and local-link checks; record actual results in the publication transcript.
- [x] Confirm target account/repository, public visibility, license, and public copyright attribution with the owner.
- [x] Add the approved license and finalize documentation before creating the release commit.
- [ ] Build both final ZIP attachments from that exact commit; re-extract and verify them.
- [ ] After explicit publication approval, upload expanded source, enable Issues, set About, and publish the tagged pre-release with both attachments.
- [ ] Verify remote pages, tag commit, pre-release flag, downloadable attachments, and actual Actions status.

Only completed local steps are checked here. Remote verification is reported after publication; unchecked items are not failures or implied passes.

## Package / local checks

- [ ] Edit maintained `sources/`, regenerate all four folders, and verify synchronization.
- [ ] Run package and offline regression tests; check an extracted final archive too.
- [ ] Verify previous-version upgrade preserves private calibration and keeps backups outside discovery paths.
- [ ] Verify no private calibration, credentials, task data, temporary staging files, or bytecode is packaged.
- [ ] Record actual environments and results in `VALIDATION.md`; keep behavior tests separate.

## Live behavior / publication

- [ ] Test skill discovery and explicit-only invocation in each claimed client.
- [ ] Test real picker calibration, actual model switching, and continuation after confirmation.
- [ ] Verify no pre-confirm execution, scope-bound approval, safe tool recovery without needless confirmation, and output-correction/stage stops with tool evidence.
- [ ] Verify unresolved side-effect outcomes are not blindly replayed and persistent blockers stop without looping.
- [ ] Exercise task domains beyond coding and design; test fixed/restricted choices.
- [ ] Run the behavior scenarios or document precisely which were run and failed.
- [ ] Measure savings before making quantified claims.
- [ ] Choose a license and review inspiration/attribution before public reuse.
- [ ] Publish only when authorized; avoid implying this local preview is already on GitHub or in a marketplace.

The presence of a CI workflow is not proof that GitHub Actions ran. The preview's local checks do not certify live behavior.
