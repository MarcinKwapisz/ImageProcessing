from PIL import Image
from gi.repository import GLib, GdkPixbuf
import gi

gi.require_version("Gtk", "3.0")

class Images():
    def __init__(self):
        self.image = Image.open('/home/marcin/Projekty/PycharmProjects/SkeletonAppPO/123')

    def ImageLoader(self, path):
        self.image = Image.open(path)

    def image2pixbuf(self):
        data = self.image.tobytes()
        w, h = self.image.size
        data = GLib.Bytes.new(data)
        print(self.image.size,self.image.mode)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, True, 8, w, h, w*3)
        return pix

    def gamma(self):
        pass