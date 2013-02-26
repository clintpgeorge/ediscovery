'''
Created on Feb 26, 2013

@author: cgeorge
'''
import os 
import wx 
import tempfile

from decimal import Decimal 
from gui.RandomSamplerGUI import RandomSamplerGUI
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from file_utils import find_files_in_folder, copy_files_with_dir_tree
from gui.file_list_control import file_list_control

class RandomSampler(RandomSamplerGUI):
    '''
    Random sampler GUI class
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        # Calls the parent class's method 
        super(RandomSampler, self).__init__(parent) 
        
        self.dir_path = tempfile.gettempdir() # a cross-platform way of getting the path to the temp directory
        self.output_dir_path = tempfile.gettempdir()
        self._tc_data_dir.SetValue(self.dir_path)
        self._tc_output_dir.SetValue(self.output_dir_path)
        
        self.SEED = 2013 
        

        self._set_confidence_level_and_interval()
        
        _bsizer_process_files = wx.BoxSizer(wx.HORIZONTAL)
        
        self._process_files_tree = file_list_control(self._panel_samples, 0, self.output_dir_path)
        _bsizer_process_files.Add(self._process_files_tree, 0, wx.EXPAND | wx.ALL, border=5)
        
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self._on_update_mark, self._process_files_tree)
        self.Bind(wx.EVT_ACTIVATE, self._on_save_mark_file_status, self._process_files_tree)
        self._process_files_tree.Show(False) # Not showing the file_list_control initially
        self._panel_samples.SetSizerAndFit(_bsizer_process_files) 

        self.Center()
        self.Show(True)
   

    def _on_appln_close( self, event ):
        super(RandomSampler, self)._on_appln_close(event) 
        self._handles_close()
    
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
        self._handles_close()
    
    def _on_click_sel_data_dir( self, event ):
        """
        Open a folder for input
        
        """
        super(RandomSampler, self)._on_click_sel_data_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the input folder to sample", self.dir_path, wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_path = dlg.GetPath()
        dlg.Destroy()
        self._tc_data_dir.SetValue(self.dir_path)
        self.SetStatusText("The selected input folder is %s" % self.dir_path)
        
    
    def _on_click_sel_output_dir( self, event ):
        """ 
        Open a folder for output 
        
        """
        super(RandomSampler, self)._on_click_sel_output_dir(event) 
        
        dlg = wx.DirDialog(self, "Choose the output folder to save", self.output_dir_path, wx.DD_DIR_MUST_EXIST)
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
            
            self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()) / Decimal('100')
            self.precision_val = float(self._tc_confidence_interval.GetValue()) / 100.0 
            
            if not os.path.exists(self.dir_path) or not os.path.exists(self.output_dir_path):
                dlg = wx.MessageDialog(self, "Please enter a valid input/output directory", "Error", wx.ICON_ERROR)
                dlg.ShowModal()
                return 
            
            file_list = find_files_in_folder(self.dir_path)
            self.SetStatusText('%d files found in %s.' % (len(file_list), self.dir_path) )
            
            sampled_files = random_sampler(file_list, self.confidence_val, self.precision_val, self.SEED)
            self.SetStatusText('%d files are sampled out of %d files.' % (len(sampled_files), len(file_list)))
            
            copy_files_with_dir_tree(self.dir_path, sampled_files, self.output_dir_path)
            self.SetStatusText('%d randomly sampled files (from %d files) are copied to the output folder.' % (len(sampled_files), len(file_list)))

            
            # shows the tree list control 
            self._process_files_tree.on_changed_output_dir(self.output_dir_path)
            self._process_files_tree.Show(True)
            
            self._panel_samples.GetSizer().Layout()
            self._panel_samples.Refresh()

        
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Error", wx.ICON_ERROR)
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
        self.SetStatusText("Saved " + str(update_message) + " files at " + os.path.basename(self.output_dir_path))

        
    
    def _on_click_copy_files( self, event ):
        super(RandomSampler, self)._on_click_copy_files(event) 
    
    def _on_click_exit( self, event ):
        super(RandomSampler, self)._on_click_exit(event) 
        self._handles_close()
   
    def _handles_close(self):
        
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy() 


    def _set_confidence_level_and_interval(self):
        
        confidence_levels = ['%.3f' % (w * Decimal('100')) for w in  SUPPORTED_CONFIDENCES.keys()]
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
            
        self._tc_confidence_interval.SetValue(str(DEFAULT_CONFIDENCE_INTERVAL))
        
        
        

def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    RandomSampler(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()
    

