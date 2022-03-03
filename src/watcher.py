# watcher.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import gi
gi.require_version("Gtk", "4.0")

from gi.repository import GLib, Gio


DELETED_EVENTS = (Gio.FileMonitorEvent.MOVED_OUT, Gio.FileMonitorEvent.DELETED)
CHANGED_EVENTS = (Gio.FileMonitorEvent.CHANGED, Gio.FileMonitorEvent.RENAMED)


class Watcher:
    def __init__(self, main_widget, filename):
        self.main_widget = main_widget
        self.filename = filename

        gfile = Gio.File.new_for_path(filename)
        self.monitor = gfile.monitor_file(Gio.FileMonitorFlags.WATCH_MOVES, None)
        self.monitor.connect("changed", self.on_changed)

    def on_changed(self, file_monitor, _file, _other_file, event_type):
        file_monitor.cancel()
        GLib.idle_add(self.main_widget.declare_file_created, self.filename)
        page = self.main_widget.itemlists[self.filename].page
        if event_type in CHANGED_EVENTS:
            page.changed_bar.show_text(True)
            page.changed_bar.set_revealed(True)
        if event_type in DELETED_EVENTS:
            page.deleted_bar.show_text(True)
            page.deleted_bar.set_revealed(True)
