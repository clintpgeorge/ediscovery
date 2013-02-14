#!/usr/bin/python
import os
import wx
import webbrowser
'''
This control is used to list, mark and unmark files in a directory.
Right click adds to Middle list of selected items
Double click deletes a selected item in the selected list in middle
Mark returns marked files

Author: Abhiram J
Date: 10 Feb 13
'''
class file_list_control(wx.Panel):
    def __init__(self, parent, id, target_dir):
        wx.Panel.__init__(self, parent, id)
        
         
        
        # Instantiating all the sizers
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        panel2 = wx.Panel(self, -1)
        
        # Adding controls
        self.tree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1),
                                wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS\
                                | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_VARIABLE_ROW_HEIGHT\
                                | wx.SUNKEN_BORDER)
        if not os.path.isdir(target_dir):
            target_dir = os.path.curdir
        root = self.tree.AddRoot(target_dir)
        self.get_dirs(root)
        
        # Binding events
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_open_file, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_marked, self.tree, id =1)
        self.display = wx.ListBox(panel2, -1, style=wx.LB_SINGLE )
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_unmarked, self.display, id = wx.ID_DELETE)
        self.activate = wx.Button(self,wx.ID_APPLY, "Mark")
        self.Bind(wx.EVT_BUTTON, self.on_return, self.activate,  id =1)
        
        #Setting layout
        vbox.Add(self.tree, 1, wx.EXPAND)
        vbox2.Add(self.display, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(panel2, 1, wx.EXPAND)
        hbox.Add(self.activate, 1)
        panel1.SetSizer(vbox)
        panel2.SetSizer(vbox2)
        self.SetSizer(hbox) 
        
        self.Centre()
         
    def on_changed_output_dir(self, target_dir):
        '''
        Action on changing the directory to view files - refresh
        the file directory 
        '''
        self.tree.DeleteAllItems()
        self.display.Clear()
        root = self.tree.AddRoot(target_dir)
        self.get_dirs(root)
    
    def on_sel_changed(self, event):
        '''
        Action on opening a directory in the file tree
        '''
        item =  event.GetItem()
        self.get_dirs(item)
        
    def get_dirs(self, item):
        '''
        Fetches the contents of a directory 
        '''
        dirname = self.tree.GetItemText(item)
        dir_list = []
        if os.path.isdir(dirname) is  True:
            dir_list += os.listdir(dirname)
        for pathname in dir_list:
            new_item = self.tree.AppendItem(item,pathname)
            self.tree.SetPyData(new_item,os.path.abspath(pathname))
            
    def on_marked(self, evt):
        '''
        Gets the file path marked in the file tree by a right click
        and adds it to display control which shows selected files 
        '''
        current_item = evt.GetItem()
        file_path = self.tree.GetPyData(current_item)
        if not file_path in self.display.GetItems():
            self.display.Append(self.tree.GetPyData(current_item))

    def on_open_file (self, event):
        '''
        Open a file
        '''
        current_item  = event.GetItem()
        file_path = self.tree.GetPyData(current_item)
        try:
            webbrowser.open(file_path)
        except Exception:
            dlg = wx.MessageDialog(self, str(Exception), "Cannot open this file", wx.ICON_ERROR)
            dlg.ShowModal()             
        
    def on_unmarked(self,evt):
        '''
        Action on double click on display panel:
        Delete a file from the selected list(display)
        '''
        self.display.Delete(self.display.GetSelection())
        
    def on_return(self, evt):
        '''
        Action on pressing Mark/Activate control
        Returns a list of selcted items to process
        '''
        return self.display.GetItems()
        