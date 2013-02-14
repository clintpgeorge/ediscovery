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
        
        
        if not os.path.isdir(target_dir):
            target_dir = os.path.curdir
        
        # Adding sizers
        sizer_main = wx.GridBagSizer(5, 5)
        panel_left = wx.BoxSizer(wx.VERTICAL)
        panel_center = wx.BoxSizer(wx.VERTICAL)
        panel_right = wx.BoxSizer(wx.VERTICAL)
        
        # Adding controls
        # Tree is a directory of files - input from target directory
        # Display shows selected items. Items are selected by right 
        # clicking in the tree. Items are deleted by double clicking on display
        # Mark/Activate returns the files as a list
        self.tree = wx.TreeCtrl(self, 1, wx.DefaultPosition, (-1,-1),
                                wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS\
                                | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_VARIABLE_ROW_HEIGHT\
                                | wx.SUNKEN_BORDER)
        self.display = wx.ListBox(self, -1, style=wx.LB_SINGLE )
        self.activate = wx.Button(self, wx.ID_APPLY, "Mark")
        self.help_label_files = wx.StaticText(self, label = 'Files to add')
        self.help_label_selected_files = wx.StaticText(self, label = 'Selected files')
        
        root = self.tree.AddRoot(target_dir)
        self.get_dirs(root)
        
        # Adding event handlers 
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK,
                       self.on_marked, self.tree, id =1)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED,
                       self.on_open_file, self.tree, id = wx.ID_OPEN)
        self.Bind(wx.EVT_LISTBOX_DCLICK,
                  self.on_unmarked, self.display, id = wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.on_return, self.activate,  id =1)
        
        # Setting layout
        panel_left.Add(self.tree, flag = wx.EXPAND)
        panel_center.Add(self.display, flag = wx.EXPAND)
        panel_right.Add(self.activate, flag = wx.EXPAND)
        sizer_main.Add(self.help_label_files,pos = (0,0), span = (1,1),
                       flag = wx.ALL , border = 2)
        sizer_main.Add(self.help_label_selected_files,pos = (0,1), span = (1,1),
                       flag = wx.ALL, border =  2)
        sizer_main.Add(panel_left,pos = (1,0), span = (1,1),
                       flag = wx.ALL | wx.EXPAND, border = 2)
        sizer_main.Add(panel_center,pos = (1,1), span = (1,1),
                       flag = wx.ALL | wx.EXPAND, border = 2)
        sizer_main.Add(panel_right,pos = (1,2), span = (1,1),
                       flag = wx.ALL | wx.EXPAND, border = 2)
        self.SetSizeHints(200,100,400,200)
        sizer_main.Fit(self)
        self.Layout()
        self.Refresh()
         
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
        