import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Vte, GLib, Gdk, GLib


import os
import pty
import subprocess
import threading

class VirtualTerm(Vte.Terminal):
    
    def __init__(self, gtk_box=None):
        super().__init__()

        self.ready = False
        self.input_buffer = []
        self.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["/bin/bash"],
            [],
            0,
            None,
            None,
            -1,
            None,
            self.on_spawn_ready,
            None
        )

        if gtk_box:
            self.gtk_box = gtk_box
            self.gtk_box.show_all()
            self.gtk_box.pack_start(self, True, True, 0)
            self.gtk_box.reorder_child(self, 0)
            self.gtk_box.show_all()

        self.set_color_background(Gdk.RGBA(0.98, 0.98, 0.98, 1))  
        self.set_color_foreground(Gdk.RGBA(0.2, 0.2, 0.2, 1)) 
        

    def on_spawn_ready(self,*arg,**kargs):
        
        self.ready = True
        self.write("clear")
        self.write("cd /home/inception/git/pych ")
        self.write("clear")
        for line in self.input_buffer:
            self.write(line)

    def write(self,txt=""):
        if self.ready:
            cmd = txt.encode()+b'\n'
            self.feed_child(cmd)
        else:
            self.input_buffer.append(txt)        

class App:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("glade/mainUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("main_window")
        window.connect("destroy", Gtk.main_quit)
        window.connect("key-press-event", self.on_key_press)
        window.show_all()
        
        self.vterm = VirtualTerm(builder.get_object("box_terminal"))
        self.box_plugins = builder.get_object("box_plugins")

        button1 = Gtk.Button(label="Build {pych_plugins}")
        button1.connect("clicked",lambda obj: self.on_plugin_build_clicked(obj,"/home/inception/git/pych_plugins/build.sh host"))
        self.box_plugins.pack_start(button1,True,True,0)
        self.box_plugins.show_all()

        button1 = Gtk.Button(label="Build {pych_plugins} Remote")
        button1.connect("clicked",lambda obj: self.on_plugin_build_clicked(obj,"/home/inception/git/pych_plugins/build.sh $REMOTE_ARCH"))
        self.box_plugins.pack_start(button1,True,True,0)
        self.box_plugins.show_all()
        
        self.onActivate(None)

    def on_plugin_build_clicked(self,obj,path):
        self.vterm.write(path)
        pass

    def on_ed_cmd_activate(self,obj):
        self.vterm.write(obj.get_text())
        obj.set_text("")        

    def onBuild(self,obj):
        self.vterm.write("pych-xbuild")

    def onRun(self,obj):
        self.vterm.write("./models/run.sh")

    def onActivate(self,obj):
        # self.vterm.write("source activate.sh && export PS1=''")
        self.vterm.write("source activate.sh")
        
    def on_btn_remote_build_clicked(self,obj):
        self.vterm.write("./scripts/remote.sh build")

    def on_btn_remote_copy_clicked(self,obj):
        self.vterm.write("./scripts/remote.sh copy")
    
    def on_btn_remote_all_clicked(self,obj):
        self.vterm.write("./scripts/remote.sh all")

    def on_btn_remote_mount_clicked(self,obj):
        self.vterm.write("./scripts/remote.sh mount")
    
    def on_btn_remote_umount_clicked(self,obj):
        self.vterm.write("./scripts/remote.sh umount")

    def on_key_press(self,widget, event):
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        shift = event.state & Gdk.ModifierType.SHIFT_MASK
        key = Gdk.keyval_name(event.keyval)

        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        elif ctrl and shift and key == 'C':
            self.vterm.copy_clipboard()
            return True
        elif ctrl and shift and key == 'V':
            self.vterm.paste_clipboard()
            return True
        
        return False


app = App()

Gtk.main()








