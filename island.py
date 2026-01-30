import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class DynamicIsland(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.set_keep_above(True)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)

        self.container = Gtk.EventBox()
        self.container.set_name("island_main")
        self.add(self.container)

        self.label = Gtk.Label(label="☁️ Sky OS Ready")
        self.label.set_margin_top(10)
        self.label.set_margin_bottom(10)
        self.label.set_margin_start(20)
        self.label.set_margin_end(20)
        self.container.add(self.label)

        screen = Gdk.Screen.get_default()
        self.move(screen.get_width() // 2 - 100, 5)

        GLib.timeout_add(500, self.update_island_logic)
        self.show_all()

    def update_island_logic(self):
        if os.path.exists("/tmp/skyid_scanning"):
            self.label.set_text("🔍 Sky ID: Сканирование...")
            self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0.45, 0.85, 0.9))
        elif os.path.exists("/tmp/skyid_success"):
            self.label.set_text("✅ Доступ разрешен")
            self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.1, 0.8, 0.1, 0.9))
            GLib.timeout_add_seconds(3, self.reset_island)
        return True

    def reset_island(self):
        if os.path.exists("/tmp/skyid_success"): os.remove("/tmp/skyid_success")
        self.label.set_text("☁️ Sky OS")
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.8))
        return False

if __name__ == "__main__":
    win = DynamicIsland()
    Gtk.main()
