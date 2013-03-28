'''
Created on Feb 26, 2013

@author: abhiramj  & cgeorge
'''
import os
import wx 
# import tempfile
import webbrowser
# import time
import shelve

from datetime import datetime 
from decimal import Decimal 
from gui.RandomSamplerGUI import RandomSamplerGUI, TagDocumentDialog
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from file_utils import find_files_in_folder, convert_size, start_thread, copy_with_dialog, get_destination_file_path, free_space

SHELVE_FILE_NAME = 'random_sampler.shelve'

class RSConfig: 
    def __init__(self, data_folder, output_folder, confidence_interval, confidence_level):
        self._data_folder = data_folder
        self._output_folder = output_folder
        self._confidence_interval = confidence_interval
        self._confidence_level = confidence_level
        self._current_page = 0
        self._created_date = datetime.now() 
        self._modified_date = datetime.now() 
        

class RandomSampler(RandomSamplerGUI):
    '''
    Random sampler GUI class
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        # Defaults for random sample calculation
        self.SEED = 2013      
        
#        # Some value needs to initialized for this to run without exception
#        self.confidence_val = DEFAULT_CONFIDENCE_LEVEL / Decimal('100')
#        self.precision_val = DEFAULT_CONFIDENCE_INTERVAL
                
        # Calls the parent class's method 
        super(RandomSampler, self).__init__(parent) 
        
        # Setting the icon
        app_icon = wx.Icon(os.path.join('res','uflaw-edisc1-icon.ico'), wx.BITMAP_TYPE_ICO, 32, 32)
        self.SetIcon(app_icon)
        
#        # stack to store files and tags
#        self.file_tag_dict = {}
#        '''
#        This is the tag format
#        
#        self.file_tag_dict(filename) = [('Reviewed','True'),('Accept', 'False'),('A1','False'),('A2','True')]
#        '''
#        
#        # initialize the default list of tags and the current tag
#        self.DEFAULT_TAGS_NUMBER = 2
#        self.REVIEWED_TAG_INDEX = 0
#        self.ACCEPT_TAG_INDEX = 1
#        self.current_file_selected = None
#        self.default_tag = ('Default' , 'True')
#        self.current_tag_list = self.make_default_tag_list()
#        self._tag_list.ClearAll()
#        self._tag_list.InsertColumn(0,'Tag')
#        self._tag_list.InsertColumn(1,'Status')
#        self._tag_list.InsertStringItem(self.REVIEWED_TAG_INDEX, 'Reviewed')
#        self._tag_list.SetStringItem(self.REVIEWED_TAG_INDEX, 1, 'False')
#        self._tag_list.InsertStringItem(self.ACCEPT_TAG_INDEX, 'Accept')
#        self._tag_list.SetStringItem(self.ACCEPT_TAG_INDEX, 1, 'False')
#        
#        # Separator for splitting tags
#        self.TAG_NAME_SEPARATOR = " , "
#        self.TAG_PREFIX = 'tag :'
#        
#        # Maximum depth of folders expanded for display
#        self.MAX_FOLDER_DEPTH = 2
        

        

#        self.from_copy_files_dir = self.dir_path 
#        self.to_copy_files_dir = self.output_dir_path

#        self.Bind(wx.EVT_COMMAND_FIND_REPLACE_ALL, self._on_load_tag_list)
#        self._panel_samples.Show(False) # make the tree list control invisible
        
#        # Icon defaults
#        self.icon_size = (16,16)
#        self.image_list = wx.ImageList(self.icon_size[0], self.icon_size[1])
#        self._tc_results.SetImageList(self.image_list)
#        self.folder_icon     = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, self.icon_size))
#        self.folder_open_icon = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, self.icon_size))
#        self.file_icon     = self.image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, self.icon_size))  

        self._is_io_updated = False # for the i/o tab updates  
        self._is_ct_updated = False # for the confidence tab updates      
        self._is_rt_updated = False # for the review tab updates      
        self._lc_review_loaded = False # for the review tab table 
        self._is_samples_created = False # for the samples tab  
        self._current_page = 0
        self.nb_config_sampler.ChangeSelection(self._current_page)

        # Loads confidence levels 
        self._load_cbx_confidence_levels()
        
        # Sets up the application state
        self._shelf_application_setup()
        
        self.Center()
        self.Show(True)
    

        
        
    
#    def _on_remove_tag(self, event):
#        '''
#        Action on click on remove tag
#        removes a tag from list
#        Arguments: Event of remove tag button pressed
#        Returns: Nothing
#        '''
#        
#        super(RandomSampler, self)._on_remove_tag(event)
#        
#        item_index = self._tag_list.GetFirstSelected()
#        
#        if (item_index <> self.ACCEPT_TAG_INDEX and item_index <>  self.REVIEWED_TAG_INDEX):
#            self.current_tag_list.pop(item_index)
#            self._tag_list.DeleteItem(item_index)
#        
#        # Refresh tags
#        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
#        self.GetEventHandler().ProcessEvent(reload_tag)
#        
#        self.update_tag_in_results_tree()

    def _on_appln_close( self, event ):
        '''
        Action on closing the window
        Arguments: Nothing
        Returns: Nothing
        '''
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
        self._on_close()
    
    def _on_nb_page_changed( self, event ):
        '''
        Handles the notebook page change event. 
        Currently it allows the user to go back 
        to prior pages 
        
        
        '''
        
        selected_page = event.Selection
        if selected_page < self._current_page:
            self._current_page = selected_page
        
        self.nb_config_sampler.ChangeSelection(self._current_page)


    
    def _on_click_io_next( self, event ):

        # validations 
        if self.dir_path == '' or self.output_dir_path == '':
            self._show_error_message("Value Error!", "Please chose Source Document Folder and Sampled Output Folder.")
            self._tc_data_dir.SetFocus()
            return
        elif self._tc_data_dir.GetValue().strip() == self._tc_output_dir.GetValue().strip():
            self._show_error_message("Value Error!", "Sampled Output Folder cannot be the same as Source Document Folder. Please chose a different folder.")
            self._tc_output_dir.SetFocus()
            return 
        elif len(self.file_list) == 0:
            self._show_error_message("Value Error!", "The Source document Folder does not have any files to sample.")
            self._tc_data_dir.SetFocus()
            return 
        
        if self._is_io_updated:
            self._shelf_update_io_tab_state()
            self._is_io_updated = False # updates the global         
        
        if self._is_io_updated or not self._shelf_has_samples:    
            # Generates samples based on initial configurations     
            self._generate_file_samples()
        
        self._current_page = 1
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.SetStatusText('')

    def _on_click_cl_goback( self, event ):
        self._current_page = 0
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    
    def _on_click_cl_next( self, event ):

        # Stores the configurations into a file 
        if self._is_ct_updated:
            self._shelf_update_confidence_tab_state()        
            self._is_ct_updated = False 
        
        self._current_page = 2
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    
    def _on_click_out_goback( self, event ):
        self._current_page = 1
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    def _on_click_out_go_to_review( self, event ):
        
        if not self._is_samples_created:
            self._show_error_message("Review Error!", "Please create the sample before review.")
            return 
        
        # Sets up the review tab 
        
        self._shelf_update_sample_tab_state()
        self._setup_review_tab(self.sampled_files)
        
        # changes the tab selection 

        self._current_page = 3
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    
    
    def _on_click_io_sel_data_dir( self, event ):
        """
        Select the data folder
        Arguments: Event of item selected
        Returns: Nothing
        """
        super(RandomSampler, self)._on_click_io_sel_data_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the input folder to sample", self.dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_path = dlg.GetPath()

            self.SetStatusText("The selected data folder is %s" % self.dir_path)
            message_dialog =  wx.MessageDialog(parent = self, 
                                               message = "This may take a few minutes. \nPress OK to continue loading... ",
                                               caption = "Loading Source Documents",
                                               style = wx.ICON_INFORMATION | wx.OK)
            message_dialog.ShowModal()
            self.do_load(message_dialog)
        dlg.Destroy()
        
        self._tc_data_dir.SetValue(self.dir_path)
        self._tc_out_data_dir.SetValue(self.dir_path)
        
        self._st_num_data_dir_files.SetLabel('%d documents available' % len(self.file_list))
        self._st_out_num_data_dir_files.SetLabel('%d documents available' % len(self.file_list))
        self._is_io_updated = True
#        
#        self.sampled_files = random_sampler(self.file_list,
#                                            self.confidence_val,
#                                            self.precision_val, self.SEED)
#        self.SetStatusText('%d files are sampled out of %d files.' % (len(self.sampled_files), len(self.file_list)))
#
#        self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
#        self._st_out_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
#        self._st_num_samples.Show()
    
    
    def _generate_file_samples(self):
        '''
        This function generates file sample based on the 
        class variables such as file_list, confidence_val, 
        and precision_val and sets the sample status label     
        '''
        
        # Generate samples 

        self.sampled_files = random_sampler(self.file_list, self.confidence_val, self.precision_val, self.SEED)

        # Set status text 
        
        status_text = '%d sample documents will be selected' % len(self.sampled_files)
        self._st_num_samples.SetLabel(status_text)
        self._st_out_num_samples.SetLabel(status_text)
        self._st_num_samples.Show()
        self._st_out_num_samples.Show()
        
        self._is_ct_updated = True # it's a passive change 
    
        
    def _on_precision_changed(self, event):
        '''
        Triggers an event and updates the sample list on precision - aka 
        confidence interval change.
        Arguments: Event of new precision value
        Returns: Nothing
        '''
        
        def show_precision_error():
            self._show_error_message("Value Error!", "Please enter a confidence interval between 0 and 100.")
            self._tc_confidence_interval.ChangeValue(str(int(DEFAULT_CONFIDENCE_INTERVAL))) # Sets the default value 
            self._tc_confidence_interval.SetFocus()
            
        
        super(RandomSampler, self)._on_precision_changed(event)
        
        # Maybe intermittently null string, escaping 
        try:
            # Checks for positive values 
            ci = float(self._tc_confidence_interval.GetValue())
            if ci < 0 or ci > 99:
                show_precision_error()
                return 
            
            self.get_precision_as_float()
            self._tc_out_confidence_interval.ChangeValue(self._tc_confidence_interval.GetValue())
            self.SetStatusText('Confidence interval is changed as ' + self._tc_confidence_interval.GetValue())
            self._is_ct_updated = True # for the confidence tab updates
        except ValueError:
            show_precision_error()
            return None 
        
        self._generate_file_samples()
        
#        self.sampled_files = random_sampler(self.file_list, self.confidence_val, self.precision_val, self.SEED)
#        self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
#        self._st_out_num_samples.SetLabel('%d samples found' % len(self.sampled_files))

    
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
        
        self._tc_out_confidence_levels.SetValue(self._cbx_confidence_levels.GetValue())
        self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()) / Decimal('100')
        self.SetStatusText('Confidence level is changed as ' + self._cbx_confidence_levels.GetValue())
        self._is_ct_updated = True # for the confidence tab updates

        self._generate_file_samples()
        
#        self.sampled_files = random_sampler(self.file_list, self.confidence_val, self.precision_val, self.SEED)
#
#        self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
#        self._st_out_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
#        # self.GetSizer().Layout()

   
    def _on_click_io_sel_output_dir( self, event ):
        """ 
        Selects the output folder 
        Arguments: Nothing
        Returns: Nothing
        """
        super(RandomSampler, self)._on_click_io_sel_output_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the output folder to save",
                           self.output_dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_path = dlg.GetPath()
        dlg.Destroy()
        
        self._tc_output_dir.SetValue(self.output_dir_path)
        self._tc_out_output_dir.SetValue(self.output_dir_path)
        self.SetStatusText("The selected output folder is %s" % self.output_dir_path)
        self._is_io_updated = True
        
#    def _on_save_mark_file_status(self, e):
#        '''
#        Handles status update to upper control on saving marked file
#        Arguments: New status message
#        Returns: Nothing
#        '''
#        update_message = e.GetClientData()
#        self.SetStatusText("Saved " + str(update_message) + " files at " 
#                           + os.path.basename(self.output_dir_path))    

    
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
        
        self._is_samples_created = True  
        
        # Check if path exists
        if (not os.path.exists(self.dir_path) or
        not os.path.exists(self.output_dir_path)):
            self._show_error_message("Value Error!", "Please enter a valid Source Document Folder and Sampled Output Folder.")
            return 
        
        # Get total file size
        total_file_size = 0
        try:
            
            for x in map(os.path.getsize, self.sampled_files):
                total_file_size += long(x)
            
            total_diskspace = free_space(self.output_dir_path)
            if (total_diskspace < total_file_size):
                
                msg = "Producing the sample will take {} space. Space on your drive ({}) is insufficient.".format( print_total_file_size, convert_size(total_diskspace))
                self._show_error_message("Error - Not Enough Space", msg)
                return 
        
        except OSError:
            self._show_error_message("Sample Creation Error", "File read error! Please check access permissions.")

            
        print_total_file_size = convert_size(total_file_size)
        
        dlg = wx.MessageDialog(self,
                               "Do you really want to copy {} files to {}? This will take {} space".format(len(self.sampled_files),
                                self.output_dir_path, print_total_file_size),
                               "Confirm Copy", wx.YES|wx.NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        
        #Show status of copy
        if result == wx.ID_YES and total_file_size > 0:
            
            progress_dialog = wx.ProgressDialog(
                                                'Creating samples', 
                                                'Please wait for a few minutes...', 
                                                parent = self, 
                                                style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME)
            
            # Runs copy on a different thread
            thread = start_thread(self.do_copy, total_file_size, progress_dialog)
            progress_dialog.ShowModal()
            
            # from time import sleep
            # while thread.isAlive(): sleep(0.1)

            self.Enable(True)
            self.SetStatusText('%d samples (from %d files) are created to the output folder.' % (len(self.sampled_files), len(self.file_list)))

#            # shows the tree list control and sets defaults 
#            self.from_copy_files_dir = self.dir_path
#            self.to_copy_files_dir = self.output_dir_path
#            self._tc_results.DeleteAllItems()
#            root = self._tc_results.AddRoot(self.to_copy_files_dir)
#            self._tc_results.SetPyData(root, os.path.abspath(self.to_copy_files_dir))
#            self._tc_results.SetItemImage(root,self.folder_icon, wx.TreeItemIcon_Normal)
#            self._tc_results.SetItemImage(root,self.folder_open_icon, wx.TreeItemIcon_Expanded)
#            self.get_dirs(root,0)
#            
#            # Set defaults for all tagging panel
#            self.disable_tag_interface()
#            self.current_file_selected = ''
#            self.current_tag_list = []
#            self._panel_samples.Show(True)
#            self._panel_samples.GetSizer().Layout()
#            self.GetSizer().Layout()
        
        else :
            self.SetStatusText('Sample creation is cancelled.')
            
            
            
    #********************************************* Review Tab Handling *******************************************************  
    
    
    def _setup_review_tab(self, sampled_files):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        
        if self._lc_review_loaded: 
            return 
        
        # Sets the list control headers 
        
        self._lc_review_loaded = True 
        
        self._lc_review.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self._lc_review.InsertColumn(1, 'File Name', width=350)
        self._lc_review.InsertColumn(2, 'Responsive?', wx.LIST_FORMAT_CENTRE)
        self._lc_review.InsertColumn(3, 'Privileged?', wx.LIST_FORMAT_CENTRE)
        
        
#        # Initializes the list control 
#        
#        file_id = 0
#        for fs in sampled_files:
#            _, tail = os.path.split(fs)
#            self._lc_review.InsertStringItem(file_id, str(file_id + 1))
#            self._lc_review.SetStringItem(file_id, 1, tail)
#            self._lc_review.SetStringItem(file_id, 2, 'No')
#            self._lc_review.SetStringItem(file_id, 3, 'No')           
#            file_id += 1 

        
        # Initializes from the shelf 
        
        samples_lst = self.shelf['samples']
        file_id = 0
        for fs in samples_lst:
            self._lc_review.InsertStringItem(file_id, str(file_id + 1))
            self._lc_review.SetStringItem(file_id, 1, fs[1])
            self._lc_review.SetStringItem(file_id, 2, fs[4])
            self._lc_review.SetStringItem(file_id, 3, fs[5])           
            file_id += 1 
        
        
    
    def _on_review_list_item_selected(self, event):

        # Gets the selected row's details 
        
        self.selected_doc_id = self._lc_review.GetFocusedItem()
        
        if self.selected_doc_id < 0: return 
        
        relevant = self._lc_review.GetItem(self.selected_doc_id, 2)
        privileged = self._lc_review.GetItem(self.selected_doc_id, 3)
        
        # file_name = self._lc_review.GetItem(self.selected_doc_id, 1)
        # print 'Selected row id: ', self.selected_doc_id, file_name.Text, relevant.Text, privileged.Text     
        
        # Handles the document tags check boxes 
        
        if relevant.Text == 'Yes':
            self._chbx_doc_relevant.SetValue(True)
        else:
            self._chbx_doc_relevant.SetValue(False)
            
        if privileged.Text == 'Yes':
            self._chbx_doc_privileged.SetValue(True)
        else:
            self._chbx_doc_privileged.SetValue(False)
        
        # Shows the tags panel 
        
        self._panel_doc_tags.Show()
        self._panel_doc_tags.GetParent().GetSizer().Layout()
        
#        
#    def _on_review_list_item_deselected( self, event ):
#        '''
#        Hides the tags panel
#        '''
#        self._panel_doc_tags.Hide() 
#        self._panel_doc_tags.GetParent().GetSizer().Layout()
        

        
        
    def _on_check_box_doc_relevant( self, event ):
        '''
        Handles the selected document relevant check box 
        check and uncheck events 
         
        '''
        is_checked = self._chbx_doc_relevant.GetValue()
        if is_checked: 
            self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
        else: 
            self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
        self._is_rt_updated = True 
    
    def _on_check_box_doc_privileged( self, event ):
        '''
        Handles the selected document privileged check box 
        check and uncheck events 
         
        '''
        is_checked = self._chbx_doc_privileged.GetValue()
        if is_checked: 
            self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
        else: 
            self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
        
        self._is_rt_updated = True 


    def _on_click_clear_all_doc_tags( self, event ):
        '''
        Clear all assigned document tags from the list control 
        '''
        
        for i in range(0, len(self.sampled_files)):
            self._lc_review.SetStringItem(i, 2, 'No')
            self._lc_review.SetStringItem(i, 3, 'No')       
            
        self._chbx_doc_relevant.SetValue(False)  
        self._chbx_doc_privileged.SetValue(False)    

        self._is_rt_updated = True 

    def _on_review_list_item_activated(self, event):
        '''
        Handles the list control row double click event 
        
        '''
        
        # Gets the selected row's details 
        
        self.selected_doc_id = self._lc_review.GetFocusedItem()
        
        if self.selected_doc_id < 0: return 
        
        relevant = self._lc_review.GetItem(self.selected_doc_id, 2)
        privileged = self._lc_review.GetItem(self.selected_doc_id, 3)
        src_file_path = self.sampled_files[self.selected_doc_id]
        dest_file_path = get_destination_file_path(self.dir_path, src_file_path, self.output_dir_path)
        
        is_relevant = False 
        is_privileged = False 
        if relevant.Text == 'Yes': is_relevant = True 
        if privileged.Text == 'Yes': is_privileged = True 
        _, file_name = os.path.split(src_file_path)

        if os.path.exists(dest_file_path):
                  
            try:
                
                # Open a file   

                webbrowser.open(dest_file_path)


                # Creates a document tagging dialog 
                
                dlg = TagDocument(self, file_name, is_relevant, is_privileged)
                
                # Gets the tag selections from the dialog
                
                if dlg.ShowModal() == wx.ID_OK:
                    is_relevant = dlg._chbx_doc_relevant.GetValue()  
                    is_privileged = dlg._chbx_doc_privileged.GetValue()
                    
                    # Sets the selections to the parent window 

                    self._chbx_doc_relevant.SetValue(is_relevant)
                    if is_relevant: 
                        self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
                    else: 
                        self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
                    
                    self._chbx_doc_privileged.SetValue(is_privileged)
                    if is_privileged: 
                        self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
                    else: 
                        self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
                        
                    self._is_rt_updated = True 
                    
                # Destroys the dialog object 
                
                dlg.Destroy()


            except Exception as anyException:
                self._show_error_message("Open File Error!", str(anyException))
        
        else: 
            self._show_error_message("Open File Error!", "The file does not exist!")

        
    
    def _on_click_review_goback( self, event ):
        '''
        Handles the review tab GoBack button event 
        '''
        
        if self._is_rt_updated:
            self._shelf_update_review_tab_state()
        
        self._current_page = 2
        self.nb_config_sampler.ChangeSelection(self._current_page)
    
    def _on_click_review_exit( self, event ):
        '''
        Exits
        Arguments: Nothing
        Returns: Nothing
        '''
        if self._is_rt_updated:
            self._shelf_update_review_tab_state()
            
        self._on_close()
        
        
        
    #********************************************* END Review Tab Handling *******************************************************  

        
    
#    def _on_activated_file(self, event):
#        '''
#        Marks a file as reviewed on double click
#        Returns: None
#        Arguments: File to set status
#        '''
#        super(RandomSampler, self)._on_activated_file(event)
#        
#        #Get filename
#        if self.current_tag_list is not None:
#            self.file_tag_dict[self.current_file_selected] = self.current_tag_list
#        treeitem = event.GetItem()
#        filename  = self.get_filename_from_treenode(treeitem)
#        
#        #Nothing if directory
#        if os.path.isdir(filename):
#            return
#        
#        self.current_file_selected = filename
#        
#        
#        #Get tag for filename
#        tag = self.file_tag_dict.get(filename)
#        if tag is None:
#            self.current_tag_list = self.make_default_tag_list()
#        self.set_tag_status(self.REVIEWED_TAG_INDEX, 'True')
#        self.file_tag_dict[filename] = self.current_tag_list  
#        
#        #Open file        
#        try:
#            webbrowser.open(filename)
#        except Exception as anyException:
#            dlg = wx.MessageDialog(self, str(anyException), "Cannot open this file",
#                                    wx.ICON_ERROR)
#            dlg.ShowModal()
#        # Fire an event to reload the tag listbox
#        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
#        self.GetEventHandler().ProcessEvent(reload_tag)
#        
#        self.update_tag_in_results_tree()
#    
#    def make_default_tag_list(self):
#        '''
#        Makes a default tag to add
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        
#        tag_label = 'DEFAULT LABEL'
#        new_tag = []
#        for i in xrange(self.DEFAULT_TAGS_NUMBER): 
#            new_tag.append((tag_label, 'False'))
#        tag_0 = new_tag.pop(self.REVIEWED_TAG_INDEX)
#        tag_0 = ('Reviewed', 'False')
#        new_tag.insert(self.REVIEWED_TAG_INDEX, tag_0)
#        tag_1 = new_tag.pop(self.ACCEPT_TAG_INDEX)
#        tag_1 = ('Accept', 'False')
#        new_tag.insert(self.ACCEPT_TAG_INDEX, tag_1)
#        
#        return new_tag
#    
#    def set_tag_status(self, index, value):
#        '''
#        Sets tag indexed by index to value
#        Arguments: 
#        index: Index of tag to set
#        value: value to set, for now only use True/False 
#        '''
#        tag_name, tag_value = self.current_tag_list.pop(index)
#        tag_dirty = (tag_name, value)
#        self.current_tag_list.insert(index, tag_dirty)
#    
#    def _on_select_file(self, event):
#        '''
#        Gets tag on file select and fires an event to show status of file
#        Returns: None
#        Arguments: File to display status for 
#        '''
#        
#        super(RandomSampler, self)._on_select_file(event)
#        treeitem = event.GetItem()
#        self.get_dirs(treeitem,0)
#        self._tc_results.Refresh()
#        filename = self.get_filename_from_treenode(treeitem)
#        # Do not tag directories
#        if os.path.isdir(filename):
#            self.disable_tag_interface()
#            return
#        self.enable_tag_inteface()
#        # If no current tag, load a default tag
#        if (self.current_file_selected is None or self.current_tag_list is None):
#            self.current_tag_list  = self.make_default_tag_list()
#            self.current_file_selected = filename
#        
#        # Else save the current tag and load from the tag dictionary for next file
#        else:
#            self.file_tag_dict[self.current_file_selected] = self.current_tag_list
#            tag = self.file_tag_dict.get(filename)
#            if tag is None:
#                tag = self.make_default_tag_list()
#            self.current_file_selected = filename
#            self.current_tag_list = tag
#        
#        # Fire an event to reload the tag listbox
#        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
#        self.GetEventHandler().ProcessEvent(reload_tag)
#             
#    
#    def _on_load_tag_list( self , evt):
#        '''
#        Reloads the tag list from 'dirty' tag in the tag dictionary
#        Take note to save the last dirty tag before closing
#        Returns: None
#        Arguments: None
#        '''
#        # Format the current 'dirty' tag and add to control
#        self._tag_list.ClearAll()
#        self._tag_list.InsertColumn(0,'Tag')
#        self._tag_list.InsertColumn(1,'Status')
#        row_num = 0
#        for  tag_name, tag_value in self.current_tag_list:
#            self._tag_list.InsertStringItem(row_num, tag_name)
#            if tag_value is None: 
#                self._tag_list.SetStringItem(row_num, 1, 'False')
#                self._tag_list.SetItemData(row_num, 0)
#            else:
#                self._tag_list.SetStringItem(row_num, 1, str(tag_value))
#                if str(tag_value) == 'False':
#                    self._tag_list.SetItemData(row_num, 0)
#                if str(tag_value) == 'True':
#                    self._tag_list.SetItemData(row_num, 1)
#            row_num = row_num + 1

    def _on_click_out_exit( self, event ):
        '''
        Exits
        Arguments: Nothing
        Returns: Nothing
        '''
        self._on_close()
        
        
 
    
#    def _on_click_log_details( self, event ):
#        '''
#        Saves the marked history to a file in a specified folder
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_click_log_details(event) 
#        # Save the tag_list and Get type of selected tag to be saved
#        self.file_tag_dict[self.current_file_selected] = self.current_tag_list
#        save_files = self.file_tag_dict.keys()
#        tag_selected_type = self._cbx_tag_type.GetValue()
#        if tag_selected_type == 'Reviewed':
#            tag_selected_index = self.REVIEWED_TAG_INDEX
#        elif tag_selected_type == 'Accept':
#            tag_selected_index = self.ACCEPT_TAG_INDEX
#        else:
#            tag_selected_index = -1
#        
#        save_filename = 'Log_history_' + time.strftime("%b%d%Y%H%M%S", time.localtime())
#        fire_mark_saved  = wx.PyCommandEvent(wx.EVT_ACTIVATE.typeId)
#        try:
#            with open(os.path.join(self.to_copy_files_dir,save_filename), 'w') as file_handle:
#                file_handle.write('Data Folder:' + self.from_copy_files_dir + '\n')
#                file_handle.write('Sampled Output:' + self.to_copy_files_dir + '\n')
#                file_handle.write('Confidence Level: +/-'+str(self.confidence_val) + '\n')
#                file_handle.write('Confidence Interval: +/-'+str(self.precision_val) + '\n')
#                for save_file in save_files:
#                    
#                    # Lookahead for the required tag status
#                    is_write = True 
#                    index = 0
#                    if (tag_selected_index >= 0):
#                        for item, status in self.file_tag_dict.get(save_file):
#                            if (index == tag_selected_index and status == 'False'):
#                                is_write = False
#                                break
#                            index = index +1     
#                        
#                    # Start writing the selected file tags
#                    if is_write is True:
#                        file_handle.write(save_file)
#                        for item, status in self.file_tag_dict.get(save_file):
#                            file_handle.write('\n' + '\t'+ item + '\t' + str(status))
#                        file_handle.write('\n')
#            self.GetEventHandler().ProcessEvent(fire_mark_saved)
#        # Fire an event warning of the exception
#        except Exception as anyException:
#            fire_mark_saved.SetClientData(str(anyException))
#            self.GetEventHandler().ProcessEvent(fire_mark_saved)
#            dlg = wx.MessageDialog(self, "Unable to write save history of files.", "Error", wx.ICON_ERROR)
#            dlg.ShowModal()
   
   
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
            if self.shelf is not None:
                self.shelf.close()
            self.Destroy()

    def _show_error_message(self, _header, _message):
        '''
        Shows error messages in a pop up 
        '''
        
        dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()


    def _load_cbx_confidence_levels(self):
        '''
        Loads the supported confidence levels 
        '''
        
        confidence_levels = ['%.3f' % (w * Decimal('100')) for w in  SUPPORTED_CONFIDENCES.keys()]
        confidence_levels.sort()
        self._cbx_confidence_levels.Clear()
        for cl in confidence_levels:
            self._cbx_confidence_levels.Append(cl)


    def _init_confidence(self):
        '''
        Sets default confidence level and interval in Top Level interface
        Arguments: None
        Returns: None
        '''
        self.confidence_val = DEFAULT_CONFIDENCE_LEVEL / Decimal('100')
        items = self._cbx_confidence_levels.GetItems()
        index = -1
        try:
            index = items.index(str(DEFAULT_CONFIDENCE_LEVEL))
            self._cbx_confidence_levels.SetSelection(index)
        except ValueError:
            self._cbx_confidence_levels.ChangeValue(str(DEFAULT_CONFIDENCE_LEVEL))
        
        self._tc_out_confidence_levels.ChangeValue(str(DEFAULT_CONFIDENCE_LEVEL))
        
        # Set default confidence interval 
        self.precision_val = DEFAULT_CONFIDENCE_INTERVAL / 100
        str_precision = str(int(DEFAULT_CONFIDENCE_INTERVAL))
        self._tc_confidence_interval.ChangeValue(str_precision)
        self._tc_out_confidence_interval.ChangeValue(str_precision)

        # Hides the status messages 
        self._st_num_samples.Show(False)
        self._st_out_num_samples.Show(False)

    def _init_controls(self):
        '''
        Initialize all the application controls to defaults 
         
        '''
        
        # for the I/O tab 
        self.dir_path = '' # tempfile.gettempdir() # a cross-platform way of getting the path to the temp directory
        self.output_dir_path = '' # tempfile.gettempdir()
        self._tc_data_dir.ChangeValue('') # We shouldn't load all files from temp on init (this maybe big!!) 
        self._tc_output_dir.ChangeValue('')
        self._tc_out_data_dir.ChangeValue('')
        self._tc_out_output_dir.ChangeValue('')
        self.file_list = []
        self._st_num_data_dir_files.SetLabel('0 documents available')
        self._st_out_num_data_dir_files.SetLabel('0 documents available')

        # for the confidence tab 
        self._init_confidence()




        
    def _shelf_application_setup(self):
        '''
        Loads an existing shelf stored in the application 
        state file located in the application directory  
        '''

        # Creates the data shelf if not exists 
        self.shelf = shelve.open(SHELVE_FILE_NAME) # open -- file may get suffix added by low-level

        self._shelf_has_cfg = False 
        self._shelf_has_samples = False
        if self.shelf.has_key('config'):
            self._shelf_has_cfg = True 
            if self.shelf.has_key('samples'):
                self._shelf_has_samples = True
        
        # Loads the the application state from the shelf 
        if self._shelf_has_cfg:
            
            cfg = self.shelf['config']
            self.dir_path = cfg._data_folder 
            self.output_dir_path = cfg._output_folder 
            self.precision_val = cfg._confidence_interval
            self.confidence_val = cfg._confidence_level
            self.file_list = self.shelf['file_list'] 
            
            # already reached review page 
            if cfg._current_page == 3: 
                self._is_samples_created = True 
            
            # for the I/O tab 
            self._tc_data_dir.SetValue(self.dir_path)
            self._tc_output_dir.SetValue(self.output_dir_path)
            self._tc_out_data_dir.SetValue(self.dir_path)
            self._tc_out_output_dir.SetValue(self.output_dir_path)
            self._st_num_data_dir_files.SetLabel('%d documents available' % len(self.file_list))
            self._st_out_num_data_dir_files.SetLabel('%d documents available' % len(self.file_list))
            
            # for confidence interval 
            str_confidence_level = str(self.confidence_val * Decimal('100'))
            str_precision = str(int(self.precision_val * 100))
            self._cbx_confidence_levels.SetValue(str_confidence_level)
            self._tc_confidence_interval.ChangeValue(str_precision)
            self._tc_out_confidence_levels.ChangeValue(str_confidence_level)
            self._tc_out_confidence_interval.ChangeValue(str_precision) 
            
        # Creates the data shelf for the first time 
        else:
            
            # Initializes the necessary controls 
            self._init_controls()
            
            self.shelf['file_list'] = self.file_list
            self.shelf['config'] = RSConfig(self.dir_path, self.output_dir_path, self.precision_val, self.confidence_val) 
            self.shelf.sync()
        
        if self._shelf_has_samples:
            self._shelf_load_file_samples()
            
            
        
    
    def _shelf_update_io_tab_state(self):
        '''
        Updates the data folder and output folder 
        into the shelf
        '''    
        cfg = self.shelf['config']
        cfg._data_folder = self.dir_path
        cfg._output_folder = self.output_dir_path
        cfg._modified_date = datetime.now()
        cfg._current_page = 0 
        self.shelf['config'] = cfg
        self.shelf['file_list'] = self.file_list
        self.shelf['samples'] = self.sampled_files = [] # need to reset the samples   
        self.shelf.sync()
     
    
    def _shelf_update_confidence_tab_state(self):
        '''
        Updates the confidence level and interval  
        into the shelf
        '''    
        cfg = self.shelf['config']
        cfg._confidence_level = self.confidence_val
        cfg._confidence_interval = self.precision_val
        cfg._modified_date = datetime.now()
        cfg._current_page = 1
        self.shelf['config'] = cfg
        self._shelf_has_cfg = True 

        file_id = 0 
        samples_lst = []       
        for src_file_path in self.sampled_files:
            src_dir, file_name = os.path.split(src_file_path)
            dest_file_path = get_destination_file_path(self.dir_path, src_file_path, self.output_dir_path)
            dest_dir, _ = os.path.split(dest_file_path) # gets destination directory 
            
            fs = [file_id, file_name, src_dir, dest_dir, '', '']   
            samples_lst.append(fs) # adds every file into the samples dictionary 
            file_id += 1
        
        self.shelf['samples'] = samples_lst 
        self.shelf.sync()
        self._shelf_has_samples = True 

    def _shelf_update_sample_tab_state(self):
        cfg = self.shelf['config']
        cfg._modified_date = datetime.now()
        cfg._current_page = 2
        self.shelf['config'] = cfg
        self.shelf.sync()

    def _shelf_update_review_tab_state(self):
        '''
        This function update the state of the review tab 
        '''
        samples_lst = self.shelf['samples']
        cfg = self.shelf['config']
        
        cfg._modified_date = datetime.now()
        cfg._current_page = 3

        for file_id in range(0, len(samples_lst)):
            relevant = self._lc_review.GetItem(file_id, 2)
            privileged = self._lc_review.GetItem(file_id, 3)
            samples_lst[file_id][4] = relevant.Text
            samples_lst[file_id][5] = privileged.Text
        
        self.shelf['samples'] = samples_lst
        self.shelf['config'] = cfg
        self.shelf.sync()
        

    def _shelf_load_file_samples(self):
        '''
        This function loads already saved file samples in the shelf      
        '''
        
        # Loads samples 
        self.sampled_files = []
        
        samples_lst = self.shelf['samples']
        if len(samples_lst) == 0:
            self._shelf_has_samples = False 
            return 
        
        for fs in samples_lst: 
            self.sampled_files.append(os.path.join(fs[2], fs[1]))
        
        # Set status text 
        
        status_text = '%d sample documents will be selected' % len(self.sampled_files)
        self._st_num_samples.SetLabel(status_text)
        self._st_out_num_samples.SetLabel(status_text)
        self._st_num_samples.Show()
        self._st_out_num_samples.Show()

    
    def _shelf_update_doc_tags_state(self, file_id, is_relevant, is_privileged):
        '''
        Updates the given document sample' tags 
        '''
        
        # Gets the file dictionary 
        fs = self.shelf['samples'][file_id]
        fs[4] = is_relevant
        fs[5] = is_privileged
        self.shelf.sync()
        

    
    def _shelf_get_doc_state(self, file_id):
        '''
        Gets the file sample dictionary from 
        the application state 
        '''
        fs = self.shelf['samples'][file_id]
        return fs 
    
    

            
#    def _on_edit_status(self, event):
#        '''
#        Edits Label for Accept
#        Arguments: event identifying the row to edit
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_edit_status(event)
#        # Do not let user edit if it is the Reviewed Tag
#        row_num = event.GetIndex()
#        if (row_num is self.REVIEWED_TAG_INDEX):
#            event.Veto()
#            return
#        status =  self._tag_list.GetItemData(row_num)
#        # This is a circuitous way as you can't directly read the tag_list tag status
#        # So we save a 0/1 for the status. Supports only boolean 
#        if status is 0: 
#            self._tag_list.SetStringItem(row_num , 1, 'True')
#            self.set_tag_status(row_num, 'True')
#            self._tag_list.SetItemData(row_num , 1)
#        if status is 1: 
#            self._tag_list.SetStringItem(row_num , 1, 'False')
#            self.set_tag_status(row_num, 'False')
#            self._tag_list.SetItemData(row_num , 0)
#        
#        self.update_tag_in_results_tree()
#        
#            
#    def _on_clear_tags(self, event):
#        '''
#        Removes tags for all files
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_clear_tags(event)
#        self.file_tag_dict.clear()
#        self.current_tag_list = self.make_default_tag_list()
#        self.current_file_selected = self.to_copy_files_dir
#        reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
#        self.GetEventHandler().ProcessEvent(reload_tag)
#        
#        self.to_copy_files_dir = self.output_dir_path
#        self._tc_results.DeleteAllItems()
#        root = self._tc_results.AddRoot(self.to_copy_files_dir)
#        self._tc_results.SetPyData(root, os.path.abspath(self.to_copy_files_dir))
#        self._tc_results.SetItemImage(root,self.folder_icon, wx.TreeItemIcon_Normal)
#        self._tc_results.SetItemImage(root,self.folder_open_icon, wx.TreeItemIcon_Expanded)
#        self.get_dirs(root,0)
#        
#    def _on_add_tag(self, event):
#        '''
#        Adds a new default tag to end of file list
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_add_tag(event)
#        dlg = LabelChoiceDialog(self, "Enter Label", style=wx.CAPTION)
#        result = dlg.ShowModal()
#        if result == wx.ID_OK:
#            tag_name = dlg.label_name.GetValue()
#            tag_value = dlg.label_value.GetValue()
#
#            self.current_tag_list.append((tag_name,tag_value))
#            self.file_tag_dict[self.current_file_selected] = self.current_tag_list
#            # Refresh tags
#            reload_tag  = wx.PyCommandEvent(wx.EVT_COMMAND_FIND_REPLACE_ALL.typeId)
#            self.GetEventHandler().ProcessEvent(reload_tag)
#            # Reload the tag in tree
#            self.update_tag_in_results_tree()
        
#    def _on_edit_property(self, event):
#        '''
#        Edits tag for file
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_edit_property(event)
#        row_num = event.GetIndex()
#        # Do not let default tag_names to be edited
#        if row_num is self.REVIEWED_TAG_INDEX or row_num is self.ACCEPT_TAG_INDEX:
#            event.Veto()
#        
#        self.update_tag_in_results_tree()
#            
#    def _on_set_property(self, event):
#        '''
#        Sets tag name  for file
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        super(RandomSampler, self)._on_set_property(event)
#        # If no name set the name back to previous
#        row_num = event.GetIndex()
#        if row_num is self.REVIEWED_TAG_INDEX or row_num is self.ACCEPT_TAG_INDEX:
#            event.Veto()
#        new_tag_property_name = event.GetLabel()
#        if new_tag_property_name is '':
#            return 
#        # Pop the appropriate tag and then update it
#        tag_name, tag_value = self.current_tag_list.pop(row_num)
#        tag_dirty = (new_tag_property_name, tag_value)
#        self.current_tag_list.insert(row_num, tag_dirty)
#        
#        self.update_tag_in_results_tree()
#        
        
#    def get_dirs(self, item, level):
#        '''
#        Fetches the contents of a directory 
#        Arguments: 
#        item: Item to be expanded
#        level: Level of expansion from initial click
#        Returns: Nothing
#        '''
#        if level == self.MAX_FOLDER_DEPTH:
#            return  
#        dirname = self._tc_results.GetPyData(item)
#        dir_list = []
#        if os.path.isdir(dirname) is  True:
#            try:
#                # Dont append to list if files added previously
#                if self._tc_results.GetChildrenCount(item, False) == 0:
#                    dir_list += os.listdir(dirname)
#                    dir_list.sort()
#                    for pathname in dir_list:
#                        new_item = self._tc_results.AppendItem(item,pathname)
#                        self._tc_results.SetPyData(new_item,os.path.join(dirname, pathname))
#                        self.get_dirs(new_item, level +1)
#                        if os.path.isdir(os.path.join(dirname,pathname)):
#                            self._tc_results.SetItemImage(new_item,self.folder_icon, wx.TreeItemIcon_Normal)
#                            self._tc_results.SetItemImage(new_item,self.folder_open_icon, wx.TreeItemIcon_Expanded)
#                        else:
#                            self._tc_results.SetItemImage(new_item,self.file_icon, wx.TreeItemIcon_Normal)
#                    
#            except OSError:
#                None
#            
#    def get_filename_from_treenode(self, treeitem):
#        '''
#        Returns filename for given node
#        Arguments: treeitem to get filename for
#        Returns: filename
#        '''
#        
#        return self._tc_results.GetPyData(treeitem)
#    
#    def get_positive_tag_string(self, filename):
#        '''
#        Gets the string containing the positive tags concatenated with a tag name separator
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        # First write current dirty tag to file_tag_dict to process it
#        
#        self.file_tag_dict[self.current_file_selected] = self.current_tag_list 
#        
#        # No tag present case
#        tag_list = self.file_tag_dict.get(filename)
#        if tag_list is None:
#            return ""
#        else:
#            tag_prefix = 'tag :'
#            tag_string = ''
#            index = 0
#            for tag in tag_list:
#                tag_name, tag_status = tag
#                if index is not 0:
#                    if tag_status == 'True':
#                        tag_string = tag_string+self.TAG_NAME_SEPARATOR+tag_name
#                        index = index+1
#                else:
#                    if tag_status == 'True':
#                        tag_string = tag_string+tag_name
#                        index = index+1
#                
#                    
#            
#            # Remove the separator at the list
#            if tag_string.endswith(self.TAG_NAME_SEPARATOR):
#                tag_string = tag_string[0:(0-len(self.TAG_NAME_SEPARATOR))]
#            if tag_string <> '':
#                return tag_prefix+tag_string
#            return ''
#    
#    def update_tag_in_results_tree(self):
#        '''
#        Fires an update to load new tag in tree
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        # Get TreeItem and filename
#        tree_item = self._tc_results.GetSelection()
#        filename = self.get_filename_from_treenode(tree_item)
#                
#        # Get the displayname and positive tag and join them 
#        display_name = self._tc_results.GetItemText(tree_item).split(self.TAG_PREFIX)[0]
#        self._tc_results.SetItemText(tree_item,display_name + "  " + self.get_positive_tag_string(filename))
#        self._tc_results.Refresh()
#    
#    def disable_tag_interface(self):
#        '''
#        Disables all events on tagging inteface:
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        self._btn_add_tag.Disable()
#        self._btn_remove_tag.Disable()
#        self._tag_list.Disable()
#        
#    
#    def enable_tag_inteface(self):
#        '''
#        Disables all events on tagging inteface:
#        Arguments: Nothing
#        Returns: Nothing
#        '''
#        self._btn_add_tag.Enable()
#        self._btn_remove_tag.Enable()
#        self._tag_list.Enable()


class TagDocument(TagDocumentDialog):
    '''
    Tag document custom dialog implementation 
    '''


    def __init__(self, parent, file_name, relevant, privileged):
        '''
        Constructor
        '''
        
        # Calls the parent class's method 
        
        super(TagDocument, self).__init__(parent) 
        
        # Sets the dialog controls based on the selected document value 
        
        self.SetTitle('Tag %s' % file_name)
        self._chbx_doc_privileged.SetValue(privileged)
        self._chbx_doc_relevant.SetValue(relevant)
        
        
    def _on_click_add_tags( self, event ):
        '''
        Returns the numeric code 'ID_OK' to caller
        '''
        
        self.EndModal(wx.ID_OK) 
    
    def _on_click_clear_tags( self, event ):
        '''
        Clears the check box values 
        '''
        
        self._chbx_doc_privileged.SetValue(False)
        self._chbx_doc_relevant.SetValue(False)
        

#
#class LabelChoiceDialog(wx.Dialog):
#    def __init__(self, parent, title, style):
#        wx.Dialog.__init__(self,parent =  parent,pos = wx.DefaultPosition,size = wx.Size(200,200), title=title,
#                          style=wx.CAPTION)
#        
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        self.label_name_text = wx.StaticText( self, wx.ID_ANY, u"Enter the label name. ", wx.DefaultPosition, wx.Size( -1,-1 ) )
#        self.label_name = wx.TextCtrl(parent = self, size = wx.DefaultSize)
#        value_choices = ['True', 'False']
#        self.label_value_text = wx.StaticText( self, wx.ID_ANY, u"Enter the label value. ", wx.DefaultPosition, wx.Size( -1,-1 ))
#        self.label_value = wx.ComboBox(parent = self, size = wx.DefaultSize, choices = value_choices, style = wx.CB_READONLY | wx.CB_DROPDOWN)
#        self.label_value.SetValue('True')
#        
#      
#        
#        
#        button_panel = wx.BoxSizer(wx.HORIZONTAL)
#        ok_button = wx.Button(self, id = wx.ID_OK, label='OK')
#        close_button = wx.Button(self,id = wx.ID_CANCEL, label='CANCEL')
#        button_panel.Add(ok_button, border = 5)
#        button_panel.Add(close_button,border = 5)
#        
#        
#        sizer.Add(self.label_name_text, 0, wx.CENTER, 5)
#        sizer.Add(self.label_name, 0,  wx.CENTER, 5)
#        sizer.Add(self.label_value_text, 0,  wx.CENTER, 5)
#        sizer.Add(self.label_value, 0 ,  wx.CENTER, 5)
#
#        
#        sizer.Add(button_panel,0 , wx.ALIGN_LEFT, 5)
#
#        self.SetSizerAndFit(sizer)
#
#        
#    def OnClose(self, e):
#        
#        self.Destroy()
#        
#        self.SetSizer(sizer)

def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    RandomSampler(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()
    