import sys
import os
import gi
import re
import image

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Gio, GObject

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imageObject = image.Images()

        self.pixbuf = self.imageObject.image2pixbuf()
        self.label = Gtk.Image.new_from_pixbuf(self.pixbuf)
        self.add(self.label)
        self.label.show()

    # def change_image(self, img):
    #     photo = img
    #     extension = re.split(r'\.', img)[-1]
    #     self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(photo)
    #     self.label.set_from_pixbuf(self.pixbuf)

    def change_image(self, img):
        self.imageObject.ImageLoader(img)
        self.pixbuf = self.imageObject.image2pixbuf()
        self.label.set_from_pixbuf(self.pixbuf)

    def save_image(self, route):
        self.pixbuf.savev(route, extension, ["quality"], ["100"])

    def scale(self, width, height):
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(photo, width, height, False)
        self.label.set_from_pixbuf(self.pixbuf)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.example.myapp",
            **kwargs
        )
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("choose", None)
        action.connect("activate", self.on_choose)
        self.add_action(action)

        action = Gio.SimpleAction.new("save", None)
        action.connect("activate", self.on_save)
        self.add_action(action)

        action = Gio.SimpleAction.new("scale", None)
        action.connect("activate", self.on_scale)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder()
        try:
            builder.add_from_file("menu.ui")
        except:
            print("file not found")
            sys.exit()
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("appmenu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title="Image processing")
            self.window.set_default_size(800, 800)

        self.window.present()

    def on_choose(self, action, param):
        choose_dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=None,
                                              action=Gtk.FileChooserAction.OPEN)
        self.add_filters(choose_dialog)
        choose_dialog.add_buttons("_Open", Gtk.ResponseType.OK)
        choose_dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
        choose_dialog.set_default_response(Gtk.ResponseType.OK)
        response = choose_dialog.run()
        if response == Gtk.ResponseType.OK:
            photo = choose_dialog.get_filename()
            self.window.change_image(photo)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        choose_dialog.destroy()

    def on_save(self, action, param):
        choose_dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=None,
                                              action=Gtk.FileChooserAction.SAVE)
        self.add_filters(choose_dialog)
        choose_dialog.add_buttons("_Save", Gtk.ResponseType.OK)
        choose_dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)
        choose_dialog.set_default_response(Gtk.ResponseType.OK)
        response = choose_dialog.run()
        if response == Gtk.ResponseType.OK:
            route = choose_dialog.get_filename()
            self.window.save_image(route)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        choose_dialog.destroy()

    def on_scale(self, action, param):
        scale_dialog = Gtk.MessageDialog(title="Choose size", message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.OK_CANCEL)
        dialogBox = scale_dialog.get_content_area()
        width = Gtk.Entry()
        width.set_visibility(True)
        width.set_size_request(250, 0)
        height = Gtk.Entry()
        height.set_visibility(True)
        height.set_size_request(250, 0)
        dialogBox.pack_end(width, False, False, 0)
        dialogBox.pack_end(height, False, False, 0)
        scale_dialog.show_all()
        response = scale_dialog.run()
        height = height.get_text()
        width = width.get_text()
        scale_dialog.destroy()

        if (response == Gtk.ResponseType.OK) and (re.search('^[0-9]*$',width)) and (re.search('^[0-9]*$',height)):
            self.window.scale(int(width), int(height))
        else:
            return None


    def add_filters(self, dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Photos")
        filter_py.add_pattern("*.png")
        filter_py.add_pattern("*.jpg")
        filter_py.add_pattern("*.jpeg")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
