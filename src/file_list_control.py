#!/usr/bin/python
import os
import wx
import webbrowser
import time
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
        control_layout_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tree_sizer = wx.BoxSizer(wx.VERTICAL)
        control_sizer = wx.BoxSizer(wx.VERTICAL)
        display_sizer = wx.BoxSizer(wx.VERTICAL)
        tree_panel = wx.Panel(self, -1)
        display_panel = wx.Panel(self, -1)
        
        # Adding controls
        self.tree_label_text = "Directory contents"
        self.tree_label = wx.StaticText(tree_panel, label=self.tree_label_text)
        self.display_label_text = "Selected files"
        self.display_label = wx.StaticText(display_panel, label=self.display_label_text)
        self.target_dir = os.curdir
        self.tree = wx.TreeCtrl(tree_panel, 1, wx.DefaultPosition, wx.Size(300,200),
                                wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT
                                | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HAS_VARIABLE_ROW_HEIGHT\
                                | wx.SUNKEN_BORDER)
        if not os.path.isdir(target_dir):
            target_dir = os.path.curdir 
        root = self.tree.AddRoot(target_dir)
        self.tree.SetPyData(root, os.path.abspath(target_dir))
        self.get_dirs(root)
        
        # Binding events
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_sel_changed, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_open_file, id=1)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_marked, self.tree, id =1)
        self.display = wx.ListBox(display_panel, -1, style=wx.LB_SINGLE )
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_unmarked, self.display, id = wx.ID_DELETE)
        self.save_button = wx.Button(self,wx.ID_APPLY, "Save List")
        self.select_button = wx.Button(self,wx.ID_ADD, "Select")
        self.remove_button = wx.Button(self,wx.ID_REMOVE, "Remove")
        self.Bind(wx.EVT_BUTTON, self.on_save_marked_history, self.save_button, id = wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.on_marked, self.select_button, id = wx.ID_ANY)
        self.Bind(wx.EVT_BUTTON, self.on_unmarked, self.remove_button, id = wx.ID_ANY)
        
        #Setting layout
        tree_sizer.Add(self.tree_label)
        tree_sizer.Add(self.tree, 1, wx.EXPAND)
        display_sizer.Add(self.display_label)
        display_sizer.Add(self.display, 1, wx.EXPAND)
        control_sizer.Add(self.select_button, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        control_sizer.Add(self.remove_button, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        control_sizer.Add(self.save_button, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        control_layout_sizer.Add(tree_panel, 1, wx.EXPAND)
        control_layout_sizer.Add(display_panel, 1, wx.EXPAND)
        control_layout_sizer.Add(control_sizer, 1)
        tree_panel.SetSizer(tree_sizer)
        display_panel.SetSizer(display_sizer)
        self.SetSizer(control_layout_sizer) 
        
        self.Centre()
         
    def on_changed_output_dir(self, target_dir):
        '''
        Action on changing the directory to view files - refresh
        the file directory 
        '''
        self.target_dir = target_dir
        self.tree.DeleteAllItems()
        self.display.Clear()
        root = self.tree.AddRoot(target_dir)
        self.tree.SetPyData(root, os.path.abspath(target_dir))
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
        
        dirname = self.tree.GetPyData(item)
        dir_list = []
        if os.path.isdir(dirname) is  True and self.tree.GetChildrenCount(item, False) == 0:
            dir_list += os.listdir(dirname)
        for pathname in dir_list:
            new_item = self.tree.AppendItem(item,pathname)
            self.tree.SetPyData(new_item,os.path.join(dirname, pathname))
            
    def on_marked(self, evt):
        '''
        Gets the file path marked in the file tree by a right click
        and adds it to display control which shows selected files 
        '''
        current_items = self.tree.GetSelections()
        for current_item in current_items:
            file_path = self.tree.GetPyData(current_item)
            if not file_path in self.display.GetItems():
                self.display.Append(self.tree.GetPyData(current_item))
            fire_mark  = wx.PyCommandEvent(wx.EVT_FILEPICKER_CHANGED.typeId)
        fire_mark.SetClientData(self.display.GetCount())
        self.GetEventHandler().ProcessEvent(fire_mark)

    def on_open_file (self, event):
        '''
        Open a file
        '''
        current_item  = event.GetItem()
        file_path = self.tree.GetPyData(current_item)
        try:
            webbrowser.open(file_path)
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Cannot open this file", wx.ICON_ERROR)
            dlg.ShowModal()             
        
    def on_unmarked(self,evt):
        '''
        Action on double click on display panel:
        Delete a file from the selected list(display)
        '''
        self.display.Delete(self.display.GetSelection())
        fire_unmark  = wx.PyCommandEvent(wx.EVT_FILEPICKER_CHANGED.typeId)
        fire_unmark.SetClientData(self.display.GetCount())
        self.GetEventHandler().ProcessEvent(fire_unmark)
        

    def on_save_marked_history(self, evt):
        '''
        Saves the marked history to a file in a specified folder
        '''
        save_files = self.display.GetStrings()
        save_filename = 'save history ' + time.strftime("%b %d %Y %H %M %S",time.localtime())
        fire_mark_saved  = wx.PyCommandEvent(wx.EVT_ACTIVATE.typeId)
        try:
            with open(os.path.join(self.target_dir,save_filename), 'w') as file_handle:
                for save_file in save_files:
                    file_handle.write(save_file + '\n')
            fire_mark_saved.SetClientData(self.display.GetCount())
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
        except Exception as anyException:
            print str(anyException)
            fire_mark_saved.SetClientData(str(anyException))
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
            dlg = wx.MessageDialog(self, "Unable to write save history of files.", "Error", wx.ICON_ERROR)
            dlg.ShowModal()