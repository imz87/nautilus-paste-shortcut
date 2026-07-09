# Task

Add Fedora-friendly packaging assets for local RPM or COPR distribution.

# Background

The project can already be installed locally with `install.sh`, but publishing for Fedora users will be easier with packaging metadata and documented install/uninstall behavior.

# Files Expected To Change

- `packaging/*`
- `README.md`
- `.docs/project/packaging.md`

# Implementation Steps

1. Add basic RPM packaging assets.
2. Document package dependencies and install paths.
3. Document how to restart Nautilus after package install or removal.

# Acceptance Criteria

- [x] The repository contains basic Fedora packaging assets.
- [x] README documents the packaged installation path and dependencies.
- [x] Packaging docs explain local RPM or COPR distribution intent.

# Out Of Scope

- Do not publish to Fedora or COPR from this task.
- Do not change runtime behavior.

# Risks

- Packaging paths may vary slightly by Fedora release.

# Questions

- None currently.

# Commit Message

Add Fedora packaging assets

# Completion

- **Review verdict:** Approve
- **Summary:** Added RPM spec file, documented build/install/uninstall workflow in README and packaging docs, used `git archive` for clean source archives, documented restart guidance for both install and removal.
- **Verification:** `python3 -m py_compile src/nautilus_paste_shortcut.py src/core_logic.py`, `bash -n install.sh`, `rpmspec -q --parse packaging/nautilus-paste-shortcut.spec`
- **Residual risks:** None. Packaging paths may vary slightly by Fedora release.
