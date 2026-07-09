# Packaging Notes

## Current Distribution

- Local install through `install.sh`
- Source distribution through GitHub
- Fedora RPM packaging assets in `packaging/`

## RPM Packaging

The repository contains a `.spec` file for building RPM packages:

```text
packaging/nautilus-paste-shortcut.spec
```

### Build a Local RPM

1. Install build dependencies:
   ```bash
   sudo dnf install rpm-build rpmdevtools
   ```

2. Set up the RPM build tree:
   ```bash
   rpmdev-setuptree
   ```

3. Create a source tarball:
   ```bash
   git archive --format=tar.gz --prefix=nautilus-paste-shortcut-0.1.0/ \
       HEAD -o ~/rpmbuild/SOURCES/nautilus-paste-shortcut-0.1.0.tar.gz
   ```

4. Build the RPM:
   ```bash
   rpmbuild -ba packaging/nautilus-paste-shortcut.spec
   ```

5. Install the built RPM:
   ```bash
   sudo dnf install ~/rpmbuild/RPMS/noarch/nautilus-paste-shortcut-0.1.0-1.*.rpm
   ```

6. Restart Nautilus:
   ```bash
   nautilus -q
   ```

### Uninstall

Remove the installed package and restart Nautilus so the extension is no longer loaded:

```bash
sudo dnf remove nautilus-paste-shortcut
nautilus -q
```

### Install Paths

- Extension file: `/usr/share/nautilus-python/extensions/nautilus_paste_shortcut.py`
- License: `/usr/share/licenses/nautilus-paste-shortcut/LICENSE`
- Documentation: `/usr/share/doc/nautilus-paste-shortcut/README.md`

### Package Dependencies

- `python3-nautilus` - Nautilus Python bindings
- `nautilus-python` - Nautilus Python extension loader (provides `libnautilus-python.so`)
- `python3-gobject` - Python GObject introspection bindings
- `gtk4` - GTK4 toolkit

**Important:** `nautilus-python` is the extension loader, not just Python bindings. Without it, Nautilus silently ignores `.py` files in the extensions directory. The `install.sh` script checks for this before copying files.

### COPR Distribution

COPR packages can be built from the same spec file. To publish to COPR:

1. Create a COPR account at `copr.fedorainfracloud.org`
2. Add a new project
3. Upload the spec file and source tarball
4. Enable builds for desired Fedora releases

## Cross-Distro Support

The local installer (`install.sh`) works on any Linux distribution with a compatible Nautilus 4 desktop. The installer checks for the Nautilus Python extension loader before copying files.

Package names vary by distribution. The `nautilus-python` package (or equivalent) must provide `libnautilus-python.so`. See `README.md` for distro-specific install commands.

## Release Artifact Packaging

GitHub Actions can build package artifacts and attach them to GitHub Releases. This provides downloadable installable packages for multiple distributions.

### Version File

The repository uses a `VERSION` file as the single source of truth for package versions. The release workflow reads this file and validates it against Git tags when triggered by version tags.

```bash
cat VERSION
# Output: 0.1.0
```

### Build Artifacts

The release workflow builds these package formats:

| Distribution | Format | Build Container |
|---|---|---|
| Fedora/RHEL | `.rpm` | `fedora:latest` |
| Ubuntu/Debian | `.deb` | `ubuntu:24.04` |
| Arch Linux | `.pkg.tar.zst` | `archlinux:latest` |
| openSUSE | `.rpm` | `opensuse/tumbleweed:latest` |

### Packaging Files

- **Fedora**: `packaging/nautilus-paste-shortcut.spec`
- **Ubuntu/Debian**: `packaging/debian/`
- **Arch Linux**: `packaging/arch/PKGBUILD`
- **openSUSE**: `packaging/opensuse/nautilus-paste-shortcut.spec`

### Installation from Release Artifacts

Fedora/RHEL:
```bash
sudo dnf install ./nautilus-paste-shortcut-*.rpm
nautilus -q
```

Ubuntu/Debian:
```bash
sudo apt install ./nautilus-paste-shortcut_*.deb
nautilus -q
```

Arch Linux:
```bash
sudo pacman -U nautilus-paste-shortcut-*.pkg.tar.zst
nautilus -q
```

openSUSE:
```bash
sudo zypper install ./nautilus-paste-shortcut-*.rpm
nautilus -q
```

### Important Distinctions

**GitHub Release artifacts are NOT the same as native package repositories.** They do not provide automatic updates. Users must download and install new versions manually from GitHub Releases.

**Package signing is deferred to a separate task.** Current release artifacts are unsigned.

### Future Repository Publishing

Native package repository publishing is separate work:

- **Fedora/RHEL family**: COPR repository (planned)
- **Debian/Ubuntu family**: PPA or apt repository (planned)
- **Arch family**: AUR package recipe (planned)
- **openSUSE family**: OBS publishing (planned)

Repository publishing requires package signing, credentials, and different automation than release artifact builds.

## Non-Goals

- This project is not a GNOME Shell extension.
- It should not be submitted to `extensions.gnome.org`.
