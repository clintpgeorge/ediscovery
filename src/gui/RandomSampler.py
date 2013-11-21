# -*- coding: iso-8859-15 -*-
'''
Created on Feb 26, 2013

@author: abhiramj  & cgeorge
'''

import os
import wx 
import sys
import webbrowser
import shelve
import subprocess
import tempfile
import distutils
import shutil
import wx.animate
from distutils import dir_util
from gui.HTML import Table, TableRow, TableCell, link
from gui.RandomSamplerGUI import RandomSamplerGUI,LicenseDialog,HelpDialog
from gui.TaggingControl import TaggingControl
from datetime import datetime 
from decimal import Decimal 
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from file_utils import find_files_in_folder, convert_size, start_thread, copy_with_dialog, get_destination_file_path, free_space
from _winreg import OpenKey, CloseKey, QueryValueEx, HKEY_LOCAL_MACHINE
from pickle import TRUE, FALSE
from multiprocessing import Event
import shutil
#from test.test_mutants import Parent
from _pyio import open




SHELVE_FILE_EXTENSION = '.shelve'
REPORT_COMPLETE = 'complete_report.html'
REPORT_RESPONSIVE = 'responsive_docs_report.html' 
REPORT_PRIVILEGED = 'privileged_docs_report.html'
DEFAULT_FILE_VIEWER = 'IrfanView'
APP_DIR=os.getcwd()
ABOUT_TEXT =  u"""Random sampler: 
This application randomly samples the files 
from the given data folder and copies them to the output 
folder. Sample size is determined by the given 
confidence interval.
        
         
© 2013 University of Florida.  All rights reserved. 
"""
DEFAULT_TAGS = ["Responsive/Non-Responsive[Default]", "Privileged/Non-Privileged[Default]"]

def get_IrfanView_path():
    '''
    Gets IrfanView path
    '''
    # Registry key path where IrfanView is stored
    key_paths = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\IrfanView']
    subkey = "InstallLocation"
    for key_path in key_paths:
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE,key_path)
            key_value = QueryValueEx(key,subkey)
            CloseKey(key)
            path_value = key_value[0].split("\"")[1]
            return path_value
            # Entry is like this - ("C:\Program Files (x86)\IrfanView\i_view32.exe" "%1", 1)
            # We will decode this
        except WindowsError:
            pass
    return None

'''
To generate HTML reports 
'''
def rstatus(val):
    if val.strip() == '':
        return 'NA'
    else:
        return val.strip() 
    
def row_status(resp, priv):            
    if resp.strip() == '' and priv.strip() == '':
        return 'NA'
    else: 
        return 'R'

resp_colors = {}
resp_colors['Yes'] = '#2EFE9A'
resp_colors['No'] = '#58ACFA'
resp_colors['NA'] = '#D8D8D8'

priv_colors = {}
priv_colors['Yes'] = '#F78181'
priv_colors['No'] = '#F3F781'
priv_colors['NA'] = '#D8D8D8'

row_colors = {}
row_colors['R'] = '#F8E0E6' 
row_colors['NA'] = '#D8D8D8'

class LoadDialog1 ( wx.Dialog ):
    
    def __init__( self, parent,id ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Loading File", pos = wx.DefaultPosition, size = wx.Size( 450,75 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        _fgsizer_dialog = wx.FlexGridSizer( 0, 2, 0, 0 )
        _fgsizer_dialog.SetFlexibleDirection( wx.BOTH )
        _fgsizer_dialog.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        gif_fname = os.path.join(APP_DIR,"hourglass1.gif")
        gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname, pos=(10, 10))
        gif.GetPlayer().UseBackgroundColour(True)        
        self._gif_ld_image = gif
        _fgsizer_dialog.Add( self._gif_ld_image, 0, wx.ALL, 5 )
        self._gif_ld_image.Play()
        
        self._st_ld_label = wx.StaticText( self, wx.ID_ANY, u"Estimating the number of files. Please wait...\nNote: 1000000 documents approximately take 10 minutes to count\n(Times may vary depending on processor used)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self._st_ld_label.Wrap( -1 )
        self._st_ld_label.SetFont( wx.Font( 9, 74, 90, 90, False, "Tahoma" ) )
        
        _fgsizer_dialog.Add( self._st_ld_label, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.SetSizer( _fgsizer_dialog )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass

class LoadDialog ( wx.Dialog ):
    
    def __init__( self, parent,id ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Loading File", pos = wx.DefaultPosition, size = wx.Size( 400,85 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 8, 74, 93, 90, False, "Tahoma" ) )
        
        gbSizer = wx.GridBagSizer( 0, 0 )
        gbSizer.SetFlexibleDirection( wx.BOTH )
        gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        gif_fname = os.path.join(APP_DIR,"hourglass1.gif")
        gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname, pos=(10, 10))
        gif.GetPlayer().UseBackgroundColour(True)        
        self._gif_ld_image = gif
        gbSizer.Add( self._gif_ld_image, wx.GBPosition( 0, 0 ), wx.GBSpan( 2, 1 ), wx.ALL, 5 )
        self._gif_ld_image.Play()
        
        
        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Estimating the number of files. Please wait...", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )
        gbSizer.Add( self.m_staticText24, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Note: 1000000 documents approximately take 10 minutes to count\n(The time may vary depending on the system configuration)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText25.Wrap( -1 )
        self.m_staticText25.SetFont( wx.Font( 7, 74, 93, 90, False, "Tahoma" ) )
        
        gbSizer.Add( self.m_staticText25, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        
        self.SetSizer( gbSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    


class RSConfig: 
    '''
    Application State  
    '''
    def __init__(self, data_folder, output_folder, confidence_interval, confidence_level,tempdir):
        self._data_folder = data_folder
        self._output_folder = output_folder
        self._confidence_interval = confidence_interval
        self._confidence_level = confidence_level
        self._current_page = 0
        self._created_date = datetime.now() 
        self._modified_date = datetime.now() 
        self._tempdir=tempdir
        
        

class RandomSampler(RandomSamplerGUI,LicenseDialog):
    '''
    Random sampler GUI class
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        self.SEED = 2013      
                        
        # Calls the parent class's method 
        super(RandomSampler, self).__init__(parent) 
        
        # Setting the icon
        app_icon = wx.Icon(os.path.join('res','uflaw.ico'), wx.BITMAP_TYPE_ICO, 32, 32)
        self.SetIcon(app_icon)
        
        
        #setup default values for project
        self.shelf = None
        self.project_title = '' 
        self.dir_path = ''
        self.output_dir_path = ''
        self.file_list = []      
        
        from os.path import expanduser
        home = expanduser("~")
        self.directory=os.path.join(home,"E-Discovery Random Sampler")
        if(os.path.exists(self.directory)==False):
            os.mkdir(self.directory)
#         print self.directory
    
        
        # Load default tags
        #self._add_default_tags()
        self.ADDITIONAL_TAGS = []
        

#       
        self._is_io_updated = False # for the i/o tab updates  
        self._is_ct_updated = False # for the confidence tab updates
        self._is_tags_updated = False # for tags tab updates      
        self._is_rt_updated = False # for the review tab updates      
        self._lc_review_loaded = False # for the review tab table 
        self._is_samples_created = False # for the samples tab  
        self._is_project_loaded = False # Existing project loaded status
        self._prior_page_status = 0 # to keep the prior last page before application exit
        self._is_project_selected=False  
        self._is_project_new=False
        self._current_page = 0
        self.nb_config_sampler.ChangeSelection(self._current_page)
        self.Bind(wx.EVT_COMMAND_SET_FOCUS, self._on_copy_enable_review)

        # Loads confidence levels 
        self._load_cbx_confidence_levels()
        
        # Sets up the application state
        self.get_shelve_files()
        
        # setup review tag
        self._lc_review = TaggingControl( self._panel_review_tag, self)

        # Hide panel for dynamic tags
        #self.nb_config_sampler.RemovePage(2);
        self.GetSizer().Layout()
        
        self._st_new_project_title.Show(False)
        
        self.Center()
        self.Show(True)
        
    
    def get_shelve_files(self):
        '''
        Adds shelve files in cutrrent directory
        '''
        
        try:
            # Gets all shelves in the current directory
            current_dir = self.directory
            shelve_file_list = [filename for filename in os.listdir(current_dir) if filename.endswith('.shelve')]
            shelve_file_list = [filename.replace(SHELVE_FILE_EXTENSION, '') for filename in shelve_file_list]
            
            # Indexes shelf config with name
            self.shelve_config_dict = {}
            for shelve_file in shelve_file_list:
                current_shelve = shelve.open(os.path.join(self.directory,shelve_file + SHELVE_FILE_EXTENSION))
                if current_shelve.has_key('config'):
                    self.shelve_config_dict[shelve_file]= current_shelve['config']
                    self._cbx_project_title.Append(shelve_file)
                current_shelve.close()
        except Exception,e:
            self.error(e)

    def _on_appln_close( self, event ):
        '''
        Action on closing the window
        Arguments: Nothing
        Returns: Nothing
        '''
        try:
            self._on_close()
        except Exception,e:
            self.error(e)
    
    def _on_mitem_about( self, event ):
        
        try:
            super(RandomSampler, self)._on_mitem_about(event) 
            dlg = wx.MessageDialog(self, ABOUT_TEXT, "About Random Sampler", wx.OK)
            dlg.ShowModal() # Shows it
            dlg.Destroy() # finally destroy it when finished.
        except Exception,e:
            self.error(e)
    
    def _on_mitem_help( self, event ):
        '''
        Action on pressing help button
        Arguments: Nothing
        Returns: Nothing
        '''
        
        try:
            super(RandomSampler, self)._on_mitem_help(event) 
            file_path="HELP.txt"
            try:
                with open(file_path,'r') as content:
                    print_message=content.read()
            except Exception,e:
                print_message="Help file is missing or currently cannot be opened"
            dialog=HelpDialog(None)
            dialog._tc_help.SetValue(print_message)#wx.TextCtrl( self, wx.ID_ANY, print_message, wx.Point( -1,1 ), wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
            dialog.Show()
        except Exception,e:
            self.error(e)
    
    def _on_mitem_exit( self, event ):
        '''
        Action on closing the window
        Arguments: Nothing
        Returns: Nothing
        '''
        try:
            self._on_close()
        except Exception,e:
            self.error(e)
    
    def _on_nb_page_changed( self, event ):
        '''
        Handles the notebook page change event. 
        Currently it allows the user to go back 
        to prior pages 
        
        
        '''
        try:
            selected_page = event.Selection
            if selected_page < self._current_page:
                self._current_page = selected_page
            
            self.nb_config_sampler.ChangeSelection(self._current_page)
        except Exception,e:
            self.error(e)
        
    def _on_update_project_name(self, event):
        try:
            self.project_title = self._cbx_project_title.GetValue()
            # Enable all controls
            if self.project_title not in self._cbx_project_title.GetStrings() or self.project_title == '':     
                self._cbx_project_title.Enable()   
                self._tc_data_dir.Enable()
                self._tc_output_dir.Enable()
                self._btn_io_sel_data_dir.Enable()
                self._btn_io_sel_output_dir.Enable()
                self._is_project_loaded = False
            elif self._is_project_loaded == False :
                self._show_error_message("Duplicate Project!", "Project already exists, Enter a unique name")
                self.project_title = ""
                self._cbx_project_title.SetValue("")
            else :
                self._shelf_application_setup()
                self._is_project_loaded = True
        except Exception,e:
            self.error(e)
                
    def _on_set_existing_project(self, event):
        '''
        Shows info for existing loaded project
        '''
        try:
            self.project_title = self._cbx_project_title.GetValue()
            self._shelf_application_setup()
            self._is_project_loaded = True
        except Exception,e:
            self.error(e)
        
    def _on_click_io_next( self, event ):
        
        try:    
            # set project title
            if self._is_project_new==True:
                self.project_title = self._tc_io_new_project.GetValue()
                # Enable all controls
                if len(self.project_title) == 0:
                    self._show_error_message("Value Error!", "Enter a title for the project.")
                    self._cbx_project_title.SetFocus() 
                    return
                tempdir=os.path.join(self.directory,"tmp",self.project_title)
                if self._tempdir!=self.dir_path:
                    if tempdir!=self._tempdir:
                        if os.path.exists(self._tempdir):
                            os.rename(self._tempdir, tempdir)
                            self._tempdir=tempdir
                
                if self.project_title not in self._cbx_project_title.GetStrings():     
                    self._tc_data_dir.Enable()
                    self._tc_output_dir.Enable()
                    self._btn_io_sel_data_dir.Enable()
                    self._btn_io_sel_output_dir.Enable()
                    self._is_project_loaded = False
                elif self._is_project_loaded == False :
                    self._show_error_message("Duplicate Project!", "Project already exists, Enter a unique name")
                    self.project_title = ""
                    self._cbx_project_title.SetValue("")
                    return
            else:
                self.project_title = self._cbx_project_title.GetValue()
            # validations
            
            if len(self.project_title) == 0:
                self._show_error_message("Value Error!", "Enter a title for the project.")
                self._cbx_project_title.SetFocus() 
                return
            elif self.dir_path == '' or self.output_dir_path == '':
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
            
            if os.path.exists(self.output_dir_path)==False:
                os.makedirs(self.output_dir_path)
            try:
                temp=tempfile.mktemp("", "", self.output_dir_path)
                test_file=open(temp,"w")
                test_file.close()
                os.remove(temp)
            except IOError,ioe:
                self._show_error_message("Insufficient Permission", "The selected output directory might not have write permissions, Please choose another directory or provide sufficient privileges ")
                self.output_dir_path = ""
                self._tc_output_dir.SetValue("")
                self._tc_out_output_dir.SetValue("")
                return     
            
            
            if self._is_project_loaded is False:
                self._shelf_application_setup()
            #self._cbx_project_title.Disable()
            
            if self._is_io_updated:
                self._shelf_update_io_tab_state()
                self._is_io_updated = False # updates the global         
            
    
            if self._is_io_updated or not self._shelf_has_samples:    
                # Generates samples based on initial configurations
                self._generate_file_samples()
            
            self._current_page = 1
            self.nb_config_sampler.ChangeSelection(self._current_page)
            self.SetStatusText('')
        except Exception,e:
            self.error(e)

    def _on_click_cl_goback( self, event ):
        try:
            self._current_page = 0
            self.nb_config_sampler.ChangeSelection(self._current_page)
            self.SetStatusText('')
        except Exception,e:
            self.error(e)
    
    def _on_click_cl_next( self, event ):
        # Stores the configurations into a file
        try:
            if self._is_ct_updated:
                self._shelf_update_confidence_tab_state()        
                self._is_ct_updated = False
            
            self._current_page = 2
            #self._shelf_update_tags_state() remove
            self.nb_config_sampler.ChangeSelection(self._current_page)
            self.SetStatusText('')
        except Exception,e:
            self.error(e)
        
    def _on_click_out_goback( self, event ):
        try:
            self._current_page = 1
            self.nb_config_sampler.ChangeSelection(self._current_page)
            self.SetStatusText('')
        except Exception,e:
            self.error(e)
    
    def _on_click_out_go_to_review( self, event ):
        '''
        TODO: need to fix an error in application state update 
        '''
        try:
            self._tc_preview.SetValue('')
            
            if not self._is_samples_created and self._prior_page_status < 3:
                self._show_error_message("Review Error!", "Please create the sample before go to review.")
                return 
            
            if self._is_samples_created and self._prior_page_status >= 3:
                self._shelf_update_samples()
            elif self._is_samples_created:
                self._shelf_update_sample_tab_state()
                
            # Sets up the review tab 
            
            self._lc_review._setup_review_tab(self.sampled_files)
            
            # changes the tab selection 
    
            self._current_page = 3
            self.nb_config_sampler.ChangeSelection(self._current_page)
            self.SetStatusText('')
        except Exception,e:
            self.error(e)
  
    def _on_click_io_sel_data_dir( self, event ):
        """
        Select the data folder
        Arguments: Event of item selected
        Returns: Nothing
        """
    
        try:
            super(RandomSampler, self)._on_click_io_sel_data_dir(event)
            
            if self._is_project_new==True:
                self.project_title = self._tc_io_new_project.GetValue()
                # Enable all controls
                if self.project_title  in self._cbx_project_title.GetStrings():     
                    self._show_error_message("Duplicate Project!", "Project already exists, Enter a unique name")
                    self.project_title = ""
                    self._tc_io_new_project.SetValue("")
                    return
            
            if len(self.project_title) == 0:
                self._show_error_message("Value Error!", "Enter a title for the project.")
                self._cbx_project_title.SetFocus() 
                return
            
            self._shelf_has_samples = False
            
            dlg = wx.DirDialog(self, "Choose the input folder to sample", self.dir_path, wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.dir_path = dlg.GetPath()
                self._copy=True
                msg_dialog=LoadDialog(None,-1)
                msg_dialog.Show()
                msg_dialog.Update()
                file_count,pst_count,pst_size=self.generate_files_preprocess()
                msg_dialog.Destroy()
               
                num_files=file_count+pst_count#set progress maximum value of progress ar to total number of files
                update_count=int(0.2*file_count)+1#update progess bar after ever 20% of ordinary files and PST files 
                if(self._copy==False):
                    return 
                wait_str=""
                wait_time=(file_count*600/1000000)+(file_count*0.05/update_count)+(pst_count*0.05)+(pst_size*1200/1024)
                wait_time=int(wait_time)
                
                if (wait_time<3600):
                    minutes=int(wait_time/60)+1
                    wait_str="File may take approximately "+ str(minutes) +" minutes"
                else:
                    hours=int(wait_time/3600)
                    minutes=int((wait_time%3600)/60)+1
                    wait_str="File may take approximately "+ str(hours) +" hours"
                    if(minutes>0):
                        wait_str+=" "+ str(minutes) +" minutes"
                    
                #exit()
                wait_str+=" to load.\n(The time may vary depending on the system configuration)\n You may minimize the window while we load your documents."
                
                self.SetStatusText("The selected data folder is %s" % self.dir_path)
                message_dialog = wx.ProgressDialog(
                                                    'Loading Files', 
                                                    'Loading source documents. '+wait_str, 
                                                    parent = self, maximum=num_files)

                message_dialog.ShowModal()
                self.generate_files(message_dialog,num_files,update_count)
                message_dialog.Destroy()
                self._tc_data_dir.SetValue(self.dir_path)
                self._tc_out_data_dir.SetValue(self.dir_path)
                self._tc_project_title.SetValue(self.project_title)
                
                self._st_num_data_dir_files.SetLabel('%d documents' % len(self.file_list))
                self._st_out_num_data_dir_files.SetLabel('%d documents' % len(self.file_list))
                self._is_io_updated = True
            else:
                self.SetStatusText("")
            dlg.Destroy()
            
            
        except Exception,e:
            self.error(e)
        
    def generate_files_preprocess(self):
        try:
            wx.BeginBusyCursor()
            pst_count=0
            pst_size=0
            file_count=0
            for root, _, files in os.walk(self.dir_path):
                for file_name in files:
                    complete_fileName=os.path.join(root, file_name)
                    _, fileExtension = os.path.splitext(complete_fileName)
                    if fileExtension==".pst":
                        pst_count+=1
                        pst_size+=os.path.getsize(complete_fileName)
                    else:
                        file_count+=1
            if pst_count>0:
                self._tempdir=os.path.join(self.directory,"tmp",self.project_title)
                if(os.path.exists(self._tempdir)):
                    shutil.rmtree(self._tempdir)
                os.makedirs(self._tempdir)
            else:
                self._tempdir=self.dir_path
            
            wx.EndBusyCursor()
            pst_size=int(pst_size/(1024*1024))
            return file_count,pst_count,pst_size
        except Exception,e:
            self.error(e)
   
    def generate_files(self,dialog,num_files,update_count):
        file_list_tmp=[]
        count=0
        file_count=0
        
        error_str=""
        for root, _, files in os.walk(self.dir_path):
            for file_name in files:
                #wx.CallAfter(self._statusbar.SetLabel,"abc")
                
                complete_fileName=os.path.join(root, file_name)
                fileName, fileExtension = os.path.splitext(complete_fileName)
                if fileExtension==".pst":
                    pstTemp=os.path.join(self._tempdir,os.path.basename(fileName))
                    os.mkdir(pstTemp)
                    
                    shutil.copy(complete_fileName, os.path.abspath(pstTemp))
                    abc=os.path.basename(complete_fileName)
                    pstTempFile=os.path.join(pstTemp,abc)

                    try:
                        self.convert_pst(pstTempFile, pstTemp)
                        
                        for rootPST, _, filesPST in os.walk(pstTemp):
                            for file_name_PST in filesPST:
                                file_list_tmp.append(os.path.join(rootPST, file_name_PST))
                    except Exception,e:
                        error_str+=file_name
                    count=count+1
                    dialog.Update(count)
                    wx.MilliSleep(50)
                else:
                    
                    file_list_tmp.append(os.path.join(root, file_name))
                    file_count+=1
                    if file_count==update_count:
                        count=count+file_count
                        file_count=0
                        dialog.Update(count)
                        wx.MilliSleep(50)
        dialog.Update(num_files)
        
        self.file_list=file_list_tmp
        
        if(error_str!=""):
            try:
                fileName=os.path.join(os.path.expanduser('~'),"E-Discovery Random Sampler","error.log")
                file_err=open(fileName,"a") 
                date=unicode(datetime.now())
                file_err.flush()
                file_err.write(date+u"=>")
                file_err.write(u"Could not read "+ unicode(error_str)+u"\n")
            except Exception,ex:
                print ex
    
            
            self._show_error_message("Copy Error","Source PST files could not be processed, for more information please check " + fileName)
            file_err.close()
        
    def _generate_file_samples(self):
        '''
        This function generates file sample based on the 
        class variables such as file_list, confidence_val, 
        and precision_val and sets the sample status label     
        '''
        try:
            # Generate samples
            self.sampled_files = random_sampler(self.file_list, self.confidence_val, self.precision_val, self.SEED)
    
            # Set status text 
            
            status_text = '%d sample documents will be selected' % len(self.sampled_files)
            self._st_num_samples.SetLabel(status_text)
            self._st_out_num_samples.SetLabel(status_text)
            self._st_num_samples.Show()
            self._st_out_num_samples.Show()
            
            self._is_ct_updated = True # it's a passive change 
        except Exception,e:
            self.error(e)
        
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
            if ci <= 0 or ci > 99:
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
        try:
        
            super(RandomSampler, self)._on_confidence_changed(event)
            
            self._tc_out_confidence_levels.SetValue(self._cbx_confidence_levels.GetValue())
            self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()) / Decimal('100')
            self.SetStatusText('Confidence level is changed as ' + self._cbx_confidence_levels.GetValue())
            self._is_ct_updated = True # for the confidence tab updates
    
            self._generate_file_samples()
        except Exception,e:
            self.error(e)
        
    def _on_click_io_sel_output_dir( self, event ):
        """ 
        Selects the output folder 
        Arguments: Nothing
        Returns: Nothing
        """
        try:
            super(RandomSampler, self)._on_click_io_sel_output_dir(event) 
            
            if self._is_project_new==True:
                self.project_title = self._tc_io_new_project.GetValue()
                # Enable all controls
                if self.project_title  in self._cbx_project_title.GetStrings():     
                    self._show_error_message("Duplicate Project!", "Project already exists, Enter a unique name")
                    self.project_title = ""
                    self._tc_io_new_project.SetValue("")
                    return
            
            if len(self.project_title) == 0:
                self._show_error_message("Value Error!", "Enter a title for the project.")
                self._cbx_project_title.SetFocus() 
                return
            
            dlg = wx.DirDialog(self, "Choose the output folder to save",
                               self.output_dir_path, wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                self.output_dir_path = dlg.GetPath()
                #test_file=os.path.join(self.output_dir_path,datetime.now())       
            dlg.Destroy()
            
            self._tc_output_dir.SetValue(self.output_dir_path)
            self._tc_out_output_dir.SetValue(self.output_dir_path)
            self._tc_project_title.SetValue(self.project_title)
            self.SetStatusText("The selected output folder is %s" % self.output_dir_path)
            self._is_io_updated = True
        except Exception,e:
            self.error(e)
              
    def do_copy(self, total_size, dialog):
        '''
        Thread to handle copy
        Arguments: Total size of copy, Handle to dialog
        '''
        try:
            wx.BeginBusyCursor()
            copy_with_dialog(self.dir_path,self._tempdir, self.sampled_files,
                                         self.output_dir_path, total_size, dialog)
            finish_copy_event  = wx.PyCommandEvent(wx.EVT_COMMAND_SET_FOCUS.typeId)
            self.GetEventHandler().ProcessEvent(finish_copy_event)
            wx.EndBusyCursor()
        except Exception,e:
            self.error(e)        
        
    def convert_pst(self, pstfilename,temp):
        '''
        This method will be a little creative 
        '''        
        #ToDo....NOT SAFE
        try:
            subprocess.check_output(['readpst', '-o', os.path.abspath(temp), '-e', '-b', '-S', pstfilename], stderr=subprocess.STDOUT,shell=True)
            print temp
            print pstfilename
            #print response
            for root, _, files in os.walk(temp):
                for file_name in files:
                    filename=os.path.join(root, file_name)
                    _, fileExtension = os.path.splitext(filename)
                    if fileExtension!="":
                        os.remove(filename)
        except Exception, e:
            raise
            
    def _on_click_copy_files( self, event ):
        '''
        Handles event of copy files button pressed
        Arguments: Nothing
        Returns: Nothing
        '''
        
        try:
            super(RandomSampler, self)._on_click_copy_files(event)
              
            # Check if path exists
            if (not os.path.exists(self.dir_path) or
            not os.path.exists(self.output_dir_path)):
                self._show_error_message("Value Error!", "Please enter a valid Source Document Folder and Sampled Output Folder.")
                return 
            
            # Get total file size
            total_file_size = 0
            try:
                for x in map(os.path.getsize, self.sampled_files):
                    if long(x)==0:# Hack-- To handle if all files are of zero bytes
                        total_file_size +=1
                    else:
                        total_file_size += long(x)
            
                
                total_diskspace = free_space(self.output_dir_path)
                if (total_diskspace < total_file_size):
                    
                    msg = "Producing the sample will take {} space. Space on your drive ({}) is insufficient.".format( total_file_size, convert_size(total_diskspace))
                    self._show_error_message("Error - Not Enough Space", msg)
                    return 
            
            except OSError as anyExp:
                self._show_error_message("Error creating samples", "There was an error reading some files! Please check that you have access to the files.")
                return
    
            
            #Show status of copy
            if total_file_size >= 0:
        
                progress_dialog = wx.ProgressDialog(
                                                    'Creating samples', 
                                                    'Please wait for a few minutes...', 
                                                    parent = self)
                
                # Runs copy on a different thread
                thread = start_thread(self.do_copy, total_file_size, progress_dialog)
                progress_dialog.ShowModal()
                thread.join()
                #progress_dialog.Show(False)
                #self._btn_out_go_to_review.Enable()
                self._btn_out_go_to_review.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ))
                #self._btn_out_go_to_review.SetLabel("Next(Samples Created, Go to Review)")
                self.shelf['isSampleCreated']=True
                self._is_samples_created=True
                self.shelf.sync()
                self.Enable(True)
                self.SetStatusText('%d samples (from %d files) are created to the output folder.' % (len(self.sampled_files), len(self.file_list)))
                    
            else :
                self.SetStatusText('Sample creation is cancelled.')
        except Exception, e:
            self.error(e)
     
    #Check            
    def _add_default_tags(self):
        '''
        Adds the default tags to the listbox of tags
        '''
        try:
            for tag in DEFAULT_TAGS:
                self._lbx_tag.Append(tag)
        except Exception,e:
            self.error(e)
         
    def _on_rbx_responsive_updated( self, event ):
        '''
        Handles the selected document responsive check box 
        check and uncheck events 
         
        '''
        try:
            responsive_status = self._rbx_responsive.GetStringSelection() 
            if responsive_status == 'Yes': 
                self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
            elif responsive_status == 'No': 
                self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
            elif responsive_status == 'Unknown': 
                self._lc_review.SetStringItem(self.selected_doc_id, 2, '')
            self._is_rt_updated = True
        except Exception,e:
            self.error(e) 
    
    def _on_rbx_privileged_updated( self, event ):
        '''
        Handles the selected document privileged check box 
        check and uncheck events 
         
        '''
        try:
            privileged_status = self._rbx_privileged.GetStringSelection() 
            if privileged_status == 'Yes': 
                self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
            elif privileged_status == 'No': 
                self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
            elif privileged_status == 'Unknown': 
                self._lc_review.SetStringItem(self.selected_doc_id, 3, '')
            self._is_rt_updated = True
        except Exception,e:
            self.error(e)  

    def _on_click_clear_all_doc_tags( self, event ):
        '''
        Clear all assigned document tags from the list control 
        '''
        try:
            for i in range(0, len(self.sampled_files)):
                self._lc_review.SetStringItem(i, 2, '')
                self._lc_review.SetStringItem(i, 3, '')       
            
            self._rbx_responsive.SetStringSelection('Unknown')    
            self._rbx_privileged.SetStringSelection('Unknown')  
                
    
            self._is_rt_updated = True
        except Exception,e:
            self.error(e)
            
    def _on_click_review_goback( self, event ):
        '''
        Handles the review tab GoBack button event 
        '''
        try:
            if self._is_rt_updated:
                self._shelf_update_review_tab_state()
            
            self._current_page = 2
            self.nb_config_sampler.ChangeSelection(self._current_page)
        except Exception,e:
            self.error(e)
    
    def _on_click_review_exit( self, event ):
        '''
        Exits
        Arguments: Nothing
        Returns: Nothing
        '''
        try:
            self._on_close()
        except Exception,e:
            self.error(e)
        
    def _on_click_review_gen_report( self, event ):
        if self._is_rt_updated:
            self._shelf_update_review_tab_state()
        
        # Separate report types
        report_type = self._cbx_report_types.GetValue()
        try:
            samples_lst = self.shelf['samples']
            if report_type == 'Responsive':
                file_name = os.path.join(self.output_dir_path, REPORT_RESPONSIVE)   
                responsive = []
                for fs in samples_lst: 
                    if fs[4] == 'Yes': 
                        responsive.append(fs)
                if len(responsive) == 0:
                    self._show_error_message('Report Generation', 'There are no responsive documents available.')
                    return 
                html_body = self._gen_responsive_html_report(responsive)
            elif report_type == 'Privileged':
                file_name = os.path.join(self.output_dir_path, REPORT_PRIVILEGED)   
                privileged = []
                for fs in samples_lst: 
                    if fs[5] == 'Yes': 
                        privileged.append(fs)
                if len(privileged) == 0:
                    self._show_error_message('Report Generation', 'There are no privileged documents available.')
                    return 
                html_body = self._gen_privileged_html_report(privileged)
            elif report_type == 'All':
                file_name = os.path.join(self.output_dir_path, REPORT_COMPLETE)   
                responsive = []
                privileged = []
                for fs in samples_lst: 
                    if fs[4] == 'Yes': 
                        responsive.append(fs)
                    if fs[5] == 'Yes': 
                        privileged.append(fs)
                html_body = self._gen_complete_html_report(samples_lst, responsive, privileged)
            
            
            # Saves into a file path 
            self._save_html_report(html_body, file_name)
            
            # Open the HTML report in the default web browser 
            webbrowser.open(file_name)
        except Exception,e:
            # Report generation failed 
            self.error(e)
                    
    def _save_html_report(self, html_body, file_name):
        '''
        Stores into a file 
        '''
        
        try:
            with open(file_name, "w") as hw: 
                hw.write(unicode(
                """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                <html>
                <head>
                    <title>Document Sample Review Report</title>
                </head>
                <body style="font-family:verdana,helvetica;font-size:9pt">
                <h2>Document Sample Review Report</h2>
                
                Report overview: 
                
                <br/><br/>
                """))
                
                hw.write(unicode(self._gen_specifications_html()))
    
                hw.write(unicode(html_body))
    
                hw.write(unicode(
                """
                <hr/>
                <p>Report is generated on: %s</p>
                </body>
                </html>""" % datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))
        except Exception, e:
            print e
            self.error(e)

    def _gen_specifications_html(self): 
        try:
            hrow = TableRow(cells=['Sampler Specifications', 'Entries'], bgcolor='#6E6E6E')
            setting_table = Table(header_row=hrow, border=0)
    
            config_cell = TableCell("Source document folder", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(self.dir_path, bgcolor = '#CEF6F5', align = 'left')
            setting_table.rows.append([config_cell, setting_cell])
            
            config_cell = TableCell("Sampled output folder", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(self.output_dir_path, bgcolor = '#CEF6F5', align = 'left')
            setting_table.rows.append([config_cell, setting_cell])
            
            config_cell = TableCell("Confidence level (%)", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(self.confidence_val*100, bgcolor = '#CEF6F5', align = 'right')
            setting_table.rows.append([config_cell, setting_cell])
            
            config_cell = TableCell("Confidence interval (%)", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(self.precision_val*100, bgcolor = '#CEF6F5', align = 'right')
            setting_table.rows.append([config_cell, setting_cell])
            
            config_cell = TableCell("Total documents in the source document folder", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(len(self.file_list), bgcolor = '#CEF6F5', align = 'right')
            setting_table.rows.append([config_cell, setting_cell])
            
            config_cell = TableCell("The sample size", bgcolor = '#CEF6F5', align = 'left')
            setting_cell = TableCell(len(self.sampled_files), bgcolor = '#CEF6F5', align = 'right')
            setting_table.rows.append([config_cell, setting_cell])
            
            return str(setting_table)
        except Exception,e:
            self.error(e)
        
    def _gen_complete_html_report(self, samples, responsive, privileged):
        try:
            # Generate HTML tags for all documents 
            hrow = TableRow(cells=['#', 'File Name', 'Responsive', 'Privileged'], bgcolor='#6E6E6E')
            all_table = Table(header_row=hrow)
            for fs in samples:
                
                rc_colr = resp_colors[rstatus(fs[4])]
                pc_colr = priv_colors[rstatus(fs[5])]
                r_colr = row_colors[row_status(fs[4], fs[5])]
                num_cell = TableCell(fs[0] + 1, bgcolor=r_colr, align='center')
                file_name = link(fs[1], os.path.join(fs[3], fs[1]))
                fn_cell = TableCell(file_name, bgcolor=r_colr)
                resp_cell = TableCell(fs[4], bgcolor=rc_colr, align='center')
                priv_cell = TableCell(fs[5], bgcolor=pc_colr, align='center')
                
                all_table.rows.append([num_cell, fn_cell, resp_cell, priv_cell])
            
            html_body = """
            %s 
    
            %s 
    
            <hr/>
            <h3>Complete Sample</h3>
            %s 
            <br/>
            """ % (self._gen_responsive_html_report(responsive), self._gen_privileged_html_report(privileged), str(all_table))
            
            return html_body
        except Exception,e:
            self.error(e)
       
    def _gen_responsive_html_report(self, responsive):
        '''
        Generate HTML tags for responsive documents 
        '''
        try:
            if len(responsive) == 0: return ''
            hrow = TableRow(cells=['#', 'File Name'], bgcolor='#6E6E6E')
            resp_table = Table(header_row=hrow)
            for fs in responsive:
                r_colr = resp_colors['Yes']
                num_cell = TableCell(fs[0] + 1, bgcolor=r_colr, align='center')
                file_name = link(fs[1], os.path.join(fs[3], fs[1]))
                fn_cell = TableCell(file_name, bgcolor=r_colr)
                resp_table.rows.append([num_cell, fn_cell])
                
            html_body = """
            <hr/>
            <h3>Responsive Documents</h3>
            %s 
            <br/>
            """ % str(resp_table)
            
            return html_body
        except Exception,e:
            self.error(e)
      
    def _gen_privileged_html_report(self, privileged):
        '''
        Generate HTML tags for privileged documents 
        '''
        try:
            if len(privileged) == 0: return ''
            
            hrow = TableRow(cells=['#', 'File Name'], bgcolor='#6E6E6E')
            priv_table = Table(header_row=hrow)
            for fs in privileged:
                r_colr = priv_colors['Yes']
                num_cell = TableCell(fs[0] + 1, bgcolor=r_colr, align='center')
                file_name = link(fs[1], os.path.join(fs[3], fs[1]))
                fn_cell = TableCell(file_name, bgcolor=r_colr)
                priv_table.rows.append([num_cell, fn_cell])
                
            html_body = """
            <hr/>
            <h3>Privileged Documents</h3>
            %s 
            <br/>
            """ % str(priv_table)
            
            return html_body
        except Exception,e:
            self.error(e)
        
    #********************************************* END Review Tab Handling *******************************************************  

    def _on_click_out_exit( self, event ):
        '''
        Exits
        Arguments: Nothing
        Returns: Nothing
        '''
        try:
            self._on_close()
        except Exception,e:
            self.error(e)   
   
    def _on_close(self):
        '''
        Closes the Application after confirming with user
        Arguments: Nothing
        Returns: Nothing
        '''
        try:
            dlg = wx.MessageDialog(self,
                                   "Do you really want to close this application?",
                                   "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_OK:
                
                # Handles the shelf 
                if self.shelf is not None:
                    if self._is_rt_updated:
                        self._shelf_update_review_tab_state()
                    self.shelf.close()
                
                self.Destroy()
        except Exception,e:
            self.error(e)

    def _show_error_message(self, _header, _message):
        '''
        Shows error messages in a pop up 
        '''
        try:
            dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        except Exception,e:
            self.error(e)

    def _load_cbx_confidence_levels(self):
        '''
        Loads the supported confidence levels 
        '''
        try:
            confidence_levels = ['%.3f' % (w * Decimal('100')) for w in  SUPPORTED_CONFIDENCES.keys()]
            confidence_levels.sort(reverse=True)
            self._cbx_confidence_levels.Clear()
            for cl in confidence_levels:
                self._cbx_confidence_levels.Append(cl)
        except Exception,e:
            self.error(e)

    def _init_confidence(self):
        '''
        Sets default confidence level and interval in Top Level interface
        Arguments: None
        Returns: None
        '''
        try:
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
        except Exception,e:
            self.error(e)

    def _init_controls(self):
        '''
        Initialize all the application controls to defaults 
         
        '''

        # for the confidence tab 
        try:
            self._init_confidence()
        except Exception,e:
            self.error(e)

    def _shelf_application_setup(self):
        '''
        Loads an existing shelf stored in the application 
        state file located in the application directory  
        '''
        # Creates the data shelf if not exists 
        try:
            self.shelf = shelve.open(os.path.join(self.directory,self.project_title+SHELVE_FILE_EXTENSION),writeback=TRUE) # open -- file may get suffix added by low-level
            if self._is_project_new:
                self._cbx_project_title.Append(self.project_title)
                self._cbx_project_title.SetValue(self.project_title)
                self._chk_io_new_project.SetValue(False)
                self._is_project_new=False
                self._tc_io_new_project.Disable()
                self._tc_io_new_project.SetValue("Title of new project...")
                self._cbx_project_title.Enable()
                self._is_samples_created=False
                ##self._btn_out_go_to_review.Enable(False)
                self._btn_out_go_to_review.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )
                #self._btn_out_go_to_review.SetLabel("Please Create Samples")
                
                
    
            self._shelf_has_cfg = False 
            self._shelf_has_samples = False
            if self.shelf.has_key('config'):
                self._shelf_has_cfg = True 
                if self.shelf.has_key('samples'):
                    self._shelf_has_samples = True
                    if self.shelf['isSampleCreated']:
                        self._is_samples_created = True
                        #self._btn_out_go_to_review.Enable()
                        self._btn_out_go_to_review.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ))
                        #self._btn_out_go_to_review.SetLabel("Next(Samples Created, Go to Review)")
                    else:
                        self._is_samples_created = False
                        #self._btn_out_go_to_review.Enable(False)
                        self._btn_out_go_to_review.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )
                        #self._btn_out_go_to_review.SetLabel("Please Create Samples")
            
            # Loads the the application state from the shelf 
            if self._shelf_has_cfg:
                
                cfg = self.shelf['config']
                self.dir_path = cfg._data_folder 
                self.output_dir_path = cfg._output_folder 
                self.precision_val = cfg._confidence_interval
                self.confidence_val = cfg._confidence_level
                self._prior_page_status = cfg._current_page
                self._tempdir=cfg._tempdir
                
                #print os.getcwd()
                if os.path.isdir(self.dir_path)==False:
                    self._show_error_message("Read Error","Input Folder is missing, Project will be deleted")
                    self.shelf.close()
                    os.remove(os.path.join(self.directory,self.project_title+SHELVE_FILE_EXTENSION))
                    self.project_title=""
                    self._cbx_project_title.Clear()
                    self.get_shelve_files()
                    self._cbx_project_title.SetValue(self.project_title)
                    return
                else:
                    if os.path.isdir(self._tempdir)==False:
                        self._show_error_message("Read Error","Temporary Folder corresponding to missing, Project will be deleted")
                        self.shelf.close()
                        os.remove(os.path.join(self.directory,self.project_title+SHELVE_FILE_EXTENSION))
                        self.project_title=""
                        self._cbx_project_title.Clear()
                        self.get_shelve_files()
                        self._cbx_project_title.SetValue(self.project_title)
                        return
                    
                        
                self.file_list = self.shelf['file_list'] 
                self.ADDITIONAL_TAGS = self.shelf['additional_tags']
    
                # for the I/O tab 
                self._tc_data_dir.SetValue(self.dir_path)
                self._tc_output_dir.SetValue(self.output_dir_path)
                self._tc_out_data_dir.SetValue(self.dir_path)
                self._tc_out_output_dir.SetValue(self.output_dir_path)
                self._tc_project_title.SetValue(self.project_title)
                self._st_num_data_dir_files.SetLabel('%d documents' % len(self.file_list))
                self._st_out_num_data_dir_files.SetLabel('%d documents' % len(self.file_list))
                
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
                #if self._is_pst_project==False:
                #    self._tempdir=self.dir_path
                self.shelf['file_list'] = self.file_list
                self.shelf['additional_tags'] = []
                self.shelf['config'] = RSConfig(self.dir_path, self.output_dir_path, self.precision_val, self.confidence_val, self._tempdir) 
                self.shelf.sync()
            
            if self._shelf_has_samples:
                self._shelf_load_file_samples()
                
            self.shelf.sync()
        except Exception,e:
            self.error(e)
         
    def _shelf_update_io_tab_state(self):
        '''
        Updates the data folder and output folder 
        into the shelf
        '''    
        try:
            cfg = self.shelf['config']
            cfg._data_folder = self.dir_path
            cfg._output_folder = self.output_dir_path
            cfg._modified_date = datetime.now()
            cfg._current_page = 0 
            self.shelf['config'] = cfg
            self.shelf['file_list'] = self.file_list
            self.shelf['samples'] = self.sampled_files = [] # need to reset the samples   
            self.shelf['isSampleCreated']=False
            self._is_samples_created=False
            self._btn_out_go_to_review.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )
            self.shelf.sync()
        except Exception,e:
            self.error(e)
         
    def _shelf_update_confidence_tab_state(self):
        '''
        Updates the confidence level and interval  
        into the shelf
        '''    
        try:
            cfg = self.shelf['config']
            cfg._confidence_level = self.confidence_val
            cfg._confidence_interval = self.precision_val
            cfg._modified_date = datetime.now()
            cfg._current_page = 1
            self.shelf['config'] = cfg
            self._shelf_has_cfg = True
            self._is_samples_created=False
            self._btn_out_go_to_review.SetBackgroundColour( wx.Colour( 224, 224, 224 ) ) 
            self.shelf.sync()
    
            self._shelf_update_samples()
        except Exception,e:
            self.error(e)

    def _shelf_update_samples(self):
        '''
        Update the shelf with new samples 
        '''
        try:
            file_id = 0 
            samples_lst = []       
            for src_file_path in self.sampled_files:
                src_dir, file_name = os.path.split(src_file_path)
                dest_file_path = get_destination_file_path(self.dir_path,self._tempdir, src_file_path, self.output_dir_path)
                dest_dir, _ = os.path.split(dest_file_path) # gets destination directory 
                
                fs = [file_id, file_name, src_dir, dest_dir, '', '']   
                samples_lst.append(fs) # adds every file into the samples dictionary 
                file_id += 1
            
            self.shelf['samples'] = samples_lst 
            self.shelf.sync()
            self._shelf_has_samples = True
        except Exception,e:
            self.error(e) 

    #check

    def _shelf_update_sample_tab_state(self):
        try:
            cfg = self.shelf['config']
            cfg._modified_date = datetime.now()
            cfg._current_page = 3
            self.shelf['config'] = cfg
            self.shelf.sync()
        except Exception,e:
            self.error(e)

    def _shelf_update_review_tab_state(self):
        '''
        This function update the state of the review tab 
        '''
        try:
            samples_lst = self.shelf['samples']
            cfg = self.shelf['config']
            
            cfg._modified_date = datetime.now()
            cfg._current_page = 4
    
            for file_id in range(0, len(samples_lst)):
                responsive = self._lc_review.GetItem(file_id, 2)
                privileged = self._lc_review.GetItem(file_id, 3)
                samples_lst[file_id][4] = responsive.Text
                samples_lst[file_id][5] = privileged.Text
            
            self.shelf['samples'] = samples_lst
            self.shelf['config'] = cfg
            self.shelf.sync()
        except Exception:
            self.error(e)
        
    def _shelf_load_file_samples(self):
        '''
        This function loads already saved file samples in the shelf      
        '''
        try:
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
        except Exception:
            self.error(e)

    def _shelf_update_doc_tags_state(self, file_id, is_responsive, is_privileged, other_tags):
        '''
        Updates the given document sample' tags 
        '''
        try:
            # Gets the file dictionary 
            fs = self.shelf['samples'][file_id]
            fs[4] = is_responsive
            fs[5] = is_privileged
            fs[6] = other_tags
            self.shelf.sync()
        except Exception:
            self.error(e)
            
    def _shelf_get_doc_state(self, file_id):
        '''
        Gets the file sample dictionary from 
        the application state 
        '''
        try:
            fs = self.shelf['samples'][file_id]
            return fs
        except Exception,e:
            self.error(e)
    
    def _on_copy_enable_review(self, event):
        try:
            self._is_samples_created = True
            self._btn_out_go_to_review.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT )) 
        except Exception,e:
            self.error(e)
            
    def on_right_click_menu(self, event):
        '''
        Displays context menu on right-click 
        ''' 
        try:
            self.PopupMenu(self.menu_open)
        except Exception,e:
            self.error(e)
            
    def on_popup_open_file_viewer(self, event):
        '''
        Opens irfanview with file as argument
        '''
        
        try:
            dest_file_path = self.get_selection_file_name()
            if self.viewer_executable_location is None:
                self._show_error_message("File Open Error!", "Could not open file with " + DEFAULT_FILE_VIEWER + ". Check if "  + DEFAULT_FILE_VIEWER + " is installed.")
            try:
                subprocess.call([self.viewer_executable_location, dest_file_path])
                
                file_name = os.path.basename(dest_file_path)
                responsive_status = self._rbx_responsive.GetStringSelection()
                privileged_status = self._rbx_privileged.GetStringSelection()
                self.make_tag_popup(file_name,responsive_status, privileged_status)
            except Exception,e:
                self._show_error_message("File Open Error!", "Could not open file with " + DEFAULT_FILE_VIEWER + ". Check if "  + DEFAULT_FILE_VIEWER + " can open this file.")
        except Exception,e:
            self.error(e)
            
        
    def on_popup_open_file_other(self, event):
        '''
        Lets user choose application for viewing file
        '''
        try:
            dest_file_path = self.get_selection_file_name()
            wildcard = "All executables (*.exe)|*.exe| All files (*.*)|*.*"
            
            
            program_dialog = wx.FileDialog(self,
                                         message = "Choose an Application to open with",
                                         wildcard = wildcard,
                                         style=wx.OPEN | wx.CHANGE_DIR
                                         )
            if program_dialog.ShowModal() == wx.ID_OK:
                executable_path = program_dialog.GetPath()
                try: 
                    subprocess.call([executable_path, dest_file_path])
                    file_name = os.path.basename(dest_file_path)
                    responsive_status = self._rbx_responsive.GetStringSelection()
                    privileged_status = self._rbx_privileged.GetStringSelection()
                    self.make_tag_popup(file_name,responsive_status, privileged_status)
                except Exception,e:
                    self._show_error_message("File Open Error!", "Could not open the selected file with the Application.")
        except Exception,e:
            self.error(e)
            
    
    def on_popup_open_folder(self, event):
        '''
        Opens folder containing file
        '''
        try:
            dest_file_path = self.get_selection_file_name()
            
            selected_doc_folder = os.path.dirname(dest_file_path)
    
            try: 
                webbrowser.open_new(selected_doc_folder)
            except Exception,e:
                self._show_error_message("Folder Open Error!", "Please check that you have access to this folder")
        except Exception,e:
            self.error(e)
    
    def get_selection_file_name(self):
        '''
        Gets selected file path from review list control
        '''
        try:
            self.selected_doc_id = self._lc_review.GetFocusedItem()
    
            selected_doc_name = self._lc_review.GetItem(self.selected_doc_id, 1)
            src_file_path = self.sampled_files[self.selected_doc_id]
            dest_file_path = get_destination_file_path(self.dir_path,self._tempdir, src_file_path, self.output_dir_path)
            
            return dest_file_path
        except Exception,e:
            self.error(e)
     
    
    def get_default_fileviewer_path(self):
        '''
        Gets default fileviewer path. Additional File Viewers can be added
        to a dictionary here
        '''
        return self.DEFAULT_VIEWER_OPTIONS[DEFAULT_FILE_VIEWER]()
    
    def _on_click_io_clear(self,event):
        try:
            super(RandomSampler, self)._on_click_io_clear(event)
            self.clear()
        except Exception,e:
            self.error(e)
        
    def clear(self):
        try:
            if self._is_project_new==True:
                self._tc_io_new_project.SetValue("")
            else:
                self._cbx_project_title.SetSelection(-1)
            self._tc_data_dir.SetValue("")
            self._tc_output_dir.SetValue("")
            self.dir_path=""
            self.output_dir_path=""
            self.project_title=""
            self._st_num_data_dir_files.SetLabel('0 documents')
        except Exception,e:
            self.error(e)
            
    def _on_click_license(self,event):
        try:
            super(RandomSampler, self)._on_click_license(event)
            file_path="LICENSE.txt"
            with open(file_path,'r') as content:
                print_message=content.read()
            dialog=LicenseDialog(None)
            dialog._tc_license.SetValue(print_message)#wx.TextCtrl( self, wx.ID_ANY, print_message, wx.Point( -1,1 ), wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
            dialog.Show()
        except Exception,e:
            self.error(e)
    
    def _on_click_help(self,event):
        try:
            super(RandomSampler, self)._on_click_help(event)
            file_path="HELP.txt"
            with open(file_path,'r') as content:
                print_message=content.read()
            dialog=HelpDialog(None)
            dialog._tc_help.SetValue(print_message)#wx.TextCtrl( self, wx.ID_ANY, print_message, wx.Point( -1,1 ), wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
            dialog.Show()
        except Exception,e:
            self.error(e)
        
    def _on_click_io_sel_new_project(self,event):
        try:
            super(RandomSampler, self)._on_click_io_sel_new_project(event)
            self.clear()
            if self._chk_io_new_project.Value==True:
                self._st_new_project_title.Show(True)
                self._is_project_new=True
                self._tc_io_new_project.Enable()
                self._tc_io_new_project.SetValue("")
                self._cbx_project_title.Disable()
                self._cbx_project_title.SetSelection(-1)
            else:
                self._st_new_project_title.Show(False)
                self._is_project_new=False
                self._tc_io_new_project.Disable()
                self._tc_io_new_project.SetValue("Title of new project...")
                self._cbx_project_title.Enable()
        except Exception,e :
            self.error(e)
     
            
    def _update_project_new_name(self,event):
        try:
            super(RandomSampler, self)._update_project_new_name(event)
            self.project_title=self._tc_io_new_project.Value
        except Exception,e:
            self.error(e)

    def error(self,error):
        with open(os.path.join(os.path.expanduser('~'),"E-Discovery Random Sampler","error.log"),'a') as fl:
            date=unicode(datetime.now())
            fl.flush()
            fl.write(date+"=>")
            fl.write(unicode(error) + u'\n')
        

def main():
    '''
    The main function call 
    '''
    try:

        ex = wx.App()
        RandomSampler(None)
        
        #os.chdir(directory)
        ex.MainLoop()
    except Exception, e:
        with open(os.path.join(os.path.expanduser('~'),"E-Discovery Random Sampler","error.log"),'a') as fl:
            fl.write(unicode(e) + u'\n')

            
#            print >>fl, str(e)
    


if __name__ == '__main__':
    main()