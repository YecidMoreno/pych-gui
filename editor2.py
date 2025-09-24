import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Vte, GLib, Gdk, GLib

import os
import pty
import subprocess
import threading

from utils.pych_json import *
from modules.path_editor import *

class PropertieEditor:
    def __init__(self,j):
        
        self.j = j

        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade/block_properties.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.window.show_all()





class App:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade/editorUI.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.connect("key-press-event", self.on_key_press)
        self.window.show_all()

        self.j = read_json("ScienceMode3.json")

        json_details(self.j)

        self.show_tree(self.builder)

        self.set_accelerator()

        provider = Gtk.CssProvider()
        provider.load_from_path("glade/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        drawing_area = self.builder.get_object("canvas")
        drawing_area.connect("draw", self.on_draw)

        self.show_tree_block()
    
    def show_tree_block(self):
        
        pe = PropertieEditor(self.j["deviceIO"]["fes0_r"])
        

        pass

    def on_draw(self,widget, cr):

        cr.set_source_rgb(0.95, 0.95, 0.95)
        cr.paint() 

        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        spacing = 20
        cr.set_source_rgb(0.8, 0.8, 0.8) 

        for x in range(0, width, spacing):
            for y in range(0, height, spacing):
                cr.arc(x, y, 1.0, 0, 2 * 3.1416)
                cr.fill()
        

    def set_accelerator(self):
        self.accel_group = Gtk.AccelGroup()
        self.window.add_accel_group(self.accel_group)

        show_path_editor = self.builder.get_object("show_path_editor")
        show_path_editor.add_accelerator("activate", self.accel_group,
            Gdk.keyval_from_name("P"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        pass

    def show_tree(self,builder):
        tree = builder.get_object("tree")
        
        treestore = Gtk.TreeStore(str)
        tree.set_model(treestore)

        parent_iter = treestore.append(None, ["Grupo A"])
        treestore.append(parent_iter, ["Subitem A1"])
        treestore.append(parent_iter, ["Subitem A2"])

        
        renderer1 = Gtk.CellRendererText()
        renderer1.set_property("editable", True)
        renderer1.connect("edited", lambda cell, path, text: treestore[path].__setitem__(0, text))
        column1 = Gtk.TreeViewColumn("Nombre", renderer1, text=0)
        column1.set_clickable(True) 
        tree.append_column(column1)


        def on_row_activated(treeview, path, column):
            treeview.set_cursor(path, column, True)

        tree.connect("row-activated", on_row_activated) 

        pass
    
    def on_key_press(self,widget, event):
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        shift = event.state & Gdk.ModifierType.SHIFT_MASK
        key = Gdk.keyval_name(event.keyval)
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
    
    def on_path_editor_delete_event(self, widget, event):
        widget.hide()
        return True 

    def on_show_path_editor_activate(self,obj):
        pe = PathEditor(self.j)


app = App()
Gtk.main()

