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
from file_utils import find_files_in_folder, copy_files_with_dir_tree, convert_size, start_thread, copy_with_dialog



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
        
        
        self._st_num_samples.Hide()
        self.dir_path = tempfile.gettempdir() # a cross-platform way of getting the path to the temp directory
        self.output_dir_path = tempfile.gettempdir()
        self._tc_data_dir.SetValue(self.dir_path)
        self._tc_output_dir.SetValue(self.output_dir_path)
        
        self.file_list = find_files_in_folder(self.dir_path)
        self._st_num_data_dir_files.SetLabel('%d files found' % len(self.file_list))
        
        self.SEED = 2013

        self._set_confidence_level_and_interval()
        self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()
                                          )/ Decimal('100')
        self.get_precision_as_float()

        self._gdc_tree = self._gdc_results.GetTreeCtrl()
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_item_double_click,
                  self._gdc_tree, id=1)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self._on_add_list,
                  self._gdc_tree, id =1)
        
        self._panel_samples.Show(False) # make the tree list control invisible  

        self.Center()
        self.Show(True)
   
    def _on_remove_list(self, event):
        '''
        Action on double click on display panel:
        Delete a file from the selected list(display)
        '''
        self._lb_marked_files.Delete(self._lb_marked_files.GetSelection())
        
        fire_unmark  = wx.PyCommandEvent(wx.EVT_FILEPICKER_CHANGED.typeId)
        fire_unmark.SetClientData(self._lb_marked_files.GetCount())
        self.GetEventHandler().ProcessEvent(fire_unmark)

    def _on_appln_close( self, event ):
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
        super(RandomSampler, self)._on_mitem_help(event) 
    
    def _on_mitem_exit( self, event ):
        super(RandomSampler, self)._on_mitem_exit(event) 
        self._on_close()
    
    def _on_click_sel_data_dir( self, event ):
        """
        Select the data folder
        
        """
        super(RandomSampler, self)._on_click_sel_data_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the input folder to sample",
                           self.dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_path = dlg.GetPath()
        dlg.Destroy()
        self._tc_data_dir.SetValue(self.dir_path)
        self.SetStatusText("The selected input folder is %s" % self.dir_path)
        
        self.file_list = find_files_in_folder(self.dir_path)
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
        
        """
        super(RandomSampler, self)._on_click_sel_output_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the output folder to save",
                           self.output_dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_path = dlg.GetPath()
        dlg.Destroy()
        
        self._tc_output_dir.SetValue(self.output_dir_path)
        self.SetStatusText("The selected output folder is %s" % self.output_dir_path)
        
    
    def _on_click_run_sampler( self, event ):
        '''
        Handles the run sampler button click event 

        '''        
        super(RandomSampler, self)._on_click_run_sampler(event) 
        
        try:
            
            self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()
                                          )/ Decimal('100')
            self.get_precision_as_float()
            if (not os.path.exists(self.dir_path) or
                not os.path.exists(self.output_dir_path)):
                dlg = wx.MessageDialog(self, "Please enter a valid \
                input/output directory", "Error", wx.ICON_ERROR)
                dlg.ShowModal()
                return 
            
            
            self.sampled_files = random_sampler(self.file_list,
                                                self.confidence_val,
                                                self.precision_val, self.SEED)
            self.SetStatusText('%d files are sampled out of %d files.'
                               % (len(self.sampled_files), len(self.file_list)))
            self._st_num_samples.Show()
            self._st_num_samples.SetLabel('%d samples found' % len(self.sampled_files))
            
                        
            # shows the tree list control 
            self._gdc_results.SetPath(self.output_dir_path)
            self._gdc_results.SetDefaultPath(self.output_dir_path)
            
            self._panel_samples.Show(True)
            self._panel_samples.GetSizer().Layout()
            self.GetSizer().Layout()

        
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Error",
                                   wx.ICON_ERROR)
            dlg.ShowModal()
    
    def _on_update_mark(self, e):
        '''
        Handles status update to upper control on new file marked/unmarked
        '''
        file_count = e.GetClientData()
        self.SetStatusText("Number of files selected %s." %file_count)
        
    def _on_save_mark_file_status(self, e):
        '''
        Handles status update to upper control on saving marked file
        '''
        update_message = e.GetClientData()
        self.SetStatusText("Saved " + str(update_message) + " files at " 
                           + os.path.basename(self.output_dir_path))        
    def do_copy(self, total_size, dialog):
        '''
        Thread to handle copy
        '''
        copy_with_dialog(self.dir_path, self.sampled_files,
                                     self.output_dir_path, total_size, dialog)
        wx.CallAfter(dialog.Destroy)

        
    
    def _on_click_copy_files( self, event ):
        '''
        Handles event of copy files button pressed
        '''
        super(RandomSampler, self)._on_click_copy_files(event)
        total_file_size = 0
        try:
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
        
        if result == wx.ID_YES:
            progress_dialog = wx.ProgressDialog('Copying', 'Please wait...', parent = self, style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                | wx.PD_REMAINING_TIME)
            start_thread(self.do_copy, total_file_size, progress_dialog)
            progress_dialog.ShowModal()
            self.SetStatusText('%d randomly sampled files (from %d files) are copied \
            to the output folder.' % (len(self.sampled_files), len(self.file_list)))
         
    
    def _on_click_exit( self, event ):
        super(RandomSampler, self)._on_click_exit(event) 
        self._on_close()
 
 
    def _on_dclick_lb_marked_files( self, event ):
        super(RandomSampler, self)._on_dclick_lb_marked_files(event) 
        self._on_remove_list(event)
   
    def _on_click_add_list_item( self, event ):
        super(RandomSampler, self)._on_click_add_list_item(event) 
        self._on_add_list(event)
        
    
    def _on_click_remove_list_item( self, event ):
        super(RandomSampler, self)._on_click_remove_list_item(event) 
        self._on_remove_list(event)
    
    def _on_click_log_details( self, event ):
        '''
        Saves the marked history to a file in a specified folder
        '''
        super(RandomSampler, self)._on_click_log_details(event) 

        save_files = self._lb_marked_files.GetStrings()
        
        save_filename = 'Log_history_' + time.strftime("%b%d%Y%H%M%S", time.localtime())
        fire_mark_saved  = wx.PyCommandEvent(wx.EVT_ACTIVATE.typeId)
        
        try:
            with open(os.path.join(self.target_dir,save_filename), 'w') as file_handle:
                for save_file in save_files:
                    file_handle.write(save_file + '\n')
            fire_mark_saved.SetClientData(self._lb_marked_files.GetCount())
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
        
        except Exception as anyException:
            print str(anyException)
            fire_mark_saved.SetClientData(str(anyException))
            self.GetEventHandler().ProcessEvent(fire_mark_saved)
            dlg = wx.MessageDialog(self, "Unable to write save history\
             of files.", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
   
   
    def _on_close(self):
        
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy() 


    def _set_confidence_level_and_interval(self):
        
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
        
        
    def _on_item_double_click (self, event):
        '''
        Open a file
        '''
        try:
            webbrowser.open(self._gdc_results.GetFilePath())
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Cannot open this file",
                                    wx.ICON_ERROR)
            dlg.ShowModal()   


    def _on_add_list(self, event):
        '''
        Gets the file path marked in the file tree by a right click
        and adds it to display control which shows selected files 
        '''
        try:

            file_path = self._gdc_results.GetFilePath()
            if not file_path in self._lb_marked_files.GetItems():
                self._lb_marked_files.Append(file_path)
                
            fire_mark  = wx.PyCommandEvent(wx.EVT_FILEPICKER_CHANGED.typeId)
            fire_mark.SetClientData(self._lb_marked_files.GetCount())
            self.GetEventHandler().ProcessEvent(fire_mark)
        
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Cannot mark files",
                                    wx.ICON_ERROR)
            dlg.ShowModal() 

def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    RandomSampler(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()
    

