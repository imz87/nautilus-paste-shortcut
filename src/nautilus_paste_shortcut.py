#!/usr/bin/env python3

import gi
import sys
import traceback

gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Nautilus", "4.0")

from gi.repository import Gdk, Gio, GLib, GObject, Gtk, Nautilus

from core_logic import (
    PasteShortcutError,
    local_path_from_uri,
    paste_shortcuts,
)


TARGET_MIME_TYPE = "x-special/gnome-copied-files"
MENU_LABEL = "Paste Shortcut Here"
DIALOG_TITLE = "Paste Shortcut Here"


class PasteShortcutExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, current_folder):
        # Nautilus calls menu providers repeatedly, so keep this path
        # defensive and cheap: log unexpected failures and hide the item.
        try:
            if not self._clipboard_has_copied_files():
                return []

            folder_uri = current_folder.get_uri()
            if not local_path_from_uri(folder_uri):
                return []

            item = Nautilus.MenuItem(
                name="PasteShortcutExtension::PasteShortcutHere",
                label=MENU_LABEL,
                tip="Create symbolic links from copied files",
            )
            item.connect("activate", self._on_activate, folder_uri)
            return [item]
        except Exception as error:
            self._report_exception("get_background_items", error)
            return []

    def _clipboard_has_copied_files(self):
        display = Gdk.Display.get_default()
        if display is None:
            return False

        clipboard = display.get_clipboard()
        formats = clipboard.get_formats()
        return formats.contain_mime_type(TARGET_MIME_TYPE)

    def _on_activate(self, _menu_item, destination_uri):
        # Keep activation defensive because clipboard behavior differs between
        # Nautilus/GDK versions and desktop sessions.
        try:
            display = Gdk.Display.get_default()
            if display is None:
                self._show_error("Could not access the current display.")
                return

            clipboard = display.get_clipboard()
            formats = clipboard.get_formats()
            if not formats.contain_mime_type(TARGET_MIME_TYPE):
                self._show_error("Clipboard does not contain copied files from GNOME Files.")
                return

            # Reading TARGET_MIME_TYPE directly can crash inside the native
            # GDK/Wayland clipboard transfer before Python receives an
            # exception. The text helper keeps failures in Python where they
            # can be reported safely.
            clipboard.read_text_async(None, self._on_clipboard_text_read, destination_uri)
        except Exception as error:
            self._report_exception("_on_activate", error)
            self._show_error("Failed to start the paste shortcut action.", str(error))

    def _on_clipboard_text_read(self, clipboard, result, destination_uri):
        try:
            payload = clipboard.read_text_finish(result)
        except GLib.Error as error:
            self._show_error("Failed to read the clipboard text.", str(error))
            return
        except Exception as error:
            self._report_exception("_on_clipboard_text_read", error)
            self._show_error("Unexpected error while reading clipboard text.", str(error))
            return

        if not payload:
            self._show_error("Clipboard is empty.")
            return

        payload = self._normalize_clipboard_text(payload)

        try:
            message = paste_shortcuts(payload, destination_uri)
        except PasteShortcutError as error:
            self._show_error(str(error))
            return
        except Exception as error:
            self._report_exception("paste_shortcuts_from_text", error)
            self._show_error("Unexpected error while creating shortcuts.", str(error))
            return

        if message:
            self._show_error(message)

    def _normalize_clipboard_text(self, payload):
        lines = [line.strip() for line in payload.splitlines() if line.strip()]
        if not lines:
            return payload

        # Older Nautilus clipboard data starts with an operation marker:
        # "copy" or "cut" followed by file:// URIs. Keep that shape intact.
        if lines[0] in {"copy", "cut"}:
            return "\n".join(lines)

        # On this Fedora/Nautilus/Wayland setup, read_text_async() returns
        # plain local paths instead of the old x-special/gnome-copied-files
        # text payload. Treat those paths as copied items and convert them to
        # the payload shape used by the pure shortcut logic.
        uris = []
        for line in lines:
            uri = (
                line
                if line.startswith("file://")
                else Gio.File.new_for_path(line).get_uri()
            )
            if local_path_from_uri(uri):
                uris.append(uri)

        if not uris:
            return payload

        return "\n".join(["copy", *uris])

    def _show_error(self, message, detail=None):
        if hasattr(Gtk, "AlertDialog"):
            if detail is None:
                dialog = Gtk.AlertDialog(message=message, modal=True)
            else:
                dialog = Gtk.AlertDialog(message=message, detail=detail, modal=True)
            dialog.show(None)
            return

        dialog = Gtk.MessageDialog(
            transient_for=None,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=message,
            secondary_text=detail,
        )
        dialog.set_title(DIALOG_TITLE)
        dialog.connect("response", lambda current_dialog, _response_id: current_dialog.destroy())
        dialog.present()

    def _report_exception(self, context, error):
        trace = traceback.format_exc().strip()
        sys.stderr.write(f"[{DIALOG_TITLE}] {context}: {error}\n{trace}\n")
        sys.stderr.flush()
