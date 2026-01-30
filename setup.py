import gi
import cv2
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

class SkyIDSetup(Gtk.Window):
    def __init__(self):
        super().__init__(title="Sky ID Configuration")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(400, 500)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.image_area = Gtk.Image()
        vbox.pack_start(self.image_area, True, True, 0)

        self.btn = Gtk.Button(label="СДЕЛАТЬ СНИМОК")
        self.btn.connect("clicked", self.capture)
        vbox.pack_start(self.btn, False, False, 10)

        self.cap = cv2.VideoCapture(0)
        GLib.timeout_add(30, self.update_frame)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            h, w, d = frame_rgb.shape
            pb = GdkPixbuf.Pixbuf.new_from_data(frame_rgb.tobytes(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)
            self.image_area.set_from_pixbuf(pb)
        return True

    def capture(self, btn):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("/usr/local/bin/skyid/owner.jpg", frame)
            Gtk.main_quit()

if __name__ == "__main__":
    win = SkyIDSetup()
    win.show_all()
    Gtk.main()
