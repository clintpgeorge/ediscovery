'''
Created on Feb 26, 2013

@author: abhiramj  & cgeorge
'''
import os 
import wx 
import tempfile
import webbrowser
import time

from decimal import Decimal 
from gui.RandomSamplerGUI import RandomSamplerGUI
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from file_utils import find_files_in_folder, copy_files_with_dir_tree, convert_size, start_thread, copy_with_dialog, FileLoadDialog



class RandomSampler(RandomSamplerGUI):
    '''
    Random sampler GUI class
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        # Some value needs to initialized for this to run without exception
        self.confidence_val = DEFAULT_CONFIDENCE_LEVEL / Decimal('100')
        self.precision_val = DEFAULT_CONFIDENCE_INTERVAL
                
        # Calls the parent class's method 
        super(RandomSampler, self).__init__(parent) 
        
        # stack to store files and tags
        self.file_tag_dict = {}
        '''
        This is the tag format
        
        self.file_tag_dict(filename) = [('Reviewed','True'),('Responsive', 'False'),('A1','False'),('A2','True')]
        '''
        
        # initialize the default list of tags and the current tag
        self.DEFAULT_TAGS_NUMBER = 2
        self.REVIEWED_TAG_INDEX = 0
        self.RESPONSIVE_TAG_INDEX = 1
        self.current_file_selected = None
        self.default_tag = ('Default' , 'True')
        self.current_tag_list = self.make_default_tag_list()
        self._tag_list.InsertColumn(0,'Property')
        self._tag_list.InsertColumn(1,'Status')
        self._tag_list.InsertStringItem(self.REVIEWED_TAG_INDEX, 'Reviewed')
        self._tag_list.SetStringItem(self.REVIEWED_TAG_INDEX, 1, 'False')
        self._tag_list.InsertStringItem(self.RESPONSIVE_TAG_INDEX, 'Responsive')
        self._tag_list.SetStringItem(self.RESPONSIVE_TAG_INDEX, 1, 'False')
        
        # Separator for splitting tags
        self.TAG_NAME_SEPARATOR = " || "
        
        # Maximum depth of folders expanded for display
        self.MAX_FOLDER_DEPTH = 2
        
        self._st_num_samples.Hide()
        self.dir_path = tempfile.gettempdir() # a cross-platform way of getting the path to the temp directory
        self.output_dir_path = tempfile.gettempdir()
        self.from_copy_files_dir = self.dir_path 
        self.to_copy_files_dir = self.output_dir_path
        self._tc_data_dir.SetValue(self.dir_path)
        self._tc_output_dir.SetValue(self.output_dir_path)
        
        self.file_list = find_files_in_folder(self.dir_path)
        self._st_num_data_dir_files.SetLabel('%d files found' % len(self.file_list))
        
        # Defaults for random sample calcluation
        self.SEED = 2013

        self._set_confidence_level_and_interval()
        self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()
                                          )/ Decimal('100')
        self.get_precision_as_float()
        self.Bind(wx.EVT_COMMAND_FIND_REPLACE_ALL, self._on_load_tag_list)
        self._panel_samples.Show(False) # make the tree list control invisible
        
        # Icon defaults
        self.icon_size = (16,16)
        self.image_list = wx.ImageList(self.icon_size[0], self.icon_size[1])
        self._tc_results.SetImageList(self.image_list)
        self.folder_icon     = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, self.icon_size))
        self.folder_open_icon = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, self.icon_size))
        self.file_icon     = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.icon_size))  

        self.Center()
        self.Show(True)
   
    def _on_remove_tag(self, event):
        '''
        Action on click on remove tag
        removes a tag from list
        Arguments: Event of remove tag button pressed
        Returns: Nothing
        '''
        
        super(RandomSampler, self)._on_remove_tag(event)
        
        item_index = self._tag_list.GetFirstSelected()
        
        if item_index is not self.RESPONSIVE_TAG_INDEX or item_index is not  self.REVIEWED_TAG_INDEX:
            self.current_tag_list.pop(item_index)
            self._tag_list.DeleteItem(item_index)
        
        # Refresh tags
        #reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
        #self.GetEventHandler().ProcessEvent(reload_tag)

    def _on_appln_close( self, event ):
        '''
        Action on closing the window
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_appln_close(event) 
        self._on_close()
    
    def _on_mitem_about( self, event ):
        super(RandomSampler, self)._on_mitem_about(event) 
        
        about_text = """Random sampler: 
        This application randomly samples the files 
        from the given data folder and copies them to the output 
        folder. Sample size is determined by the given 
        confidence interval."""
        dlg = wx.MessageDialog(self, about_text, "About Random Sampler", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.
    
    def _on_mitem_help( self, event ):
        '''
        Action on pressing help button
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_mitem_help(event) 
    
    def _on_mitem_exit( self, event ):
        '''
        Action on closing the window
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_mitem_exit(event) 
        self._on_close()
    
    def _on_click_sel_data_dir( self, event ):
        """
        Select the data folder
        Arguments: Event of item selected
        Returns: Nothing
        """
        super(RandomSampler, self)._on_click_sel_data_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the input folder to sample",
                           self.dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_path = dlg.GetPath()
            message_dialog = FileLoadDialog(gui = self, title = "Files loading", cancellable = True )
            message_dialog.Show()
            start_thread(self.do_load, message_dialog)
        dlg.Destroy()
        self._tc_data_dir.SetValue(self.dir_path)
        self.SetStatusText("The selected input folder is %s" % self.dir_path)
        
        #progress_dialog = wx.ProgressDialog('Loading', 'Please wait...', parent = self, style = 
        #                                    wx.PD_SMOOTH | wx.PD_ELAPSED_TIME)
            
        # Runs load on a different thread
        
        #self.file_list = find_files_in_folder(self.dir_path)
        self._st_num_data_dir_files.SetLabel('%d files found' % len(self.file_list))
        
        
        self.sampled_files = random_sampler(self.file_list,
                                            self.confidence_val,
                                            self.precision_val, self.SEED)
        self.SetStatusText('%d files are sampled out of %d files.'
                               % (len(self.sampled_files), len(self.file_list)))
        self._st_num_samples.Show()
        self.sampled_files = random_sampler(self.file_list,
                                                self.confidence_val,
                                                self.precision_val, self.SEED)
        self._st_num_samples.Show()
        self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
        
    def _on_precision_changed(self, event):
        '''
        Triggers an event and updates the sample list on precision - aka 
        confidence interval change.
        Arguments: Event of new precision value
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_precision_changed(event)
        # Maybe intermittently null string, escaping 
        try:
            self.get_precision_as_float()
        except ValueError:
            return None 
        self.sampled_files = random_sampler(self.file_list, self.confidence_val,
                                            self.precision_val, self.SEED)
        self.SetStatusText('%d files are sampled out of %d files.'
                               % (len(self.sampled_files), len(self.file_list)))
        self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
        self._st_num_samples.Show()
    
    def get_precision_as_float(self):
        '''
        Converts precision to float
        Returns: Nothing
        Arguments: Nothing
        '''
        try:
            self.precision_val = float(self._tc_confidence_interval.GetValue()
                                       ) / 100.0 
        except ValueError:
            self.precision_val = float(int(self._tc_confidence_interval.GetValue())
                                       ) / 100.0 
            
        
    def _on_confidence_changed(self, event):
        '''
        Triggers an event and updates the sample list on confidence - aka 
        confidence level change
        Arguments: Event of new confidence
        Returns: Nothing
        '''
        
        
        super(RandomSampler, self)._on_confidence_changed(event)
        self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()
                                          )/ Decimal('100')
        self.sampled_files = random_sampler(self.file_list, self.confidence_val,
                                            self.precision_val, self.SEED)
        self.SetStatusText('%d files are sampled out of %d files.'
                               % (len(self.sampled_files), len(self.file_list)))
        self._st_num_samples.Show()
        self._st_num_samples.SetLabel('%d files found' % len(self.sampled_files))
        self.GetSizer().Layout()

        
        
    def _on_click_sel_output_dir( self, event ):
        """ 
        Selects the output folder 
        Arguments: Nothing
        Returns: Nothing
        """
        super(RandomSampler, self)._on_click_sel_output_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the output folder to save",
                           self.output_dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_path = dlg.GetPath()
        dlg.Destroy()
        
        self._tc_output_dir.SetValue(self.output_dir_path)
        self.SetStatusText("The selected output folder is %s" % self.output_dir_path)
        
        
    def _on_save_mark_file_status(self, e):
        '''
        Handles status update to upper control on saving marked file
        Arguments: New status message
        Returns: Nothing
        '''
        update_message = e.GetClientData()
        self.SetStatusText("Saved " + str(update_message) + " files at " 
                           + os.path.basename(self.output_dir_path))        
    def do_copy(self, total_size, dialog):
        '''
        Thread to handle copy
        Arguments: Total size of copy, Handle to dialog
        '''
        copy_with_dialog(self.dir_path, self.sampled_files,
                                     self.output_dir_path, total_size, dialog)

        
    def do_load(self, dialog):
        
        self.file_list = find_files_in_folder(self.dir_path)
        self.Refresh()
        dialog.Close()
    
    def _on_click_copy_files( self, event ):
        '''
        Handles event of copy files button pressed
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_click_copy_files(event)
        
        # Check if path exists
        if (not os.path.exists(self.dir_path) or
        not os.path.exists(self.output_dir_path)):
            dlg = wx.MessageDialog(self, "Please enter a valid \
            input/output directory", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            return 
        
        total_file_size = 0
        try:
            # Get total file size
            for x in map(os.path.getsize, self.sampled_files):
                total_file_size += long(x)
        except OSError:
            print "One or more files could not be read due to errors, check permissions", str(OSError)  
        print_total_file_size = convert_size(total_file_size)
        dlg = wx.MessageDialog(self,
                               "Do you really want to copy {} files to {}? This will take {} space".format(len(self.sampled_files),
                                self.output_dir_path, print_total_file_size),
                               "Confirm Copy", wx.YES|wx.NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        
        #Show status of copy
        if result == wx.ID_YES and total_file_size > 0:
            progress_dialog = wx.ProgressDialog('Copying', 'Please wait...', parent = self, style = wx.PD_CAN_ABORT
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME)
            
            # Runs copy on a different thread
            start_thread(self.do_copy, total_file_size, progress_dialog)
            #progress_dialog.ShowModal()
            self.SetStatusText('%d randomly sampled files (from %d files) are copied \
            to the output folder.' % (len(self.sampled_files), len(self.file_list)))
            
            # shows the tree list control ans sets defaults 
            self.from_copy_files_dir = self.dir_path
            self.to_copy_files_dir = self.output_dir_path
            self._tc_results.DeleteAllItems()
            root = self._tc_results.AddRoot(self.to_copy_files_dir)
            self._tc_results.SetPyData(root, os.path.abspath(self.to_copy_files_dir))
            self._tc_results.SetItemImage(root,self.folder_icon, wx.TreeItemIcon_Normal)
            self._tc_results.SetItemImage(root,self.folder_open_icon, wx.TreeItemIcon_Expanded)
            self.get_dirs(root,0)
            
            
            self._panel_samples.Show(True)
            self._panel_samples.GetSizer().Layout()
            self.GetSizer().Layout()
        
        else :
            self.SetStatusText('Copy cancelled.')
    
    def _on_activated_file(self, event):
        '''
        Marks a file as reviewed on double click
        Returns: None
        Arguments: File to set status
        '''
        super(RandomSampler, self)._on_activated_file(event)
        
        #Get filename
        if self.current_tag_list is not None:
            self.file_tag_dict[self.current_file_selected] = self.current_tag_list
        treeitem = event.GetItem()
        filename  = self.get_filename_from_treenode(treeitem)
        self.current_file_selected = filename
        
        
        #Get tag for filename
        tag = self.file_tag_dict.get(filename)
        if tag is None:
            self.current_tag_list = self.make_default_tag_list()
        self.set_tag_status(self.REVIEWED_TAG_INDEX, 'True')
        self.file_tag_dict[filename] = self.current_tag_list  
        
        #Open file        
        try:
            webbrowser.open(filename)
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Cannot open this file",
                                    wx.ICON_ERROR)
            dlg.ShowModal()
        # Fire an event to reload the tag listbox
        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
        self.GetEventHandler().ProcessEvent(reload_tag)
        
        self.update_tag_in_results_tree()
    
    def make_default_tag_list(self):
        '''
        Makes a default tag to add
        Arguments: Nothing
        Returns: Nothing
        '''
        
        tag_label = 'DEFAULT LABEL'
        new_tag = []
        for i in xrange(self.DEFAULT_TAGS_NUMBER): 
            new_tag.append((tag_label, 'False'))
        tag_0 = new_tag.pop(self.REVIEWED_TAG_INDEX)
        tag_0 = ('Reviewed', 'False')
        new_tag.insert(self.REVIEWED_TAG_INDEX, tag_0)
        tag_1 = new_tag.pop(self.RESPONSIVE_TAG_INDEX)
        tag_1 = ('Responsive', 'False')
        new_tag.insert(self.RESPONSIVE_TAG_INDEX, tag_1)
        
        return new_tag
    
    def set_tag_status(self, index, value):
        '''
        Sets tag indexed by index to value
        Arguments: 
        index: Index of tag to set
        value: value to set, for now only use True/False 
        '''
        tag_name, tag_value = self.current_tag_list.pop(index)
        tag_dirty = (tag_name, value)
        self.current_tag_list.insert(index, tag_dirty)
    
    def _on_select_file(self, event):
        '''
        Gets tag on file select and fires an event to show status of file
        Returns: None
        Arguments: File to display status for 
        '''
        
        super(RandomSampler, self)._on_select_file(event)
        treeitem = event.GetItem()
        self.get_dirs(treeitem,0)
        self._tc_results.Refresh()
        filename = self.get_filename_from_treenode(treeitem)
        # If no current tag, load a default tag
        if (self.current_file_selected is None or self.current_tag_list is None):
            self.current_tag_list  = self.make_default_tag_list()
            self.current_file_selected = filename
        
        # Else save the current tag and load from the tag dictionary for next file
        else:
            self.file_tag_dict[self.current_file_selected] = self.current_tag_list
            tag = self.file_tag_dict.get(filename)
            if tag is None:
                tag = self.make_default_tag_list()
            self.current_file_selected = filename
            self.current_tag_list = tag
        
        # Fire an event to reload the tag listbox
        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
        self.GetEventHandler().ProcessEvent(reload_tag)
             
    
    def _on_load_tag_list( self , evt):
        '''
        Reloads the tag list from 'dirty' tag in the tag dictionary
        Take note to save the last dirty tag before closing
        Returns: None
        Arguments: None
        '''
        # Format the current 'dirty' tag and add to control
        self._tag_list.ClearAll()
        self._tag_list.InsertColumn(0,'Tag')
        self._tag_list.InsertColumn(1,'Status')
        row_num = 0
        for  tag_name, tag_value in self.current_tag_list:
            self._tag_list.InsertStringItem(row_num, tag_name)
            if tag_value is None: 
                self._tag_list.SetStringItem(row_num, 1, 'False')
                self._tag_list.SetItemData(row_num, 0)
            else:
                self._tag_list.SetStringItem(row_num, 1, str(tag_value))
                if str(tag_value) is 'False':
                    self._tag_list.SetItemData(row_num, 0)
                if str(tag_value) is 'True':
                    self._tag_list.SetItemData(row_num, 1)
            row_num = row_num + 1
        #self._tag_list.RefreshItems()

    def _on_click_exit( self, event ):
        '''
        Exits
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_click_exit(event) 
        self._on_close()
 
    
    def _on_click_log_details( self, event ):
        '''
        Saves the marked history to a file in a specified folder
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_click_log_details(event) 
        # Save the tag_list and Get type of selected tag to be saved
        self.file_tag_dict[self.current_file_selected] = self.current_tag_list
        save_files = self.file_tag_dict.keys()
        tag_selected_type = self._cbx_tag_type.GetValue()
        if tag_selected_type == 'Reviewed':
            tag_selected_index = self.REVIEWED_TAG_INDEX
        elif tag_selected_type == 'Responsive':
            tag_selected_index = self.RESPONSIVE_TAG_INDEX
        else:
            tag_selected_index = -1
        
        save_filename = 'Log_history_' + time.strftime("%b%d%Y%H%M%S", time.localtime())
        fire_mark_saved  = wx.PyCommandEvent(wx.EVT_ACTIVATE.typeId)
        try:
            with open(os.path.join(self.to_copy_files_dir,save_filename), 'w') as file_handle:
                file_handle.write('Data Folder:' + self.from_copy_files_dir + '\n')
                file_handle.write('Sampled Output:' + self.to_copy_files_dir + '\n')
                file_handle.write('Confidence Level: +/-'+str(self.confidence_val) + '\n')
                file_handle.write('Confidence Interval: +/-'+str(self.precision_val) + '\n')
                for save_file in save_files:
                    
                    # Lookahead for the required tag status
                    is_write = True 
                    index = 0
                    if (tag_selected_index >= 0):
                        for item, status in self.file_tag_dict.get(save_file):
                            if (index == tag_selected_index and status == 'False'):
                                is_write = False
                                break
                            index = index +1     
                        
                    # Start writing the selected file tags
                    if is_write is True:
                        file_handle.write(save_file)
                        for item, status in self.file_tag_dict.get(save_file):
                            file_handle.write('\n' + '\t'+ item + '\t' + str(status))
                        file_handle.write('\n')
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
        # Fire an event warning of the exception
        except Exception as anyException:
            print str(anyException)
            fire_mark_saved.SetClientData(str(anyException))
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
            dlg = wx.MessageDialog(self, "Unable to write save history\
             of files.", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
   
   
    def _on_close(self):
        '''
        Closes the Application after confirming with user
        Arguments: Nothing
        Returns: Nothing
        '''
        
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.Destroy() 


    def _set_confidence_level_and_interval(self):
        '''
        Sets default confidence level and interval in Top Level interface
        Arguments: None
        Returns: None
        '''
        
        confidence_levels = ['%.3f' % (w * Decimal('100')) 
                             for w in  SUPPORTED_CONFIDENCES.keys()]
        confidence_levels.sort()
        self._cbx_confidence_levels.Clear()
        for cl in confidence_levels:
            self._cbx_confidence_levels.Append(cl)
            
        items = self._cbx_confidence_levels.GetItems()
        index = -1
        try:
            index = items.index(str(DEFAULT_CONFIDENCE_LEVEL))
            self._cbx_confidence_levels.SetSelection(index)
        except ValueError:
            self._cbx_confidence_levels.SetValue(str(DEFAULT_CONFIDENCE_LEVEL))
            
        self._tc_confidence_interval.SetValue(str(int(DEFAULT_CONFIDENCE_INTERVAL)))
        
            
    def _on_edit_status(self, event):
        '''
        Edits Label for Responsive
        Arguments: event identifying the row to edit
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_edit_status(event)
        # Do not let user edit if it is the Reviewed Tag
        row_num = event.GetIndex()
        if (row_num is self.REVIEWED_TAG_INDEX):
            event.Veto()
            return
        status =  self._tag_list.GetItemData(row_num)
        # This is a circuitous way as you can't directly read the tag_list tag status
        # So we save a 0/1 for the status. Supports only boolean 
        if status is 0: 
            self._tag_list.SetStringItem(row_num , 1, 'True')
            self.set_tag_status(row_num, 'True')
            self._tag_list.SetItemData(row_num , 1)
        if status is 1: 
            self._tag_list.SetStringItem(row_num , 1, 'False')
            self.set_tag_status(row_num, 'False')
            self._tag_list.SetItemData(row_num , 0)
        
        self.update_tag_in_results_tree()
        
            
    def _on_clear_tags(self, event):
        '''
        Removes tags for all files
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_clear_tags(event)
        self.file_tag_dict.clear()
        self.current_tag_list = self.make_default_tag_list()
        self.current_file_selected = self.to_copy_files_dir
        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
        self.GetEventHandler().ProcessEvent(reload_tag)
        
        self.to_copy_files_dir = self.output_dir_path
        self._tc_results.DeleteAllItems()
        root = self._tc_results.AddRoot(self.to_copy_files_dir)
        self._tc_results.SetPyData(root, os.path.abspath(self.to_copy_files_dir))
        self._tc_results.SetItemImage(root,self.folder_icon, wx.TreeItemIcon_Normal)
        self._tc_results.SetItemImage(root,self.folder_open_icon, wx.TreeItemIcon_Expanded)
        self.get_dirs(root,0)
        
    def _on_add_tag(self, event):
        '''
        Adds a new default tag to end of file list
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_add_tag(event)
        self.current_tag_list.append(self.default_tag)
        
        # Refresh tags
        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
        self.GetEventHandler().ProcessEvent(reload_tag)
        # Reload the tag in tree
        self.update_tag_in_results_tree()
        
    def _on_edit_property(self, event):
        '''
        Edits tag for file
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_edit_property(event)
        row_num = event.GetIndex()
        # Do not let default tag_names to be edited
        if row_num is self.REVIEWED_TAG_INDEX or row_num is self.RESPONSIVE_TAG_INDEX:
            event.Veto()
        
        self.update_tag_in_results_tree()
            
    def _on_set_property(self, event):
        '''
        Sets tag name  for file
        Arguments: Nothing
        Returns: Nothing
        '''
        super(RandomSampler, self)._on_set_property(event)
        # If no name set the name back to previous
        row_num = event.GetIndex()
        new_tag_property_name = event.GetLabel()
        if new_tag_property_name is '':
            return 
        # Pop the appropriate tag and then update it
        tag_name, tag_value = self.current_tag_list.pop(row_num)
        tag_dirty = (new_tag_property_name, tag_value)
        self.current_tag_list.insert(row_num, tag_dirty)
        
        self.update_tag_in_results_tree()
        
        
    def get_dirs(self, item, level):
        '''
        Fetches the contents of a directory 
        Arguments: 
        item: Item to be expanded
        level: Level of expansion from initial click
        Returns: Nothing
        '''
        if level == self.MAX_FOLDER_DEPTH:
            return  
        dirname = self._tc_results.GetPyData(item)
        dir_list = []
        if os.path.isdir(dirname) is  True:
            try:
                # Dont append to list if files added previously
                if self._tc_results.GetChildrenCount(item, False) == 0:
                    dir_list += os.listdir(dirname)
                    dir_list.sort()
                    for pathname in dir_list:
                        new_item = self._tc_results.AppendItem(item,pathname)
                        self._tc_results.SetPyData(new_item,os.path.join(dirname, pathname))
                        self.get_dirs(new_item, level +1)
                        if os.path.isdir(os.path.join(dirname,pathname)):
                            self._tc_results.SetItemImage(new_item,self.folder_icon, wx.TreeItemIcon_Normal)
                            self._tc_results.SetItemImage(new_item,self.folder_open_icon, wx.TreeItemIcon_Expanded)
                        else:
                            self._tc_results.SetItemImage(new_item,self.file_icon, wx.TreeItemIcon_Normal)
                    
            except OSError:
                None
            
    def get_filename_from_treenode(self, treeitem):
        '''
        Returns filename for given node
        Arguments: treeitem to get filename for
        Returns: filename
        '''
        
        return self._tc_results.GetPyData(treeitem)
    
    def get_positive_tag_string(self, filename):
        '''
        Gets the string containing the positive tags concatenated with a tag name separator
        Arguments: Nothing
        Returns: Nothing
        '''
        # First write current dirty tag to file_tag_dict to process it
        
        self.file_tag_dict[self.current_file_selected] = self.current_tag_list 
        
        # No tag present case
        tag_list = self.file_tag_dict.get(filename)
        if tag_list is None:
            return ""
        else:
            tag_string = ''
            for tag in tag_list:
                tag_name, tag_status = tag
                if tag_status is 'True':
                    tag_string = tag_string+self.TAG_NAME_SEPARATOR+tag_name
            
            # Remove the separator at the list
            if tag_string.endswith(self.TAG_NAME_SEPARATOR):
                tag_string = tag_string[0:(0-len(self.TAG_NAME_SEPARATOR))]
            return tag_string
    
    def update_tag_in_results_tree(self):
        '''
        Fires an update to load new tag in tree
        Arguments: Nothing
        Returns: Nothing
        '''
        # Get TreeItem and filename
        tree_item = self._tc_results.GetSelection()
        filename = self.get_filename_from_treenode(tree_item)
        
        # Get the displayname and positive tag and join them 
        display_name = self._tc_results.GetItemText(tree_item).split(self.TAG_NAME_SEPARATOR)[0]
        self._tc_results.SetItemText(tree_item,display_name + "  " + self.get_positive_tag_string(filename))
        

def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    RandomSampler(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()
    