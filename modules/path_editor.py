import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PathEditor:
    def __init__(self,j):
        
        self.j = j
        self.show()
        self.update()
        
    def getSelection(self):
        selection = self.tree.get_selection()
        model, treeiter = selection.get_selected()
        if not treeiter is None:
            path = model.get_path(treeiter)
            index = path.get_indices()[0]
        else:
            path = index = None
        return selection,model,treeiter,path,index

    def onSave(self,obj):
        model = self.tree.get_model()

        self.j["plugins"]["path"]   = [ p[0] for p in model]
        
        self.win.close()
        pass
        # 
        
    def onCancel(self,obj):
        self.win.close()
        
    def onAdd(self,obj):
        self.liststore.append(None, ["./plugins/"])
        pass
        
    def onRemove(self,obj):
        selection,model,treeiter,path,index = self.getSelection()
        if treeiter is None: return

        
        model.remove(treeiter)
        
    def onUp(self,obj):
        selection,model,treeiter,path,index = self.getSelection()
        if treeiter is None: return
        if index == 0: return 

        parent_iter = model.iter_parent(treeiter)
        new_iter = model.insert(parent_iter, index - 1)
        model[new_iter][0] = model[treeiter][0]
        model.remove(treeiter)
        self.tree.get_selection().select_iter(new_iter)
        pass
        
    def onDown(self,obj):
        selection,model,treeiter,path,index = self.getSelection()
        if treeiter is None: return
        parent_iter = model.iter_parent(treeiter)

        if index == (len(model)-1): return 

        new_iter = model.insert(parent_iter, index + 2)
        model[new_iter][0] = model[treeiter][0]
        model.remove(treeiter)
        self.tree.get_selection().select_iter(new_iter)
        
        
        
    def update(self):
        
        for p in self.j["plugins"]["path"]:
            self.liststore.append(None, [p])
        pass

    def show(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade/path_editor.glade")
        self.builder.connect_signals(self)
        self.win = self.builder.get_object("path_editor")
        self.win.show_all()

        self.tree = self.builder.get_object("tree")
        self.liststore = Gtk.TreeStore(str)
        self.tree.set_model(self.liststore)

        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect("edited", lambda cell, path, new_text: self.liststore[path].__setitem__(0, new_text))

        column = Gtk.TreeViewColumn("Path", renderer, text=0)
        self.tree.append_column(column)

        def on_row_activated(treeview, path, column):
            treeview.set_cursor(path, column, True)

        self.tree.connect("row-activated", on_row_activated)

        pass
