#!/usr/bin/python
import os
import wx
'''
This control is used to list, mark and unmark files in a directory.
Right click adds to Middle list of selected items
Double click deletes a selected item in the selected list in middle
Mark returns marked files

Author: Abhiram J
Date: 10 Feb 13
'''
class file_list_control(wx.Frame):
    def __init__(self, parent, id, title, target_dir):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 350))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        panel2 = wx.Panel(self, -1)

        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1),
                                wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS\
                                | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_VARIABLE_ROW_HEIGHT\
                                | wx.SUNKEN_BORDER)
        if not os.path.isdir(target_dir):
            target_dir = os.path.curdir
        root = self.tree.AddRoot(target_dir)
        self.get_dirs(root)
        
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_marked, self.tree, id =1)
        self.display = wx.ListBox(panel2, -1, style=wx.LB_SINGLE )
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_unmarked, self.display, id = wx.ID_DELETE)
        self.activate = wx.Button(self,wx.ID_APPLY, "Mark")
        self.Bind(wx.EVT_BUTTON, self.on_return, self.activate,  id =1)
        
        vbox.Add(self.tree, 1, wx.EXPAND)
        vbox2.Add(self.display, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(panel2, 1, wx.EXPAND)
        hbox.Add(self.activate, 1)
        panel1.SetSizer(vbox)
        panel2.SetSizer(vbox2)
        self.SetSizer(hbox) 
        
        self.Centre()

    def on_sel_changed(self, event):
        item =  event.GetItem()
        self.get_dirs(item)
        
    def get_dirs(self, item):
        dirname = self.tree.GetItemText(item)
        dir_list = []
        if os.path.isdir(dirname) is  True:
            dir_list += os.listdir(dirname)
        for pathname in dir_list:
            new_item = self.tree.AppendItem(item,pathname)
            self.tree.SetPyData(new_item,os.path.abspath(pathname))
            
    def on_marked(self, evt):
        current_item = evt.GetItem()
        #root = self.tree.GetRootItem()
        #current_count = self.display.GetItemCount()
        self.display.Append(self.tree.GetPyData(current_item))
        #print current_count
        #self.display.InsertStringItem(current_count+1, self.tree.GetPyData(current_item))
    def on_unmarked(self,evt):
        self.display.Delete(self.display.GetSelection())
        
    def on_return(self, evt):
        return self.display.GetItems()
        
#class MyApp(wx.App):
#    def OnInit(self):
#        frame = file_list_control(None, -1, 'list', '')
#        frame.Show(True)
#        self.SetTopWindow(frame)
#        return True
#
#app = MyApp(0)
#app.MainLoop()