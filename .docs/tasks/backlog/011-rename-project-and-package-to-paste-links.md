# Task

Rename the project and package/artifact name from `nautilus-paste-shortcut` to `paste-links`, rename the menu wording from `Paste Shortcut` to `Paste Symlink`, and update external publishing targets on Launchpad, Fedora/COPR, and openSUSE/OBS while preserving current runtime behavior.

# Background

The current name is Nautilus-specific and no longer fits the intended direction toward multi-desktop support. The repository, package metadata, release artifact names, workflow publishing configuration, and user-facing installation commands currently use `nautilus-paste-shortcut` in many places.

The current menu wording also uses `Paste Shortcut`, but `shortcut` feels Windows-specific and does not describe the current Linux behavior precisely. The menu label should move to `Paste Symlink` as part of this naming cleanup.

This task is a naming and distribution migration. It should rename the project/package identity to `paste-links`, rename the current menu wording to `Paste Symlink`, and remove the old external package identities rather than preserving them as aliases. It must not change the current extension behavior or claim cross-desktop runtime support before that work exists.

# Files Expected To Change

- `README.md`
  - Update the project name, repository links, installation commands, package names, artifact examples, and menu wording.

- `src/nautilus_paste_shortcut.py` and related runtime-adjacent source files
  - Update the current menu label and related dialog title/user-facing text from `Paste Shortcut` to `Paste Symlink`.
  - Keep the runtime behavior unchanged.

- `.github/workflows/`
  - Update release, packaging, COPR, PPA, OBS, and any other workflow references that use the current repository/package name, artifact prefix, or external project/package identifiers.

- `packaging/nautilus-paste-shortcut.spec`
  - Rename the RPM spec file to match the new package name using `git mv old-path new-path`.
  - Update RPM package metadata and source tarball naming.

- `packaging/opensuse/nautilus-paste-shortcut.spec`
  - Rename the openSUSE spec file to match the new package name using `git mv old-path new-path`.
  - Update OBS-facing package metadata and source tarball naming.

- `packaging/debian/`
  - Update Debian package metadata, changelog package name, and any maintainer-script references that use the old package identity.

- `packaging/arch/PKGBUILD`
  - Update `pkgname`, source tarball names, install/uninstall examples, and any package-description text tied to the old name.

- `install.sh`
  - Update any project/package name text shown to users if it still uses the old identity.

- `.docs/project/packaging.md`
  - Update packaging and repository-publishing documentation to the new package/repository names and note any required manual external rename steps.

- `.docs/project/verification.md`
  - Update verification commands, expected artifact names, and menu wording.

- Other repository docs and metadata
  - Update any remaining user-facing references to the old project/package name or old menu wording where they describe the current system rather than historical task records.

# Architecture Notes

- Nautilus integration surface
  - Do not change the current Nautilus extension behavior, menu logic, clipboard handling, or symlink behavior.
  - This task changes naming and packaging identity, not desktop-runtime behavior.

- Clipboard or filesystem behavior
  - No clipboard parsing, symlink creation, destination validation, or error-dialog behavior should change.

- Packaging or install implications
  - All artifact names, package names, source tarball prefixes, install commands, and repository-publishing configuration should consistently use `paste-links`.
  - External publishing targets must be updated for:
    - Launchpad / PPA
    - Fedora COPR
    - openSUSE OBS
  - If an ecosystem requires a new project/package instead of an in-place rename, document the migration steps clearly.
  - Renamed tracked packaging files must use `git mv old-path new-path`.

- User-visible behavior boundaries
  - Users should see the new package/project name in documentation, package manager commands, and release artifacts.
  - Users should see `Paste Symlink` as the current menu/dialog wording instead of `Paste Shortcut`.
  - Do not imply KDE, Dolphin, or other multi-desktop runtime support yet; this task is naming groundwork only.

# Implementation Steps

1. Inventory all current `nautilus-paste-shortcut`, `Nautilus Paste Shortcut`, `Paste Shortcut`, and related publishing-identifier references in runtime-adjacent docs, packaging files, workflow files, and release/publishing configuration.
2. Rename the primary project/package identity to `paste-links` across repository metadata, packaging metadata, artifact names, and user-facing documentation.
3. Rename tracked spec files and any other tracked packaging files whose filenames must match the new package name using `git mv old-path new-path`.
4. Rename the current menu/dialog wording from `Paste Shortcut` to `Paste Symlink` in runtime source and user-facing documentation.
5. Update GitHub Actions workflows so release artifacts, source tarballs, package builds, repository links, and publishing targets all use `paste-links` consistently.
6. Update Debian, RPM, Arch, and openSUSE packaging metadata to build/install the renamed package without changing runtime contents.
7. Update Launchpad/PPA configuration references and documented commands to the renamed package target.
8. Update Fedora/COPR project references and documented commands to the renamed package target.
9. Update openSUSE/OBS project/package references and documented commands to the renamed package target.
10. Remove old external package/project identities instead of keeping migration aliases.
11. Update README and project docs so all current install, uninstall, verification, release, and menu-label references use `paste-links` and `Paste Symlink` consistently.
12. Verify that packaging, documentation, runtime strings, and workflow references are internally consistent after the rename.

# Acceptance Criteria

- [ ] The repository’s current package/artifact identity is `paste-links` in README, packaging metadata, and workflow configuration.
- [ ] The GitHub repository identity is updated to `paste-links` wherever this task is responsible for repository naming and links.
- [ ] RPM, DEB, Arch, and openSUSE packaging files use `paste-links` consistently for package names and artifact/source naming.
- [ ] Launchpad/PPA references are updated to the renamed package/project target or clearly document any required manual migration.
- [ ] Fedora/COPR references are updated to the renamed package/project target or clearly document any required manual migration.
- [ ] openSUSE/OBS references are updated to the renamed package/project target or clearly document any required manual migration.
- [ ] The current menu item and related dialog title use `Paste Symlink` instead of `Paste Shortcut`.
- [ ] Any tracked packaging files renamed as part of this work are moved with `git mv`.
- [ ] Documentation and verification commands use the new package name.
- [ ] Documentation and current user-facing runtime text use `Paste Symlink` consistently.
- [ ] Old external package/project identities are removed rather than kept as migration aliases.
- [ ] No runtime Nautilus behavior changes are introduced.
- [ ] No behavior changes except those explicitly requested in this task.

# Out Of Scope

- Implementing KDE, Dolphin, Nemo, Thunar, or other non-Nautilus integrations.
- Changing the existing Nautilus extension runtime behavior.
- Adding new link types or changing symlink/hardlink behavior.
- Rebranding historical completed task records under `.docs/tasks/done/`.
- Expanding package publishing to new ecosystems beyond the currently documented Launchpad, COPR, and OBS targets.

# Risks

- Some ecosystems may not support an in-place rename and may require creating a new external package/project before the old one is removed.
- Workflow logic may depend on current spec filenames, tarball prefixes, or repository identifiers in multiple places.
- Renaming the package without a clear migration path could break install/uninstall instructions or upgrade expectations for existing users.
- Repository links, badge URLs, signing references, and release filenames may drift if the rename is only partially applied.
- Menu wording may drift between runtime strings and documentation if both are not updated together.

# Questions

- Resolved: the GitHub repository itself should also be renamed to `paste-links`.
- Resolved: Python module and import paths should also be renamed as part of this naming migration where appropriate.
- Resolved: old external package names should be removed rather than kept as migration aliases.

# Commit Message

refactor(packaging): rename project identity to paste-links
