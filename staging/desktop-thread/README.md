# Desktop thread: unfinished work saved on 2026-10-04 20:27Z

Saved because greg is near his weekly limit. Thread "Build the Claude Desktop ssh plugin".
Everything finished is on GitHub on each repository's branch `claude/project-thread-fx3wkp`.
These files hold only what GitHub does not have yet. Snapshots, not instructions.

| File | What it is | How to use it |
|---|---|---|
| beethoven-extension-mac-release.bundle | Branches `wip/mac-W` (Windows MSI built and signed on the Mac: msitools wixl, Rust x86_64-pc-windows-gnu with mingw-w64, jsign against Azure Artifact Signing) and `wip/mac-R` (one release command on the Mac plus its setup script). Under review when saved. | `git fetch <bundle> 'refs/heads/*:refs/remotes/bundle/*'` in a beethoven-extension clone that has the branch head d6db850, then merge both into `claude/project-thread-fx3wkp`. |
| hpcworker-queue-fix.wip.patch | Half-done fixes for the 20 review findings of `hpcworker queue report` (wait = Start minus Eligible, sacct under TZ=UTC0 and SLURM_TIME_FORMAT=standard, -D, JobName dropped). Taken mid-edit. | `git apply` on top of b35952a; run `framework/tests/run.sh`; finish the findings in hpcworker-queue-review-findings.txt. |
| hpcworker-pr3-body.draft.md | Draft body for hpcworker PR #3 (queue report). | Update the Verified and How paragraphs after the fixes. |
| beethoven-vscode-account-fix.wip.patch | Half-done fixes for the 22 review findings of the VS Code `beethoven.account` setting. Taken mid-edit. | `git apply` on top of aa44696; finish the findings in beethoven-vscode-account-review-findings.txt. |
| beethoven-base-survey.json | The base survey so far: what each edition holds (inventories) and what two or more editions implement and where they drifted (overlap). The design was re-running with greg's 20:14Z secrets go-ahead when saved. | Input for designing beethoven-base; nothing is written in that repository yet. |
| hpcworker-v12-contract-signed-installers.patch | hpcworker's docs/V12_CONTRACT.md made byte-identical with the extension's 15.0.0 copy (section "Signed installers (15.0.0)"). Must be in hpcworker before 15.0.0 merges. | `git am` onto the hpcworker branch; it rides PR #3. |
| beethoven-base-design-and-critiques.json | The first base design and the two critiques of it (measured findings with file:line). Folded into /mnt/project-files/base/DESIGN.md. | Source for the design document. |
