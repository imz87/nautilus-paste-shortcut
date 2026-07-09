# Task

Only show `Paste Shortcut Here` when the clipboard currently contains copied local files from GNOME Files.

# Background

The initial implementation always shows the menu item and validates the clipboard when the action is clicked. That keeps the extension simple, but a more polished experience would hide the action when Nautilus's copied-files clipboard format is not present.

# Files Expected To Change

- `src/nautilus_paste_shortcut.py`
- `README.md`
- Optional: `.docs/project/verification.md`

# Implementation Steps

1. Check whether Nautilus allows safe clipboard inspection while building the background menu.
2. Hide the menu item when the clipboard does not contain supported copied local files.
3. Keep the current activation-time validation as a fallback.
4. Update docs if the visibility behavior changes.

# Acceptance Criteria

- [x] `Paste Shortcut Here` is hidden when the clipboard does not contain copied files from GNOME Files.
- [x] The action still works for one or more copied local files.
- [x] Invalid clipboard cases still fail safely.

# Out Of Scope

- Do not add a dedicated `Copy Shortcut` action.
- Do not change symlink naming behavior.

# Risks

- Clipboard inspection during menu creation may be version-sensitive across Nautilus and GTK releases.

# Questions

- None currently.

# Commit Message

Hide Paste Shortcut when clipboard is invalid

# Completion

- **Review verdict:** Approve
- **Summary:** `get_background_items()` now reads the clipboard payload and validates that it contains a `copy` operation with at least one local `file://` URI before showing the menu item. Cut operations and non-local URIs are hidden.
- **Verification:** `python3 -m py_compile src/nautilus_paste_shortcut.py`, `python3 -m pytest tests/ -v` (38 passed)
- **Residual risks:** Clipboard read during menu creation is synchronous; may be version-sensitive across GTK releases.
