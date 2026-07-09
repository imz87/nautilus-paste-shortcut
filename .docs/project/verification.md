# Verification

## Focused Checks

Use these checks for normal changes:

```bash
python3 -m py_compile src/nautilus_paste_shortcut.py
bash -n install.sh
python3 -m pytest tests/ -v
```

## CI Checks

GitHub Actions CI runs these checks automatically on push and pull request across five distributions:

- **Fedora** (`fedora:latest`)
- **Ubuntu** (`ubuntu:24.04`)
- **Debian** (`debian:bookworm`)
- **Arch Linux** (`archlinux:latest`)
- **openSUSE Tumbleweed** (`opensuse/tumbleweed:latest`)

Each matrix job runs:

1. `bash -n install.sh` -- shell syntax validation
2. `python3 -m py_compile src/nautilus_paste_shortcut.py` -- Python syntax check (only when the Nautilus typelib is available)
3. `python3 -m pytest tests/ -v` -- pure unit tests

CI success means the project passes automated static and unit checks in distro containers. It does **not** guarantee the Nautilus context menu appears on every desktop. Container CI cannot verify Wayland clipboard behavior or Nautilus menu integration.

## Manual Checks

1. Copy one file in GNOME Files and run `Paste Shortcut Here` in another folder.
2. Copy one folder in GNOME Files and run `Paste Shortcut Here` in another folder.
3. Copy multiple items and verify one symlink is created per item.
4. Repeat with an existing destination name and verify suffix handling.
5. Press `Ctrl+X` and verify the menu item is hidden.
6. Copy non-file clipboard text and verify the menu item is hidden.

## Notes

- Review is a separate manual phase after development.
- For clipboard or Nautilus API changes, prefer a real desktop test over assumptions.
- Container CI covers dependency installation, Python compilation, shell syntax, and pure logic tests. Desktop integration (context menu, clipboard, error dialogs) still requires manual verification.
