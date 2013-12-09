'''
Created on Feb 23, 2013

@author: cgeorge
'''
import sys 
import wx 
import shelve
import os 
import math
import mimetypes
import wx.grid
import wx.animate
import numpy as np 
import shutil


from lucene import BooleanClause
from datetime import datetime
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin, \
    ColumnSorterMixin
from wx import grid
from gui.SMARTeRGUI import SMARTeRGUI, RatingControl, PreferencesDialog, NewProject
from lucenesearch.lucene_index_dir import boolean_search_lucene_index, MetadataType, get_indexed_file_details

import re
import webbrowser
from gui.HTML import Table, TableRow, TableCell, link
from const import NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS, \
    CHAR_LIMIT_IN_RESULTS_TAB_CELLS, SHELVE_CHUNK_SIZE, SHELVE_FILE_EXTENSION, \
    COLUMN_NUMBER_OF_RATING
from collections import OrderedDict
from utils.utils_file import read_config, load_file_paths_index, nexists
from tm.process_query import load_lda_variables, load_dictionary, get_dominant_query_topics
from index_data import index_data 
from decimal import Decimal
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from gui.TaggingControlSmarter import TaggingControlSmarter
from gui.TaggingControlFeedback import TaggingControlFeedback
import shutil
from fileinput import filename


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
resp_colors['Yes'] = 'blue'
resp_colors['No'] = 'orange'
resp_colors['NA'] = '#D8D8D8'

priv_colors = {}
priv_colors['Yes'] = '#F78181'
priv_colors['No'] = '#F3F781'
priv_colors['NA'] = '#D8D8D8'

row_colors = {}
row_colors['R'] = '#F8E0E6' 
row_colors['NA'] = '#D8D8D8'

###########################################################################
# # This global dictionary is used to keep track of the query-results 
dictionary_of_rows = OrderedDict()
APP_DIR=os.getcwd()
# Global variables to keep track of the chunk of results displayed
present_chunk = 0

# Constants 
SHELVE_DIR_NAME = 'shelf'
USER_RATINGS_CUT_OFF = 5  # TODO: this needs to be learned
CUT_OFF=0.01
CUT_OFF_NORM=0.3
TOP_K_TOPICS = 5
LIMIT_LUCENE=1000

REPORT_COMPLETE = 'complete_report.html'
REPORT_RESPONSIVE = 'responsiveness_docs_report.html' 
REPORT_PRIVILEGED = 'privileged_docs_report.html'

CONFIGURATION_FILE_EXT = '.cfg'



###########################################################################

###########################################################################
# # Class ResultsCheckListCtrl
###########################################################################

class ResultsCheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent_panel, parent_window,rbx_response):
        wx.ListCtrl.__init__(self, parent_panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        #CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_list_item_deselect)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_row_double_click)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_row_right_click)
        self._shelve_dir = ''
        self._parent_window = parent_window  
        self._rbx_res=rbx_response
        
    def _set_table_headers(self):
        
        self.ClearAll()
        #Remove this after Testing
        columnHeaders = ['File Name','File Path','File Score']# MetadataType._types
        columnNumber = 0
        #for c in columnHeaders:
        self.InsertColumn(columnNumber, columnHeaders[0])
        columnNumber = columnNumber + 1
        self.InsertColumn(columnNumber, "File Path")
        self.InsertColumn(columnNumber + 1, "File Score")
        
        
    
    def _set_shelve_dir(self, _dir_path):
        self._shelve_dir = _dir_path
    
    def _populate_results(self, chunk_number, doc_list):
        """ Given the 'chunk_number' 
            1. Reads from that particular shelved-file
            2. Updates the dictionary_of_rows with this chunk of results
            3. Sorts the dictionary_of_rows based on rating
            4. Change all keys in the dictionary to correspond to row_numbers in the UI
            5. Change all keys in the shelved-file to correspond to row_numbers in the UI
            6. Displays the content in the RESULT tab of the UI            
        """
        # The below section of commented lines were used when search results were 
        # being fetched from the global dictionary.  
        # They are now commented because search results are now loaded from shelved-files
        # for paging the results
        '''
        global dictionary_of_rows
        self.DeleteAllItems()
        self.Refresh()
        items = dictionary_of_rows.items() 
        for key, row in items:
        '''
        # Populate the column names using the metadata types from MetadataType_types &RB
        self._set_table_headers()
        
        i=chunk_number*6
        end=0
        if (chunk_number+1)*6>len(doc_list):
            end=len(doc_list)
        else:
            end=(chunk_number+1)*6
        
        while i<end:
            index = self.InsertStringItem(sys.maxint, doc_list[i][0])
            self.SetItemData(index, i)
            cell = str(doc_list[i][0])
            self.SetStringItem(index, 0, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
            cell = str(doc_list[i][1])
            self.SetStringItem(index, 1, cell)
            cell = str(doc_list[i][2])
            self.SetStringItem(index, 2, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
            #cell = str("")
            #self.SetStringItem(index, 3, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
            i= i+1
        
        # 1. Reads from that particular shelved-file
        '''
        shelve_file = shelve.open(os.path.join(self._shelve_dir, str(chunk_number) + SHELVE_FILE_EXTENSION))
        self.DeleteAllItems()
        global dictionary_of_rows
        dictionary_of_rows = OrderedDict()
        
        # print "Re-initialized dictionary = ", dictionary_of_rows
        for key in shelve_file.keys():
            row = shelve_file[key]
            # 2. Updates the dictionary_of_rows with this chunk of results
            dictionary_of_rows.__setitem__(key, row) 
        # print "Populated Dictionary from file: \n", dictionary_of_rows.keys()
        # print "Rows size = ", len( dictionary_of_rows.values()[0] )
        # 3. Sorts the dictionary_of_rows based on rating
        dictionary_sorted_as_list = sorted(dictionary_of_rows.items(), key=lambda (k, v): v[COLUMN_NUMBER_OF_RATING], reverse=True)
        keys = map(lambda (k, v): k, dictionary_sorted_as_list)
        values = map(lambda (k, v): v, dictionary_sorted_as_list)
        dictionary_of_rows = OrderedDict(zip(keys, values))

        # print "Sorted Dictionary: \n", dictionary_of_rows.keys()
        # print "Rows size = ", len( dictionary_of_rows.values()[3] )
        
        # 4. Change all keys in the dictionary to correspond to row_numbers in the UI
        k_in_String = dictionary_of_rows.keys()
        k_in_ints = map(int, k_in_String)
        k = sorted(k_in_ints)
        v = dictionary_of_rows.values()
        dictionary_of_rows = OrderedDict(zip(map(str, k), v))
           
        # 5. Change all keys in the shelved-file to correspond to row_numbers in the UI
        for key, row in dictionary_of_rows.items():
            shelve_file[key] = row
        shelve_file.close()
        
        
        # 6. Displays the content in the RESULT tab of the UI
        items = dictionary_of_rows.items()
        
        if responsive=="true":
            low=CUT_OFF
            high=1.1
        else:
            low=0
            high=CUT_OFF
         
        for key, row in items:
            #print row[10]
            #exit()
            if float(row[10])>=low and float(row[10])<high:
                index = self.InsertStringItem(sys.maxint, row[0])
                self.SetItemData(index, long(key))
                cell = str(row[0])
                self.SetStringItem(index, 0, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
                cell = str(row[1])
                self.SetStringItem(index, 1, cell)
                cell = str(row[10])
                self.SetStringItem(index, 2, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
                cell = str("")
                self.SetStringItem(index, 3, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
            i = 0
            for cell in row:
                j = 0
                if(i==0 | i==8 | i==9):
                    column_name = self.GetColumn(j).GetText()  
                    cell = str(cell)        
                    # Only the file_path is displayed completely.
                    # The content of all other cells are restricted to 30 characters.                 
                    if(column_name <> 'file_path') and len(cell) > CHAR_LIMIT_IN_RESULTS_TAB_CELLS:
                        self.SetStringItem(index, j, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
                    else:
                        self.SetStringItem(index, j, cell)
                    j+=1
                i+=1
               ''' 
        # self.Refresh()
    
    def _on_row_right_click(self, event):
        """Right-Clicking on a row to specify the search-relevancy of the file"""
        #Rating(None, self, self._shelve_dir)
         
    def _on_row_double_click(self, event):
        focussed_item_index = self.GetFocusedItem()
        file_Name = self.GetItem(focussed_item_index, 1)
        webbrowser.get().open(file_Name.GetText())
    
    def _on_list_item_select(self, event) :
        '''
        Handles the result list row select event 
        '''
        
        focussed_item_index = self.GetFocusedItem()
        print self.GetItemText(focussed_item_index,3)
        
        responsive=self.GetItemText(focussed_item_index,3)
        if responsive == 'Yes':
            self._rbx_res.SetSelection(0)
        elif responsive == 'No':
            self._rbx_res.SetSelection(1)
        else:
            self._rbx_res.SetSelection(2)
            
        
        file_name = self.GetItem(focussed_item_index, 1).GetText()
        _, file_ext = os.path.splitext(file_name)
        msg_text = 'Cannot open "%s" in this viewer! Please double click the row to open the file in a default system file viewer.' % file_name
        try: 
            if file_ext == '.txt' or file_ext == '': 
                import unicodedata
                with open(file_name) as fp:
                    msg_text = fp.read()
                    msg_text = unicodedata.normalize('NFKD', msg_text).encode('ascii', 'ignore')  # converts to ascii 

            else:
                file_type, _ = mimetypes.guess_type(file_name, strict=True)
                msg_text = 'Cannot open "%s (type:%s)" in this viewer! Please double click the row to open the file in a default system file viewer.' % (file_name, file_type)
        except:
            pass             
            
        self._parent_window._tc_file_preview_pane.SetValue(msg_text)
    
    def _on_list_item_deselect(self, event) :
        self._parent_window._tc_file_preview_pane.SetValue('')
    
    def GetListCtrl(self):
        return self
    
    def _on_header_column_click(self, event):
        """
        This method is used to sort the rows in the RESULTS ResultsCheckListCtrl
        """
        self._populate_results(present_chunk)
        


###########################################################################
# # Class Rating
###########################################################################

class Rating (RatingControl):
    selected_record_index = None
    checklist_control = None
    
    def __init__(self, parent, checklist_control, _shelve_dir):
        """ Calls the parent class's method """ 
        super(Rating, self).__init__(parent) 
        self.Center()
        self.Show(True)
        self.checklist_control = checklist_control
        self.selected_record_index = checklist_control.GetFocusedItem()
        
        # If the Relevance-recording window is opened again, it must show the score already given  
        relevance_score = checklist_control.GetItem(self.selected_record_index, COLUMN_NUMBER_OF_RATING)
        # self.radio_control.SetSelection( int(relevance_score.GetText()) )
        
        self._rating_slider.SetValue(int(relevance_score.GetText()))
        self._shelve_dir = _shelve_dir
    

    def _on_btn_click_submit(self, event):
        """
        1. Updates the Relevance column with the given rating
        2. Stores this new rating in the dictionary
        3. Stores this new rating in the shelved-file
        """

        # 1. Updates the Relevance column with the given rating
        # rating = self.radio_control.GetSelection()
        rating = self._rating_slider.GetValue()
        self.checklist_control.SetStringItem(self.selected_record_index, COLUMN_NUMBER_OF_RATING, str(rating))
        
        # Statements to just debug
        # print "Old rating = ", dictionary_of_rows[self.selected_record_index][-1]
        # print "New rating = ", rating
        
        selected_row_in_dict = present_chunk * SHELVE_CHUNK_SIZE + self.selected_record_index
        # 2. Stores this new rating in the dictionary
        dictionary_of_rows[str(selected_row_in_dict)][-1] = str(rating)

        shelve_file = shelve.open(os.path.join(self._shelve_dir, str(present_chunk) + SHELVE_FILE_EXTENSION))
        row = shelve_file[str(selected_row_in_dict)]
        # print "Before SUBMIT : ", shelve_file[str(selected_row_in_dict)]
        row[-1] = str(rating)
        shelve_file[str(selected_row_in_dict)] = row
        # print "changed : ", shelve_file[str(selected_row_in_dict)] 
        shelve_file.close()
        
        self.checklist_control.itemDataMap = dictionary_of_rows
        self.Destroy()
'''        
class CreateProject (NewProject):
    def __init__(self, parent):
        """ Calls the parent class's method """ 
        super(NewProject, self).__init__(parent)
        self.Center()
        self.Show(True)
'''
        
class CreateProjectPopup ( wx.Dialog ):
    smarter=None
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = (u"Create New Project"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        sbsizer_project = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY,(u"Project Details") ), wx.VERTICAL )
        
        gbsizer_project = wx.GridBagSizer( 0, 0 )
        gbsizer_project.SetFlexibleDirection( wx.BOTH )
        gbsizer_project.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self._tc_project_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )

        
        gbsizer_project.Add( self._tc_project_name, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, (u"Input Data Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        gbsizer_project.Add( self.m_staticText6, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self._data_dir_picker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, (u"Select the Input Data Folder"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE )
        gbsizer_project.Add( self._data_dir_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        gbsizer_project.Add( self.m_staticline3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
        
        self._btn_clear_project_details = wx.Button( self, wx.ID_ANY, (u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gbsizer_project.Add( self._btn_clear_project_details, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self._btn_index_data = wx.Button( self, wx.ID_ANY, (u"Create Project"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gbsizer_project.Add( self._btn_index_data, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, (u"Enter New Project Title"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        gbsizer_project.Add( self.m_staticText14, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        
        sbsizer_project.Add( gbsizer_project, 1, wx.EXPAND, 5 )
        
        
        bSizer5.Add( sbsizer_project, 0, wx.ALL, 10 )
        
        
        self.SetSizer( bSizer5 )
        self.Layout()
        bSizer5.Fit( self )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self._btn_clear_project_details.Bind( wx.EVT_BUTTON, self._on_click_cancel )
        self._btn_index_data.Bind( wx.EVT_BUTTON, self._on_click_index_data )
        
        self.smarter = parent
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def _on_click_cancel( self, event ):
        self.smarter.SetStatusText('Project creation is cancelled. Please select a project from the project drop down.')
        self.Destroy()
    
    def _on_click_index_data( self, event ):
        
        project_name = self._tc_project_name.GetValue().strip()
        data_folder = self._data_dir_picker.GetPath().strip()
        
        if project_name == '' or not os.path.exists(data_folder):
            self.smarter._show_error_message("Missing Project Details!", "Please enter the required project specifications.")
            return 
        if project_name in self.smarter._cbx_project_title.GetStrings():
            self.smarter._show_error_message("Duplicate Project!", "Project name already exists! Enter a different project name.")
            self._tc_project_name.SetValue("")
        else:
            msg_dialog=LoadDialog(None,-1)
            msg_dialog.Show()
            msg_dialog.Update()
            tmp_files=os.path.join(self.smarter._SMARTeR_dir_path,project_name,"files")
            if os.path.exists(tmp_files)==True:
                shutil.rmtree(tmp_files)
            shutil.copytree(data_folder,tmp_files)
            
            for root, _ , files in os.walk(tmp_files):
                for file_name in files:
                    name, ext = os.path.splitext(file_name)
                    if ext == ".pst":
                        pstTemp=os.path.join(root,os.path.basename(name))
                        if os.path.exists(pstTemp)==False:
                            os.mkdir(pstTemp)
                        
                        shutil.copy(os.path.join(root,file_name), os.path.abspath(pstTemp))
                        temp=os.path.basename(file_name)
                        pstTempFile=os.path.join(pstTemp,temp)
                        # print pstTempFile
                        try:
                            self.convert_pst(pstTempFile, pstTemp)
                        except Exception,e:
                            print e
                        # print os.path.join(root,file_name)
                        os.remove(os.path.join(root,file_name))
            
            # print tmp_files
            
            index_data(tmp_files, self.smarter._SMARTeR_dir_path, 
                       project_name, self.smarter._cfg_dir_path, 
                       self.smarter._num_topics, self.smarter._num_passes, 
                       self.smarter._min_token_freq, self.smarter._min_token_len, 
                       log_to_file = True, lemmatize=True, stem=True, nonascii=True)
            
            self.smarter._cbx_project_title.Append(project_name)        
            self.smarter.SetStatusText('The project %s indexing is completed. Please select a project from the project drop down.' % project_name)
            msg_dialog.Destroy()
            self.Destroy()
    
    def convert_pst(self, pstfilename,temp):
        '''
        This method will be a little creative 
        '''        
        #ToDo....NOT SAFE
        import subprocess
        subprocess.check_output(['readpst', '-o', os.path.abspath(temp), '-e', '-b', '-S', pstfilename], stderr=subprocess.STDOUT,shell=True)

        #print response
        for root, _, files in os.walk(temp):
            for file_name in files:
                filename=os.path.join(root, file_name)
                _, fileExtension = os.path.splitext(filename)
                if fileExtension!="":
                    os.remove(filename)
            
    

            
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
        
        
        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"Indexing the files. Please wait...", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )
        gbSizer.Add( self.m_staticText24, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        #self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Note: 1000000 documents approximately take 10 minutes to count\n(The time may vary depending on the system configuration)", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.m_staticText25.Wrap( -1 )
        #self.m_staticText25.SetFont( wx.Font( 7, 74, 93, 90, False, "Tahoma" ) )
        
       # gbSizer.Add( self.m_staticText25, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        
        
        self.SetSizer( gbSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
            
        

###########################################################################
# # Class Preferences 
###########################################################################

class Preferences (PreferencesDialog):
    
    def __init__(self, parent):
        '''
        Calls the parent class's method 
        '''
        super(Preferences, self).__init__(parent) 
        
        self._parent = parent  # refers to the parent object    
        self._load_existing_indexing_preferences()
        
        self.Center()
        self.Show(True)
        
     
    def _load_existing_indexing_preferences(self):
        '''
        Loads and sets the existing preferences from the 
        the main class -- SMARTeR  

        Arguments: 
            parent - the main class reference 
        '''

        self._tc_num_topics.SetValue(str(self._parent._num_topics))
        self._tc_num_passes.SetValue(str(self._parent._num_passes))
        self._tc_min_token_freq.SetValue(str(self._parent._min_token_freq))
        self._tc_min_token_len.SetValue(str(self._parent._min_token_len))


    def _on_click_reset_defaults_indexing_preferences(self, event):
        '''
        Resets the indexing preferences to the default values 
        
        '''
        
        self._load_existing_indexing_preferences()
        
        
    def _on_click_save_indexing_preferences(self, event):
        '''
        Saves the indexing preferences to the class variables 
        
        TODO: 
            1. Need to save all these variables into the persistent storage 
            2. Need to handle validations such as clicking another tab, negative values, etc. 
        '''
                
        self._parent._num_topics = int(self._tc_num_topics.GetValue().strip())
        self._parent._num_passes = int(self._tc_num_passes.GetValue().strip())
        self._parent._min_token_freq = int(self._tc_min_token_freq.GetValue().strip())
        self._parent._min_token_len = int(self._tc_min_token_len.GetValue().strip()) 
        
        # destroys the pop up 
        self.Destroy()




###########################################################################
# # Class SMARTeR
###########################################################################

class SMARTeR (SMARTeRGUI):
    
    #---------------------------------------------------- Class specific methods

    def __init__(self, parent):
        
        # Calls the parent class's method 
        super(SMARTeR, self).__init__(parent)
        self.SEED = 2013  
        self._is_lucene_index_available = False 
        self._is_tm_index_available = False
        self._current_page = 0
        
        self.NOTREVIEWED_CLASS_ID = -99
        self.NEUTRAL_CLASS_ID = 0
        self.RESPONSIVE_CLASS_ID = 1
        self.UNRESPONSIVE_CLASS_ID = -1
        self.RELEVANCY_COLOR_HEX = {'not_reviewed':'#C8C8C8', 'uncertain':'#00FF33', 'relevant':'#0066CC', 'irrelevant':'#FF6600'}  
        self._doc_true_class_ids = {} # this keeps documents' TRUE classes (from user feedback or from a TRUTH file)
        self._shelve_dir = ''
        self._shelve_file_names = []  # this keeps all of the shelf files path 
        self._responsive_files = []
        self._unresponsive_files = []
        self._responsive_files_display = []
        self._unresponsive_files_display = []
        self._build_query_results_panel()
        self.__populate_metadata_fields()
        self.__default_indexing_preferences()
        
        self._query_history = []    
        self._choose_history = False
        self._choice_history = -1
        
        self._lda_num_topics = self._num_topics
        self._init_search_results = []
        
        #--------- Creates the SMARTeR directory at in the default home directory
        
        from os.path import expanduser
        default_user_home = expanduser("~")
        self._SMARTeR_dir_path = os.path.join(default_user_home, "SMARTeR")
        if not os.path.exists(self._SMARTeR_dir_path):
            os.makedirs(self._SMARTeR_dir_path)
            
        #--------------------- Creates the project configuration files directory
        
        self._cfg_dir_path = os.path.join(self._SMARTeR_dir_path, "repository")
        if not os.path.exists(self._cfg_dir_path):
            os.makedirs(self._cfg_dir_path)
            
            
        #--------- Loads all project names existing in the SMARTeR folder to GUI
            
        for _, _, files in os.walk(self._cfg_dir_path):
            for project_file_name in files:
                project_name, _ = os.path.splitext(project_file_name)
                self._cbx_project_title.Append(project_name)
        
        self._load_cbx_confidence_levels()
        self._init_confidence()
        self._notebook.ChangeSelection(0)
        self.Center()
        self.Show(True)
        
    def _get_relevancy_color(self, is_relevant):
        if is_relevant == 'Yes': return self.RELEVANCY_COLOR_HEX['relevant']
        elif is_relevant == 'No': return self.RELEVANCY_COLOR_HEX['irrelevant']
        elif is_relevant == 'Uncertain': return self.RELEVANCY_COLOR_HEX['uncertain']
        else: return self.RELEVANCY_COLOR_HEX['not_reviewed']
        
    def _get_irrelevancy_color(self, is_rrrelevant):
        if is_rrrelevant == 'Yes': return self.RELEVANCY_COLOR_HEX['irrelevant']
        elif is_rrrelevant == 'No': return self.RELEVANCY_COLOR_HEX['relevant']
        elif is_rrrelevant == 'Uncertain': return self.RELEVANCY_COLOR_HEX['uncertain']
        else: return self.RELEVANCY_COLOR_HEX['not_reviewed']
    
    def __default_indexing_preferences(self):
        
        self._num_topics = 30
        self._num_passes = 99
        self._min_token_freq = 1 
        self._min_token_len = 2
        

    def __populate_metadata_fields(self):
        '''
        This function will populate the metadata combo box 
        dynamically at the time of file loading. This will help
        to accommodate new metadata types as and when they are needed. 
        '''
        meta_data_types = MetadataType._types
        self._cbx_query_data_fields.Append(MetadataType.ALL) # adds the all field to the combo box
        for l in meta_data_types :
            self._cbx_query_data_fields.Append(l) 
        self._cbx_query_data_fields.SetSelection(0)

    def _on_notebook_page_changed(self, event):
        '''
        Handles the note book page change event 
        '''
        
        self._current_page = event.Selection
        self._notebook.ChangeSelection(self._current_page)


    def __on_close(self):
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
                
#                # Handles the shelf 
#                if self.shelf is not None:
#                    if self._is_rt_updated:
#                        self._shelf_update_review_tab_state()
#                    self.shelf.close()
                
                self.Destroy()
        except Exception,e:
            print e


    def _show_error_message(self, _header, _message):
        '''
        Shows error messages in a pop up 
        '''
        
        dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
    


    #------------------------------------------------------------ Menu functions
        
    def _on_menu_sel_preferences(self, event):
        '''
        Display's application preferences popup 
        '''
        Preferences(parent=self)
        
    def _on_menu_sel_exit(self, event):

        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()   
            

    #--------------------------------------------------------------- Project tab
    
#    def _on_click_io_sel_new_project(self,event):
#        
#        super(SMARTeR, self)._on_click_io_sel_new_project(event)
#       
#        if self._chk_io_new_project.Value==True:
#            self._tc_project_name.Show(True)
#            self._tc_project_name.Enable()
#            self._tc_project_name.SetValue("")
#            self._cbx_project_title.Disable()
#            self._cbx_project_title.SetSelection(-1)
#        else:
#            #self._tc_project_name.Show(False)
#            self._tc_project_name.Disable()
#            self._tc_project_name.SetValue("Title of new project...")
#            self._cbx_project_title.Enable()
#            self._cbx_project_title.SetSelection(0)
            
    def _on_click_index_new_project(self, event):
        
        SMARTeRGUI._on_click_index_new_project(self, event)
        self.__clear_project_details()
        msg_dlg = CreateProjectPopup(self)
        msg_dlg.Show()
    
#    def _on_file_change_mdl(self, event):
#        '''
#        Handles the model file change event  
#        '''
#        
#        file_name = self._file_picker_mdl.GetPath()
#        self.project_name = file_name
#        self.__load_model(file_name)
#
#        if self._is_tm_index_available or self._is_lucene_index_available:
#            self.SetStatusText("The %s model is loaded." % self.mdl_cfg['DATA']['name'])
#        else: 
#            self._show_error_message("Model Error", "Please select a valid model.")
#            self._file_picker_mdl.SetPath("")
#            self.mdl_cfg = None 
                    
    def __load_model(self, model_cfg_file):
        '''
        Loads the models specified in the model configuration file  
        
        Arguments: 
            model_cfg_file - the model configuration file  
        
        '''
        
        print 'Project configuration file:', model_cfg_file
        
        self.mdl_cfg = read_config(model_cfg_file)
        self._tc_data_fld.SetValue(self.mdl_cfg['DATA']['root_dir'])
        
        self._shelve_dir = os.path.join(self.mdl_cfg['DATA']['project_dir'], SHELVE_DIR_NAME)
        if not os.path.exists(self._shelve_dir): 
            os.makedirs(self._shelve_dir)
        print 'Project shelf directory:', self._shelve_dir
        
        
        self.data_dir_name = self.mdl_cfg['DATA']['root_dir']
        
        # Retrieve topic model file names 
        
        dictionary_file = self.mdl_cfg['CORPUS']['dict_file']
        path_index_file = self.mdl_cfg['CORPUS']['path_index_file']
        lda_mdl_file = self.mdl_cfg['LDA']['lda_model_file']
        lda_cos_index_file = self.mdl_cfg['LDA']['lda_cos_index_file']
        lda_num_topics = self.mdl_cfg['LDA']['num_topics']
        lda_theta_file = self.mdl_cfg['LDA']['lda_theta_file']
#        lsi_mdl_file = self.mdl_cfg['LSI']['lsi_model_file']
#        lsi_cos_index_file = self.mdl_cfg['LSI']['lsi_cos_index_file']
        

        # Loads learned topic models and file details 
        if nexists(dictionary_file) and nexists(path_index_file):
                
            self.lda_file_path_index = load_file_paths_index(path_index_file)
            self.lda_dictionary = load_dictionary(dictionary_file)
            self._num_documents = len(self.lda_file_path_index)
            self._vocabulary_size = len(self.lda_dictionary)        
            
            # Loads documents' TRUE classes
            # TODO: hard coding for the TRUTH data. This needs to be removed from the final version 
            if os.path.exists(os.path.join(self.data_dir_name, "1")):
                positive_dir = os.path.normpath(os.path.join(self.data_dir_name, "1")) # TRUE positive documents  
                for doc_id, dirname, _ in self.lda_file_path_index:
                    if dirname == positive_dir:
                        self._doc_true_class_ids[doc_id] = self.RESPONSIVE_CLASS_ID 
                    else: 
                        self._doc_true_class_ids[doc_id] = self.UNRESPONSIVE_CLASS_ID
            else: 
                for doc_id, dirname, _ in self.lda_file_path_index:
                    self._doc_true_class_ids[doc_id] = ''
            
            
            # loads LDA model details 
            if nexists(lda_mdl_file) and nexists(lda_cos_index_file): 
                self.lda_mdl, self.lda_index = load_lda_variables(lda_mdl_file, lda_cos_index_file)
                self._lda_num_topics = int(lda_num_topics)
                self._is_tm_index_available = True 
                self._lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble) # loads the LDA theta from the model theta file 
                print 'LDA: number of documents: ', self._num_documents, ' number of topics: ', self._lda_num_topics  
                    
#            # loads LSI model details 
#            if nexists(lsi_mdl_file) and nexists(lsi_cos_index_file):
#                self.lsi_mdl, self.lsi_index = load_lsi_variables(lsi_mdl_file, lsi_cos_index_file)
#                self._is_tm_index_available = True  
#                self._tc_available_mdl.AppendText('[LSI] ')    
                                   

        # Loads Lucene index files 
        lucene_dir = self.mdl_cfg['LUCENE']['lucene_index_dir']
        
        if nexists(lucene_dir):
            self.lucene_index_dir = lucene_dir
            self._is_lucene_index_available = True  

    def __clear_project_details(self):
        '''
        Clears the loaded project details
        
        TODO: this should clear all the project related 
        objects in this class 
        '''
        self._cbx_project_title.SetSelection(-1)
        self._tc_data_fld.SetValue('')
        self.mdl_cfg = None
        self._project_dir_path = ''
        self._project_cfg_file_path = ''
        self._is_tm_index_available = False
        self._is_lucene_index_available = False
        self.SetStatusText('All project details are cleared.')
             
    def _on_click_index_go_to_search(self, event):
        '''
        Handles "Go to Search" button click events 

        '''
        if self._cbx_project_title.GetCurrentSelection() == -1:
            self._show_error_message("Missing input", "Please select a project or create a new project.")
        else:
            if self._is_tm_index_available and self._is_lucene_index_available:
                self._seed_docs_details = self.__seed_docs_Kmeans_selection()
                self.__load_document_feedback()
                self._current_page = 1
                self._notebook.ChangeSelection(self._current_page)
                self.SetStatusText('')
            else: 
                self._show_error_message("Project Error", "Please select a valid project.")
                self.__clear_project_details()
                
                
    def _on_set_index_existing_project(self, event):
        
        if self._cbx_project_title.GetCurrentSelection() == -1:
            self.__clear_project_details()
            return 
        
        project_name = self._cbx_project_title.GetValue().strip()
        
        self._project_dir_path = os.path.join(self._SMARTeR_dir_path, project_name)
        self._project_cfg_file_path = os.path.join(self._cfg_dir_path, project_name + CONFIGURATION_FILE_EXT)
        self.__load_model(self._project_cfg_file_path)
        
        self.SetStatusText("The project %s index is loaded." % self.mdl_cfg['DATA']['name'])



    #--------------------------------------------- Query preliminary results tab

    def _build_query_results_panel(self):
        '''
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        _panel_left = wx.Panel(self._panel_query_results, -1)
        _panel_right = wx.Panel(self._panel_query_results, -1)

        self._st_file_preview_header = wx.StaticText(_panel_right, -1, 'File Review Pane (Text Files)')
        self._tc_file_preview_pane = wx.TextCtrl(_panel_right, -1, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 200))
        '''
        self._lc_results_res = ResultsCheckListCtrl(self._panel_res, self, self._rbx_feedack_res)
        self._lc_results_res._set_table_headers()  # Populate the column names using the metadata types from MetadataType_types &RB
        
        self._lc_results_unres = ResultsCheckListCtrl(self._panel_unres, self,self._rbx_feedack_unres)
        self._lc_results_unres._set_table_headers()  # Populate the column names using the metadata types from MetadataType_types &RB
        '''
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self._st_responsive_doc = wx.StaticText(_panel_right, -1, 'Responsive Files')
        self._st_unresponsive_doc = wx.StaticText(_panel_right, -1, 'Unresponsive Files')
        
        vbox_res = wx.BoxSizer(wx.VERTICAL)
        vbox_unres = wx.BoxSizer(wx.VERTICAL)

        self._btn_sel_all = wx.Button(_panel_left, -1, 'Select All', size=(100, -1))
        self._btn_desel_all = wx.Button(_panel_left, -1, 'Deselect All', size=(100, -1))
        self._btn_log_files = wx.Button(_panel_left, -1, 'Log', size=(100, -1))
        self._btn_load_next_chunk = wx.Button(_panel_left, -1, 'Next >', size=(100, -1))
        self._btn_load_previous_chunk = wx.Button(_panel_left, -1, '< Previous', size=(100, -1))
        self._btn_update_results = wx.Button(_panel_left, -1, 'Update Results', size=(100, -1))
        self._btn_continue = wx.Button(_panel_left, -1, 'Continue', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self._on_click_sel_all, id=self._btn_sel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_desel_all, id=self._btn_desel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_log_files, id=self._btn_log_files.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_next, id=self._btn_load_next_chunk.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_previous, id=self._btn_load_previous_chunk.GetId())        
        self.Bind(wx.EVT_BUTTON, self._on_click_update_results, id=self._btn_update_results.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_continue, id=self._btn_continue.GetId())  

        vbox2.Add(self._btn_sel_all, 0, wx.TOP, 5)
        vbox2.Add(self._btn_desel_all)
        vbox2.Add(self._btn_log_files)
        vbox2.Add(self._btn_load_next_chunk);
        vbox2.Add(self._btn_load_previous_chunk);
        vbox2.Add(self._btn_update_results);
        vbox2.Add(self._btn_continue);
        
        _panel_left.SetSizer(vbox2)
        vbox_res.Add(self._st_responsive_doc)
        vbox_res.Add(self._lc_results_res, 1, wx.EXPAND, 5)
        vbox_unres.Add(self._st_unresponsive_doc)
        vbox_unres.Add(self._lc_results_unres, 0, wx.EXPAND, 5)
        hbox2.Add(vbox_res)
        hbox2.Add((50, -1))
        hbox2.Add(vbox_unres)
        #hbox2.Add(self._lc_results_unres, 0.5, wx.EXPAND, 5)
        vbox.Add(hbox2)
        vbox.Add((-1, 10))
        vbox.Add(self._st_file_preview_header, 0.5, wx.EXPAND)
        vbox.Add((-1, 5))
        vbox.Add(self._tc_file_preview_pane, 0.5, wx.EXPAND)
        vbox.Add((-1, 10))
        #vbox.Add(vbox_unres)

        _panel_right.SetSizer(vbox)

        hbox.Add(_panel_left, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(_panel_right, 1, wx.EXPAND)
        hbox.Add((3, -1))

        self._panel_query_results.SetSizer(hbox)
        '''

    def _create_persistent_shelves(self, items):
        """
            Stores the query-results into shelves. 
            *** Currently, the shelved files are named chunkNumber.shelve ***
            *** Come up with a logic to name files so that they represent 
                the query string
            ***
        """
        self._shelve_file_names = []
        chunk_number = -1;
        shelve_file = None
        for key, row in items:
            if(int(key) % SHELVE_CHUNK_SIZE == 0):
                chunk_number = chunk_number + 1 
                fileName = str(chunk_number)
                fileName = os.path.join(self._shelve_dir, fileName + SHELVE_FILE_EXTENSION)
                self._shelve_file_names.append(fileName)
                if shelve_file is not None: 
                    shelve_file.close()
                shelve_file = shelve.open(fileName)
            shelve_file[str(key)] = row;
        global num_of_chunks
        num_of_chunks = chunk_number + 1
        shelve_file.close()
        
    def _reset_persistent_shelves(self):
        '''
        Removes all existing shelves 
        '''
        for file_name in self._shelve_file_names:
            os.remove(file_name) 
        global num_of_chunks
        num_of_chunks = 0

    def _on_click_next(self, event):
        global present_chunk
        current_chunk = present_chunk;
        
        if(current_chunk <> num_of_chunks - 1): 
            current_chunk += 1
            self._lc_results_res._populate_results(current_chunk,"true")
            self._lc_results_unres._populate_results(current_chunk,"false")
            present_chunk = current_chunk
     
    def _on_click_next_res(self, event):
        global present_chunk_res
        current_chunk = present_chunk_res;
           
                        
        if(current_chunk+1 < math.ceil(float(len(self._responsive_files))/6) ): 
            current_chunk += 1
            self._st_Resp_documents.SetLabel(u'Responsive Documents ('+str(current_chunk + 1)+'/'+str(int(math.ceil(float(len(self._responsive_files))/6)))+')')
            self._lc_results_res._populate_results(current_chunk,self._responsive_files_display)
            present_chunk_res = current_chunk
            
    def _on_click_next_unres(self, event):
        global present_chunk_unres
        
        current_chunk = present_chunk_unres;
        
        if(current_chunk+1 < math.ceil(float(len(self._unresponsive_files))/6)):
            
            current_chunk += 1
            self._st_unresp_documents.SetLabel(u'Unresponsive Documents ('+str(current_chunk + 1)+'/'+str(int(math.ceil(float(len(self._unresponsive_files))/6)))+')')
            self._lc_results_unres._populate_results(current_chunk,self._unresponsive_files_display)
            present_chunk_unres = current_chunk
            
    
    def _on_click_previous(self, event):
        global present_chunk
        current_chunk = present_chunk;
        current_chunk -= 1
        if(current_chunk >= 0): 
            
            self._lc_results_res._populate_results(current_chunk,"true")
            self._lc_results_unres._populate_results(current_chunk,"false")
            present_chunk = current_chunk
                
    def _on_click_previous_res(self, event):
        global present_chunk_res
        current_chunk = present_chunk_res;
        current_chunk -= 1
        if(current_chunk >= 0):
            self._st_Resp_documents.SetLabel(u'Responsive Documents ('+str(current_chunk + 1)+'/'+str(int(math.ceil(float(len(self._responsive_files))/6)))+')') 
            self._lc_results_res._populate_results(current_chunk,self._responsive_files_display)
            present_chunk_res = current_chunk
            
    def _on_click_previous_unres(self, event):
        global present_chunk_unres
        current_chunk = present_chunk_unres;
        current_chunk -= 1
        if(current_chunk >= 0): 
            self._st_unresp_documents.SetLabel(u'Unresponsive Documents ('+str(current_chunk + 1)+'/'+str(int(math.ceil(float(len(self._unresponsive_files))/6)))+')')
            self._lc_results_unres._populate_results(current_chunk,self._unresponsive_files_display)
            present_chunk_unres = current_chunk
            
    def _on_click_sel_all(self, event):
        num = self._lc_results_res.GetItemCount()
        for i in range(num):
            self._lc_results_res.CheckItem(i)
            
        num = self._lc_results_unres.GetItemCount()
        for i in range(num):
            self._lc_results_unres.CheckItem(i)

    def _on_click_desel_all(self, event):
        num = self._lc_results_res.GetItemCount()
        for i in range(num):
            self._lc_results_res.CheckItem(i, False)
            
        num = self._lc_results_unres.GetItemCount()
        for i in range(num):
            self._lc_results_unres.CheckItem(i, False)

#    def _on_click_log_files(self, event):
#        num = self._lc_results_res.GetItemCount()
#        for i in range(num):
#            if i == 0: self._tc_files_log.Clear()
#            if self._lc_results_res.IsChecked(i):
#                self._tc_files_log.AppendText(self._lc_results_res.GetItemText(i) + '\n')
#        pass 
    


    #---------------------------------------------------------- Start Search tab
    
    def _on_click_search_query_history(self,event):
        
        selection = self._list_query_history.GetSelection()
        self._tc_query_aggregated.SetValue(self._query_history[selection][0])
        
    
    def __lucene_append_nonresponsive_docs(self, docs):
        '''
        Appends the documents that are not retrieved via Lucene 
        search along with a default score 
        
        '''
        
        lucene_score_dict = {}
        score_list = []
        
        for doc in docs:
            lucene_score_dict[int(doc[9])] = doc[10]
            score_list.append(doc[10])
        
        if len(score_list) > 0:
            min_score = min(score_list) * 0.1 # default minimum 
        else:
            min_score = 1e-10 
        
        for doc_id, _, _ in self.lda_file_path_index:
            if int(doc_id) not in lucene_score_dict.keys():
                lucene_score_dict[int(doc_id)] = min_score
                    
        return lucene_score_dict
    
     
    
    def __search_tm_topics(self, topics_list, limit, mdl_cfg):   
        '''
        Performs search on the topic model using relevant  
        topic indices 
        
        Return:
            a list of [doc_id, doc_path, doc_name, doc_score]
        
        '''
        # import numpy as np
        EPS = 1e-24 # a constant 
        # lda_theta_file = mdl_cfg['LDA']['lda_theta_file']
        # lda_theta = np.loadtxt(lda_theta_file, dtype=np.longdouble) # loads the LDA theta from the model theta file 
        # num_docs, num_topics = lda_theta.shape
        

        
        unsel_topic_idx = [idx for idx in range(0, self._lda_num_topics) if idx not in topics_list]
        sel = np.log(self._lda_theta[:, topics_list] + EPS)
        unsel = np.log(1.0 - self._lda_theta[:, unsel_topic_idx] + EPS)
        ln_score = sel.sum(axis=1) + unsel.sum(axis=1)  
        sorted_idx = ln_score.argsort(axis=0)[::-1]
        # score = np.exp(ln_score)
        
        # Normalize the topic index search score 
        # TODO: this is an adhoc method right now. May come back later... 
        min_ln_score = min(ln_score)
        n_ln_score = (1.0 - ln_score / min_ln_score)
    
        ts_results = []
        for i in range(0, min(limit, self._num_documents)):
            ts_results.append([self.lda_file_path_index[sorted_idx[i]][0], # document id  
                              os.path.normpath(os.path.join(self.lda_file_path_index[sorted_idx[i]][1], self.lda_file_path_index[sorted_idx[i]][2])), # document path   
                              self.lda_file_path_index[sorted_idx[i]][2], # document name
                              n_ln_score[sorted_idx[i]]]) # similarity score 
            # print lda_file_path_index[sorted_idx[i]], ln_score[sorted_idx[i]], n_ln_score[sorted_idx[i]], score[sorted_idx[i]] 
            
    
        # grabs the files details from the index     
        # ts_results = get_indexed_file_details(ts_results, self.lucene_index_dir) 
        # results = [[row[0], int(row[9]), float(row[10])] for row in ts_results] # Note: we need a float conversion because it's retrieving as string 
        
        return ts_results # [doc_id, doc_path, doc_name, doc_score]
    
    
    def __fuse_lucene_tm_scores(self, lucene_score_dict, results_tm):
        '''
        This method fuse document relevancy scores from 
        Lucene with topic modeling based ranking scores. 
        Currently, it's based on Geometric mean of both 
        scores. 

        '''
        
        lucene_tm_results = []
        for doc_details in results_tm:            
            [doc_id, dir_path, doc_name, doc_score] = doc_details 
            lucene_score = lucene_score_dict[doc_id]
            mult_score = lucene_score * doc_score
            lucene_tm_results.append([doc_id, dir_path, doc_name, mult_score])
    
        #lucene_tm_results = sorted(lucene_tm_results, key=lambda student: student[1])
        
        return lucene_tm_results
    
    def __is_relevant(self, class_id):
        if class_id == self.RESPONSIVE_CLASS_ID: return 'Yes'
        elif class_id == self.UNRESPONSIVE_CLASS_ID: return 'No'
        elif class_id == self.NEUTRAL_CLASS_ID: return 'Uncertain' # Neutral 
        else: return '' # Not reviewed 
    
    def __is_irrelevant(self, class_id):
        if class_id == self.RESPONSIVE_CLASS_ID: return 'No'
        elif class_id == self.UNRESPONSIVE_CLASS_ID: return 'Yes'
        elif class_id == self.NEUTRAL_CLASS_ID: return 'Uncertain' # Neutral 
        else: return '' # Not reviewed 
    
    def __convert_is_relevant_to_id(self, feedback_label):
        if feedback_label == 'Yes': return self.RESPONSIVE_CLASS_ID
        elif feedback_label == 'No': return self.UNRESPONSIVE_CLASS_ID
        elif  feedback_label == 'Uncertain': return self.NEUTRAL_CLASS_ID  
        else: return self.NOTREVIEWED_CLASS_ID # Not reviewed 
        
    def __convert_is_irrelevant_to_id(self, feedback_label):
        if feedback_label == 'Yes': return self.UNRESPONSIVE_CLASS_ID
        elif feedback_label == 'No': return self.RESPONSIVE_CLASS_ID
        elif  feedback_label == 'Uncertain': return self.NEUTRAL_CLASS_ID  
        else: return self.NOTREVIEWED_CLASS_ID # Not reviewed 
    
    def _on_text_search_query_terms(self, event):
        if self._tc_query_aggregated.GetValue().strip() <> '':
            self._cbx_query_conjunctions.Enable()
    
    def _on_click_search_add_to_query(self, event):
        
        metadataSelected = self._cbx_query_data_fields.GetValue()
        operatorSelected = self._cbx_query_conjunctions.GetValue()
        queryBoxText = '(' + self._tc_query_terms.GetValue() + ')'

        if(self._tc_query_aggregated.GetValue() == ""):   
            self._tc_query_aggregated.AppendText(metadataSelected + ":" + queryBoxText)
        else:
            self._tc_query_aggregated.AppendText("\n" + operatorSelected + "\n" )
            self._tc_query_aggregated.AppendText(metadataSelected + ":" + queryBoxText)
            
        self._tc_query_terms.SetValue('')
        self._cbx_query_conjunctions.Enable()
    
    
    def __seed_docs_topK_selection(self, num_seed_docs=100):
        '''
        Selecting seed documents from the initial ranking results
        TODO: the seed document selection should improved, e.g., use 
        a representative sample of all the clusters found in the 
        documents (based on k-Means clustering on ranking scores)
        '''
        
        seed_docs_details = []
        for i, doc_details in enumerate(self._init_search_results):
            doc_id, doc_path, doc_name, _ = doc_details
            seed_docs_details.append([doc_id, doc_path, doc_name, self.__is_relevant(self._doc_true_class_ids[doc_id])])
            if i+1 == 100: break
        
        return seed_docs_details
    
    def __seed_docs_random_selection(self, num_seed_docs=100):
        '''
        Selecting seed documents randomly from the initial ranking results
        '''
       
        import random
        indices = range(0, self._num_documents)
        random.shuffle(indices)
        selected_random_indices = indices[1:num_seed_docs]
 
        seed_docs_details = []
        for random_index in selected_random_indices:
                doc_id, dir_path, doc_name = self.lda_file_path_index[random_index]
                doc_path = os.path.normpath(os.path.join(dir_path, doc_name))
                seed_docs_details.append([doc_id, doc_path, doc_name, self.__is_relevant(self._doc_true_class_ids[doc_id])])
       
        return seed_docs_details
    

    def __seed_docs_Kmeans_selection(self, num_seed_docs=100, num_clusters=5):
        '''
        Selecting seed documents from K-means clusters of LDA 
        document topic proportions (theta_d) 
        '''
        import random 
        
        from collections import Counter, defaultdict

        def __get_seed_doc_details(doc_id):
            
            is_resp = self.__is_relevant(self._doc_true_class_ids[doc_id])
            doc_id, dir_path, doc_name = self.lda_file_path_index[doc_id]
            doc_path = os.path.normpath(os.path.join(dir_path, doc_name))
            
            # print doc_id, doc_name, is_resp
            return [doc_id, doc_path, doc_name, is_resp]

        
        seed_docs_details = []
        desired_class_count = int(num_seed_docs / num_clusters)
        
        # K-means clustering on the LDA theta 
#        from scipy.cluster.vq import kmeans2
#        _, doc_labels = kmeans2(data=self._lda_theta + 1e-8, k=num_clusters, minit='random')
        
        if np.isnan(np.min(self._lda_theta)):
            print "Cannot perform k-means because one of the elements of the document THETA matrix is NAN."
            exit()
             
        print 'k-Means clustering'
        from scipy.cluster.vq import kmeans, vq, whiten
        whitened = whiten(self._lda_theta + 1e-15)
        codebook, _ = kmeans(whitened, num_clusters)
        doc_labels, _ = vq(whitened, codebook)
        

#        import Pycluster
#        doc_labels, error, nfound = Pycluster.kcluster(self._lda_theta, num_clusters)
#        print error # The within-cluster sum of distances for the optimal clustering solution.
#        print nfound # The number of times the optimal solution was found.
        
        
        
#        exec_count = 0
#        while True:
#            try:
#                exec_count += 1
#                _, doc_labels = kmeans2(data=self._lda_theta, k=num_clusters, minit='random')
#                break # while loop break when success 
#            except Exception as exp:
#                print exec_count, exp 
        
        # Gets class elements' document id 
        class_docs_id = defaultdict(list)
        for doc_id, doc_label in enumerate(doc_labels):
            class_docs_id[doc_label] += [doc_id] 
        

        for class_id, class_count in Counter(doc_labels).items(): # gets class_id and counts 
            
            if class_count <= desired_class_count:
                for doc_id in class_docs_id[class_id]:
                    # print class_id, 
                    seed_docs_details.append(__get_seed_doc_details(doc_id))
            else: 
                indices = range(0, class_count)
                random.shuffle(indices)
                selected_class_indices = [class_docs_id[class_id][i] for i in indices[1:desired_class_count]]
                for doc_id in selected_class_indices:
                    # print class_id, 
                    seed_docs_details.append(__get_seed_doc_details(doc_id))
        
        print 'Number of seed documents selected:', len(seed_docs_details)
        
        return seed_docs_details
            
    
    
    def _on_click_search_start(self, event):
        """
        Actions to be done when the "Run Query" button is clicked

        """
        self.eval_relv = ""
        self.eval_irrelv = ""
        global dictionary_of_rows
        dictionary_of_rows = OrderedDict()
        queryText = self._tc_query_aggregated.GetValue().strip() 
        
        #----------------------------------------------------------- Validations
        
        if not self._is_lucene_index_available: # Lucene index is mandatory 
            self._show_error_message('Run Query Error!', 'Please select a valid index for searching.')
            return   
        elif queryText == '':
            self._show_error_message('Run Query Error!', 'Please enter a valid query.')
            return 
        elif not self._is_tm_index_available:
            self._show_error_message('Run Query Error!', 'Topic model is not available for topic search.')
            return 
        
        
        #------------------------------------------------------ Parses the query
        
        filteredQuery = queryText.splitlines(True)
        luceneQuery = ' '.join(term.strip() for term in filteredQuery)
        topicQuery = ' '.join(re.split(':', term)[1].strip()[1:][:-1] for term in filteredQuery if len(re.split(':', term)) > 1) # [1:][:-1] is for remove brackets 
        
        from utils.utils_email import lemmatize_tokens, stem_tokens
        norm_tokens = ' '.join( stem_tokens( lemmatize_tokens( topicQuery.split() ) ) )
        
        print 'Lucene query:', luceneQuery
        print 'TM query:', topicQuery, 'Stems/Lemmas:', norm_tokens
        
                

        #---------------------- Document Lucene and topic modeling-based ranking
        
        dominant_topics = get_dominant_query_topics(norm_tokens, self.lda_dictionary, self.lda_mdl, TOP_K_TOPICS)
        dominant_topics_idx = [idx for (idx, _) in dominant_topics] # gets the topic indices
        
        lucene_search_results = boolean_search_lucene_index(self.lucene_index_dir, luceneQuery, self._num_documents) # lucene search 
        lda_search_results = self.__search_tm_topics(dominant_topics_idx, self._num_documents, self.mdl_cfg) # returns [doc_id, doc_path, doc_name, doc_score] 
        self._lucene_scores_dict = self.__lucene_append_nonresponsive_docs(lucene_search_results) 
        self._lucene_docs_list = [doc[0] for doc in lucene_search_results]

        if len(lucene_search_results) > 0:
            self._init_search_results = self.__fuse_lucene_tm_scores(self._lucene_scores_dict, lda_search_results) # fuses LDA and Lucene 
        else: 
            self._init_search_results = lda_search_results


        #------------- Selecting seed documents from the initial ranking results
        
        self._seed_docs_details = self.__seed_docs_Kmeans_selection()
            
        self._responsive_files = []
        self._responsive_files_display = []
        self._unresponsive_files = []
        self._unresponsive_files_display = []
        self.sampled_files_responsive = []
        self.sampled_files_unresponsive = []
        self.__load_document_feedback()
        
        flag = True
        cnt  = 0
        for query in self._list_query_history.GetItems():
            if query == luceneQuery:
                flag = False
                self._choice_history = cnt
                break
            cnt += 1
        
        if flag:
            self._list_query_history.Append(luceneQuery)
            self._query_history.append([luceneQuery, -1,"",""])
            self._choice_history = cnt
        
        # self._tc_query_aggregated.SetValue('')
        
        #------------------------------------------------------- Change of focus
        self.smarter_ranking()
        self._st_Resp_documents.SetLabel(u'Responsive Documents (1/'+str(int(math.ceil(float(len(self._responsive_files))/6)))+')')
        self._st_unresp_documents.SetLabel(u'Unresponsive Documents (1/'+str(int(math.ceil(float(len(self._unresponsive_files))/6)))+')')
        
        self._current_page = 3
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    #----------------------------------------------------- Document Feedback tab
    
    def _on_click_feedback_smart_ranking(self, event):
        self._current_page = 2
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    def smarter_ranking(self):
        """
        Actions to be done when the "SMART Ranking" button is clicked
            
        """
        
        
        #-------------------------------- Train the SVM model for classification
        # 
        # Note: self._seed_docs_details has the seed documents details 
        #       from the document feedback tab. This is a tuple 
        #       list of [file_id, file_path, file_name, file_score, class_id] 
        #       
        #       self._init_search_results has the results from the 
        #       LDA-Lucene fusion method 
        #
        #       We only consider the documents that are reviewed responsive 
        #       or unresponsive to build the SVM model 
        
                
        from libsvm.python.svmutil import svm_problem, svm_parameter, svm_train, svm_predict
        SVM_C = 32 
        SVM_g = 0.5

        num_reviewed_seed_docs = 0
        reviewed_seed_docs_id = []
        reviewed_seed_docs_cls = []
        
        for seed_doc in self._seed_docs_details:
            
            doc_id, doc_path, doc_name, is_resp = seed_doc 
            
            if is_resp in ['Yes', 'No']: # Relevant and Irrelevant classes 
                reviewed_seed_docs_id.append(doc_id)
                reviewed_seed_docs_cls.append(self.__convert_is_relevant_to_id(is_resp))
                num_reviewed_seed_docs += 1
            
            
        print 'Number of reviewed seed documents (which are responsive or unresponsive):', num_reviewed_seed_docs
        
        if num_reviewed_seed_docs > 0:

            # lda_theta_file = self.mdl_cfg['LDA']['lda_theta_file']   
            # lda_theta = np.loadtxt(lda_theta_file, dtype=np.float)
            # num_docs, _ = lda_theta.shape
            
            # Include the Lucene scores as the last element  
            # This improves the accuracy by 7% on TREC2010:Query-201 
            # corpus_docs_features = [(theta_d + [self._lucene_scores_dict[doc_id]]) for doc_id, theta_d in enumerate(self._lda_theta.tolist())]                
            corpus_docs_features = self._lda_theta.tolist()    
    
            # reviewed_seed_docs_theta = lda_theta[reviewed_seed_docs_id,:]  
            reviewed_seed_docs_theta = [corpus_docs_features[doc_id] for doc_id in reviewed_seed_docs_id] 
            
            
            # SVM train 
            
            train_prob  = svm_problem(reviewed_seed_docs_cls, reviewed_seed_docs_theta)
            train_param = svm_parameter('-t 2 -c 0 -b 1 -c %f -g %f' % (SVM_C, SVM_g))
            self._seed_docs_svm_mdl = svm_train(train_prob, train_param)
            
            # SVM prediction for all the documents in the results 
            
            self._docs_svm_label, _, p_val = svm_predict([0]*self._num_documents, corpus_docs_features, self._seed_docs_svm_mdl, '-b 0')
            self._docs_svm_decision_values = [p_v[0] for p_v in p_val]
            
            # print self._docs_svm_label
            # print self._docs_svm_decision_values  
            
        else: 
            
            print 'No training documents available for SVM training.'      
        
        
        
        #---------- Classify documents as responsive or unresponsive (using SVM)
     
        if len(self._init_search_results) == 0: 
            self.SetStatusText('No documents found in the initial ranking results. Exiting the ranking!')
            return 
        
        
        def __convert_to_display_label(class_id):
            if class_id == self.RESPONSIVE_CLASS_ID: return 'Responsive'
            else: return 'Unresponsive'   
            
        def __classify_by_threshold(doc_score):
            if float(doc_details[3]) >= CUT_OFF_NORM: return 'Responsive'
            else: return 'Unresponsive'                   
            
#        key = 0 
        
        for doc_details in self._init_search_results:
            
            doc_id, doc_path, doc_name, doc_score = doc_details # doc_details: [file_id, file_path, file_name, score]
            svm_predicted_class = self._docs_svm_label[doc_id]
            
            display_doc_details = [doc_id, doc_path, doc_name, doc_score, __convert_to_display_label(svm_predicted_class)]
            
            # print doc_name, doc_score, self._doc_true_class_ids[doc_id], svm_predicted_class, __classify_by_threshold(doc_score) 
            
            if svm_predicted_class == self.RESPONSIVE_CLASS_ID: # float(display_doc_details[3]) >= CUT_OFF_NORM:
                self._responsive_files.append([doc_path, self.__is_relevant(self._doc_true_class_ids[doc_id]), "", doc_score, doc_id])
                self._responsive_files_display.append([display_doc_details[2],display_doc_details[1],display_doc_details[3]])
            else:
                self._unresponsive_files.append([doc_path, self.__is_irrelevant(self._doc_true_class_ids[doc_id]), "", doc_score, doc_id])
                self._unresponsive_files_display.append([display_doc_details[2],display_doc_details[1],display_doc_details[3]])
                
            if self.__is_relevant(self._doc_true_class_ids[doc_id]) =='Yes':
                self.add_update_seedlist(doc_id, doc_path, os.path.basename(doc_path), 'Yes')
            elif self.__is_irrelevant(self._doc_true_class_ids[doc_id]) =='Yes':
                self.add_update_seedlist(doc_id, doc_path, os.path.basename(doc_path), 'No')  

#            # Put the results to the dictionary_of_rows
#            dictionary_of_rows.__setitem__(str(key), display_doc_details)
#            key += 1
        
        #------------------------------------------------------ Generate samples
        
        
        seed_dict = dict()
        for seed in self._seed_docs_details:
            seed_dict[seed[1]] = seed[3] # gets seed classes 
        
        correct_files = 0.0

        for doc in self._responsive_files:
            if seed_dict.has_key(doc[0]):
                if seed_dict[doc[0]] == 'Yes':
                    correct_files += 1.0
            
        for doc in self._unresponsive_files:
            if seed_dict.has_key(doc[0]):
                if seed_dict[doc[0]] == 'No':
                    correct_files += 1.0
        
        print 
        print 'Computes the SVM accuracy on the seed documents (train)'
        print 
        print 'TP+TN:', correct_files
        print 'Number of seeds:', len(self._seed_docs_details) 
        print 'Accuracy based on seeds:', correct_files / len(self._seed_docs_details) 
        print 
        
        self._query_history[self._choice_history][1] = float(correct_files)/len(self._seed_docs_details)     
        
        
        #----------------- Generate samples of Relevant and Irrelevant documents
        
        self._generate_file_samples()
        self._generate_file_samples_unres()
        
          
        self._lc_results_res._set_shelve_dir(self._shelve_dir)
        self._lc_results_res.itemDataMap = dictionary_of_rows
        self._lc_results_res.Bind(wx.EVT_LIST_COL_CLICK, self._lc_results_res._on_header_column_click)

        self._lc_results_unres._set_shelve_dir(self._shelve_dir)
        self._lc_results_unres.itemDataMap = dictionary_of_rows
        self._lc_results_unres.Bind(wx.EVT_LIST_COL_CLICK, self._lc_results_unres._on_header_column_click)
        
        items = dictionary_of_rows.items()
        #self._reset_persistent_shelves()
        #self._create_persistent_shelves(items)
        global present_chunk_res
        global present_chunk_unres
        present_chunk_res = 0
        present_chunk_unres = 0
    
        self._lc_results_res._populate_results(present_chunk,self._responsive_files_display)
        self._lc_results_unres._populate_results(present_chunk,self._unresponsive_files_display)
        self._tc_file_preview_pane.SetValue('')
        
        
        #----------------------------------------------- Goes to the results tab
        
        
                  
    
    def _on_click_feedback_back(self, event):
        self._current_page = 0
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
        
    def __load_document_feedback(self):
        
        num_seed_docs = len(self._seed_docs_details)
        
        self._st_document_feedback_title.SetLabel(u"Please review the below %d documents to increase the accuracy of document retrieval." % num_seed_docs)
        
        self.panel_feedback_doc = TaggingControlFeedback(self._panel_feedback_doc, self)
        self.panel_feedback_doc._setup_review_tab()
        
        
    def _on_rbx_doc_feedback_updated(self, event):
        '''
        Handles the document feedback tab, selected seed 
        document's 'Responsive' radio button group changes 
         
        Note: If you make any changes in this function, 
        you may consider reviewing the custom class 
        TaggingControlFeedback 
                
        TODO: All exceptions should be captured and logged 
        using the main logging method, instead of printing 
        them to the command line.  
        '''
        try:
            row_id = self.panel_feedback_doc.GetFocusedItem()
            if row_id < 0: return 
            
            is_relevant = self._rbx_doc_feedback.GetStringSelection()
            selected_doc_id = self._seed_docs_details[row_id][0]
            
            if is_relevant in ['Yes', 'No', 'Uncertain']:
                self.panel_feedback_doc.SetStringItem(row_id, 2, is_relevant)
                self._seed_docs_details[row_id][3] = is_relevant
            else: # when not reviewed 
                self.panel_feedback_doc.SetStringItem(row_id, 2, '')
                self._seed_docs_details[row_id][3] = ''

            self._doc_true_class_ids[selected_doc_id] = self.__convert_is_relevant_to_id(is_relevant)
            self.panel_feedback_doc.SetItemBackgroundColour(row_id, self._get_relevancy_color(is_relevant))    

                
        except Exception, e:
            print e
    
    def __setup_accuracy_grid(self):
        
        # TODO: Sahil, please use the below code to display samples' 
        # details in the Report tab 
        
        print 
        
        num_irrelevant_docs = len([1 for doc_sample in self.sampled_files_unresponsive if doc_sample[1] == 'Yes'])
        num_relevant_docs = len([1 for doc_sample in self.sampled_files_unresponsive if doc_sample[1] == 'No'])
        irrelevant_size = len(self.sampled_files_unresponsive)
        irrelevant_acc = float(num_irrelevant_docs) * 100.0/ float(irrelevant_size)
        
        # We ignore uncertain and not reviewed documents from the calculation  
        print 'Irrelevant Sample #%d: relevant #%d, irrelevant #%d, accuracy %1.4f' % (irrelevant_size, num_relevant_docs, 
                                                                                       num_irrelevant_docs, irrelevant_acc)
        # print 'Irrelevant sample accuracy:{:2.2f}'.format(float(num_irrelevant_docs) * 100.0/ float(num_irrelevant_docs + num_relevant_docs))
        self.eval_irrelv = "%d / %d" % (num_irrelevant_docs, irrelevant_size)

        num_irrelevant_docs = len([1 for doc_sample in self.sampled_files_responsive if doc_sample[1] == 'No'])
        num_relevant_docs = len([1 for doc_sample in self.sampled_files_responsive if doc_sample[1] == 'Yes'])
        relevant_size = len(self.sampled_files_responsive)
        relevant_acc = float(num_relevant_docs) * 100.0/ float(relevant_size)
        
        # We ignore uncertain and not reviewed documents from the calculation  
        print 'Relevant Sample #%d: relevant #%d, irrelevant #%d, accuracy %1.4f' % (relevant_size, num_relevant_docs, 
                                                                                     num_irrelevant_docs, relevant_acc)
        # print 'Relevant sample accuracy:{:2.2f}'.format(float(num_relevant_docs) * 100.0/ float(num_irrelevant_docs + num_relevant_docs))
        self.eval_relv = "%d / %d" % (num_relevant_docs, relevant_size)
        

        print 
        num_lucene_tn = 0
        num_lucene_tp = 0 
        for doc_sample in self.sampled_files_unresponsive:
            _, is_irrelevant, _, _, doc_id = doc_sample
            if doc_id not in self._lucene_docs_list and is_irrelevant == 'Yes':
                num_lucene_tn += 1
            elif doc_id in self._lucene_docs_list and is_irrelevant == 'No':
                num_lucene_tp += 1                 
        lucene_IRS_acc = float(num_lucene_tn) * 100.0 / float(irrelevant_size)

        print 'Irrelevant Sample #%d (LUCENE): TP #%d, TN #%d, accuracy %1.4f' % (irrelevant_size, num_lucene_tp, num_lucene_tn, lucene_IRS_acc)

        num_lucene_tn = 0
        num_lucene_tp = 0 
        for doc_sample in self.sampled_files_responsive:
            _, is_relevant, _, _, doc_id = doc_sample
            if doc_id not in self._lucene_docs_list and is_relevant == 'No':
                num_lucene_tn += 1
            elif doc_id in self._lucene_docs_list and is_relevant == 'Yes':
                num_lucene_tp += 1
        lucene_RS_acc = float(num_lucene_tp) * 100.0 / float(relevant_size)
        
        self._query_history[self._choice_history][2]=self.eval_relv
        self._query_history[self._choice_history][3]=self.eval_irrelv
        
        print 'Relevant Sample #%d (LUCENE): TP #%d, TN #%d, accuracy %1.4f' % (relevant_size, num_lucene_tp, num_lucene_tn, lucene_RS_acc)
        print 

        if self._grid_query_accuracy.NumberRows != len(self._query_history):
            self._grid_query_accuracy.InsertRows(0, len(self._query_history) - self._grid_query_accuracy.NumberRows)
            

        for row_count, query_details in enumerate(self._query_history):
            query, accuracy, rev, irrev = query_details
            self._grid_query_accuracy.SetCellValue(row_count, 0, query)
            if accuracy != -1:
                self._grid_query_accuracy.SetCellValue(row_count, 1, str(accuracy))
            self._grid_query_accuracy.SetCellValue(row_count, 2, str(rev))
            self._grid_query_accuracy.SetCellValue(row_count, 3, str(irrev))
                     
    def _on_click_update_results(self, event):
        '''
        This function incorporates the user ratings into 
        the ranked list. Here, we combine the highly rated 
        documents, represent it in topic modeling space, 
        and search for similar documents.  
        
        '''
        '''
        self.shelf_query = shelve.open(os.path.join(self._shelve_dir, str("rating" + SHELVE_FILE_EXTENSION)), writeback=True)  # open -- file may get suffix added by low-level
        self.shelf_query['query'] = self._tc_query.GetValue().strip() 
        for row in dictionary_of_rows:
            result = dictionary_of_rows[row]
            if result[11] != 0:
                self.shelf_query[str(result[0])] = str(result[11])
        self.shelf_query.close()
        dlg = wx.MessageDialog(self, "Information is recorded, Thank you", "Update Results", wx.OK)
        dlg.ShowModal()  # Shows it
        dlg.Destroy()  # finally destroy it when finished.
        '''
        self._current_page = 2
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def load_contextual_feedback(self, topic_list):
        _bgd_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.m_staticText = wx.StaticText(self._panel_topics, wx.ID_ANY, (
            u"You may be interested in highlighting the following topics (relevant topical words) in the search process.\nPlease mark relevant keywords or skip to next page"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText.Wrap(-1)
        _bgd_sizer.Add(self.m_staticText, 0, wx.ALL, 5)
        
        _chk_Sizer = wx.GridBagSizer(0, 0)
        _chk_Sizer.SetFlexibleDirection(wx.BOTH)
        _chk_Sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        chkbox_cnt = 0
        self.chk_box = []
        
        for topic in topic_list:
            radioBox_choices = [ (u"Relevant"), (u"Neutral"), (u"Irrelevant") ]
            self.chk_box.append(wx.RadioBox(self._panel_topics, wx.ID_ANY, (topic), wx.DefaultPosition, wx.Size(500, 50) , radioBox_choices, 1, wx.RA_SPECIFY_ROWS))
            self.chk_box[chkbox_cnt].SetSelection(1)
            
            _chk_Sizer.Add(self.chk_box[chkbox_cnt], wx.GBPosition(int(chkbox_cnt / 2), int(2 + chkbox_cnt % 2)), wx.GBSpan(1, 1), wx.ALL, 5)
            chkbox_cnt += 1
            if chkbox_cnt == 10:
                break
            
        self._next_cf_button = wx.Button(self._panel_topics, wx.ID_ANY, (u"Save Keywords"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._skip_cf_button = wx.Button(self._panel_topics, wx.ID_ANY, (u"Skip"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._next_cf_button.Bind(wx.EVT_BUTTON, self._on_click_contextual_feed)
        self._skip_cf_button.Bind(wx.EVT_BUTTON, self._on_click_skip_contextual_feed)
        _chk_Sizer.Add(self._next_cf_button, wx.GBPosition(chkbox_cnt / 2, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        _chk_Sizer.Add(self._skip_cf_button, wx.GBPosition(chkbox_cnt / 2, 3), wx.GBSpan(1, 1), wx.ALL, 5)
        
        _bgd_sizer.Add(_chk_Sizer, 1, wx.EXPAND, 5)
        self._panel_topics.SetSizer(_bgd_sizer)
        self._panel_topics.Layout()
        _bgd_sizer.Fit(self._panel_topics)
        
    def _on_click_skip_contextual_feed(self, event):
        self._current_page = 4
        self.__load_document_feedback()
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def _on_click_contextual_feed(self, event):
        
        # for chk_box in self.chk_box:
            # print chk_box.GetSelection()
        
        self._current_page = 3
        self.__load_document_feedback()
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
        
#        
#    def _on_rbx_result_responsive_update(self, event):
#        
#        
#        try:
#            selected_doc_id = self._lc_results_res.GetFocusedItem()
#            responsive_status = self._rbx_feedack_res.GetStringSelection()
#            if responsive_status == 'Responsive': 
#                self._lc_results_res.SetStringItem(selected_doc_id, 3, 'Yes')
#                #self._seed_docs_details[selected_doc_id][2] = 'Responsive'
#            elif responsive_status == 'Unresponsive': 
#                self._lc_results_res.SetStringItem(selected_doc_id, 3, 'No')
#                #self._seed_docs_details[selected_doc_id][2] = 'Unresponsive'
#            else: 
#                self._lc_results_res.SetStringItem(selected_doc_id, 3, '')
#                #self._seed_docs_details[selected_doc_id][2] = ''
#            
#        except Exception, e:
#            print e
#            
#    def _on_rbx_result_unresponsive_update(self, event):
#        
#        try:
#            selected_doc_id = self._lc_results_unres.GetFocusedItem()
#            responsive_status = self._rbx_feedack_unres.GetStringSelection()
#            if responsive_status == 'Responsive': 
#                self._lc_results_unres.SetStringItem(selected_doc_id, 3, 'Yes')
#                #self._seed_docs_details[selected_doc_id][2] = 'Responsive'
#            elif responsive_status == 'Unresponsive': 
#                self._lc_results_unres.SetStringItem(selected_doc_id, 3, 'No')
#                #self._seed_docs_details[selected_doc_id][2] = 'Unresponsive'
#            else: 
#                self._lc_results_unres.SetStringItem(selected_doc_id, 3, '')
#                #self._seed_docs_details[selected_doc_id][2] = ''
#            
#        except Exception, e:
#            print e
    
    def _init_confidence(self):
        '''
        Sets default confidence level and interval in Top Level interface
        Arguments: None
        Returns: None
        '''
        
        self.confidence_val = DEFAULT_CONFIDENCE_LEVEL / Decimal('100')
        self.confidence_val_unres=self.confidence_val
        items = self._cbx_confidence_levels.GetItems()
        items_unres=self._cbx_confidence_levels_unres.GetItems()
        index = -1
        try:
            index = items.index(str(DEFAULT_CONFIDENCE_LEVEL))
            self._cbx_confidence_levels.SetSelection(index)
        except ValueError:
            self._cbx_confidence_levels.ChangeValue(str(DEFAULT_CONFIDENCE_LEVEL))
            
        try:
            index = items_unres.index(str(DEFAULT_CONFIDENCE_LEVEL))
            self._cbx_confidence_levels_unres.SetSelection(index)
        except ValueError:
            self._cbx_confidence_levels_unres.ChangeValue(str(DEFAULT_CONFIDENCE_LEVEL))
    
        
        # Set default confidence interval 
        self.precision_val = DEFAULT_CONFIDENCE_INTERVAL / 100
        str_precision = str(int(DEFAULT_CONFIDENCE_INTERVAL))
        self._tc_confidence_interval.ChangeValue(str_precision)
        
        self.precision_val_unres = DEFAULT_CONFIDENCE_INTERVAL / 100
        str_precision = str(int(DEFAULT_CONFIDENCE_INTERVAL))
        self._tc_confidence_interval_unres.ChangeValue(str_precision)

        # Hides the status messages 
        self._st_num_samples_res.Show(False)
        self._st_num_samples_unres.Show(False)
        #self._st_num_samples_ind_unres.Show(False)                    
    def _on_click_continue(self, event):
        self._generate_file_samples()
        self._generate_file_samples_unres()
        self._current_page = 4
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
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
                self._cbx_confidence_levels_unres.Append(cl)
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
            

        # Maybe intermittently null string, escaping 
        try:
            # Checks for positive values 
            ci = float(self._tc_confidence_interval.GetValue())
            if ci <= 0 or ci > 99:
                show_precision_error()
                return 
            
            self.get_precision_as_float()
            if self._chk_toggle_cl_level.Value==True:
                self.precision_val_unres=self.precision_val
            #self._tc_out_confidence_interval.ChangeValue(self._tc_confidence_interval.GetValue())
            #self.SetStatusText('Confidence interval is changed as ' + self._tc_confidence_interval.GetValue())
        except ValueError:
            show_precision_error()
            return None 
        
        self._generate_file_samples()
        
    def _on_precision_changed_unres(self, event):
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
            

        # Maybe intermittently null string, escaping 
        try:
            # Checks for positive values 
            ci = float(self._tc_confidence_interval.GetValue())
            if ci <= 0 or ci > 99:
                show_precision_error()
                return 
            
            self.get_precision_as_float_unres()
            #self._tc_out_confidence_interval.ChangeValue(self._tc_confidence_interval.GetValue())
            #self.SetStatusText('Confidence interval is changed as ' + self._tc_confidence_interval.GetValue())
        except ValueError:
            show_precision_error()
            return None 
        
        self._generate_file_samples_unres()
        
    def _generate_file_samples(self):
        '''
        This function generates file sample based on the 
        class variables such as file_list, confidence_val, 
        and precision_val and sets the sample status label     
        '''

        # Generate samples
        self.sampled_files_responsive = random_sampler(self._responsive_files, self.confidence_val, self.precision_val, self.SEED)
        if self._chk_toggle_cl_level.Value==True:
            self.sampled_files_unresponsive = random_sampler(self._unresponsive_files, self.confidence_val, self.precision_val, self.SEED)
        
        self._st_num_samples_res.SetLabel('Responsive: %d sample documents will be selected' % len(self.sampled_files_responsive))
        self._st_num_samples_res.Show()
        
        if self._chk_toggle_cl_level.Value==True:
            self._st_num_samples_unres.SetLabel('Unresponsive: %d sample documents will be selected'% len(self.sampled_files_unresponsive))
            self._st_num_samples_unres.Show()
                
    def _generate_file_samples_unres(self):
        '''
        This function generates file sample based on the 
        class variables such as file_list, confidence_val, 
        and precision_val and sets the sample status label     
        '''

        # Generate samples
        
        self.sampled_files_unresponsive = random_sampler(self._unresponsive_files, self.confidence_val_unres, self.precision_val_unres, self.SEED)
        self._st_num_samples_ind_unres.SetLabel('Unresponsive: %d sample documents will be selected'% len(self.sampled_files_unresponsive))
        self._st_num_samples_ind_unres.Show(True)

     
#        # step 1: gets highly rated documents 
#        
#        
#        selected_docs = []  
#        excluded_docs = []
#        
#        for shelf_file_name in self._shelve_file_names:
#            sd = shelve.open(shelf_file_name)
#            for k in sd.keys():
#                row = sd[k]
#                if int(row[-1]) > USER_RATINGS_CUT_OFF:
#                    selected_docs.append(row) 
#                else: 
#                    excluded_docs.append(row) 
#            sd.close()
#            
#        # step 2: combine all email bodies to a single document 
#        # row index 5 is for the body field 
#        
#        bag_of_words = ''
#        for sdoc in selected_docs:
#            bag_of_words += sdoc[5]
#        
#        # bag_of_words_td = get_lda_query_td(bag_of_words, self.lda_dictionary, self.lda_mdl)
#        
#        # step 3: compute the distances between bag_of_words and 
#        # all other documents 
#        
#        excluded_docs = compute_topic_similarities(bag_of_words, selected_docs + excluded_docs, self.lda_dictionary, self.lda_mdl, self._lda_num_topics)
#        
#        
#        # TODO: need to figure out a good way to combine topic modeling 
#        #       similarity score and lucene scores      
#        
#        

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
                                       
    def get_precision_as_float_unres(self):
        '''
        Converts precision to float
        Returns: Nothing
        Arguments: Nothing
        '''
        try:
            self.precision_val_unres = float(self._tc_confidence_interval_unres.GetValue()
                                       ) / 100.0 
        except ValueError:
            self.precision_val_unres = float(int(self._tc_confidence_interval_unres.GetValue())
                                       ) / 100.0
                                       
    def _on_confidence_changed(self, event):
        '''
        Triggers an event and updates the sample list on confidence - aka 
        confidence level change
        Arguments: Event of new confidence
        Returns: Nothing
        '''
        self.confidence_val = Decimal(self._cbx_confidence_levels.GetValue()) / Decimal('100')
        if self._chk_toggle_cl_level.Value==True:
            self.confidence_val_unres=self.confidence_val
        self._generate_file_samples()
        
    def _on_confidence_changed_unres(self, event):
        
        self.confidence_val_unres = Decimal(self._cbx_confidence_levels_unres.GetValue()) / Decimal('100')
        self._generate_file_samples_unres()

    def _on_click_cl_goback( self, event ):
        self._current_page = 3
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    def _on_click_cl_next( self, event ):
        self._review_unres = TaggingControlSmarter(self._panel_review_unres, self.sampled_files_unresponsive,
                                                   self._rbx_response_unres, 
                                                   self._tc_preview_tags_unres, self._panel_doc_tag_unres, 
                                                   self._get_irrelevancy_color)
        self._review_unres._setup_review_tab('Irrelevant')
        self._current_page = 5
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
  
    def _on_click_change_unres_focus(self,event):
        if self._chk_toggle_cl_level.Value==True:
            self.precision_val_unres=self.precision_val
            self.confidence_val_unres=self.confidence_val
            self._generate_file_samples()
            self._panel_unres_cl.Show(False)
            self._st_num_samples_unres.Show(True)
        else:
            self.confidence_val_unres = Decimal(self._cbx_confidence_levels_unres.GetValue()) / Decimal('100')
            self.precision_val_unres = float(self._tc_confidence_interval_unres.GetValue()) / 100.0
            self._generate_file_samples_unres()
            self._panel_unres_cl.Show(True)
            self._st_num_samples_unres.Show(False)
        
    def _combine_lucene_tm_results(self, fs_results, ts_results):
        
        num_metadata_types = len(MetadataType._types)
        default_lowest_score = -99999
        
        def get_tm_score(file_id, ts_results):
            '''
            TODO: Need to improve this logic. It'd be 
            good if we can keep the scores in a dictionary. 
            Otherwise, this function will be in efficient 
            '''
            
            for ts_row in ts_results:
                if ts_row[num_metadata_types] == file_id:
                    return ts_row[num_metadata_types + 1]
                
            return default_lowest_score    
        
        
        rows = [] 
        
        for fs_row in fs_results:
            tm_score = get_tm_score(fs_row[num_metadata_types], ts_results)
            fs_row[num_metadata_types + 1] = tm_score
            rows.append(fs_row) 
            print fs_row
        
        return rows 
        
    def _on_rbx_relevant_feeback( self, event ):
        '''
        Handles "Sample Relevant" tab, document relevancy feedback 
        radio button group updated event  
         
        '''
        selected_row_id = self._review_res.GetFocusedItem()
        
        if selected_row_id > -1:
            
            is_relevant = self._rbx_response_res.GetStringSelection() 
            
            if is_relevant in ['Yes', 'No', 'Uncertain']:
                self._review_res.SetStringItem(selected_row_id, 2, is_relevant)
                self.sampled_files_responsive[selected_row_id][1] = is_relevant
            else: # when not reviewed 
                self._review_res.SetStringItem(selected_row_id, 2, '')
                self.sampled_files_responsive[selected_row_id][1] = ''
                
            self.add_update_seedlist(self.sampled_files_unresponsive[selected_row_id][4],self.sampled_files_unresponsive[selected_row_id][0],os.path.basename(self.sampled_files_unresponsive[selected_row_id][0]),is_relevant)

            self._review_res.SetItemBackgroundColour(selected_row_id, self._get_relevancy_color(is_relevant)) 
            
            selected_doc_id = self.sampled_files_responsive[selected_row_id][0]
            self._doc_true_class_ids[selected_doc_id] = self.__convert_is_relevant_to_id(is_relevant)
              
#    
#    def _on_rbx_privileged_updated_res( self, event ):
#        '''
#        Handles the selected document privileged check box 
#        check and uncheck events 
#         
#        '''
#        selected_doc_id = self._review_res.GetFocusedItem()
#        if(selected_doc_id != -1):
#            privileged_status = self._rbx_privilage_res.GetStringSelection() 
#            if privileged_status == 'Yes': 
#                self._review_res.SetStringItem(self._review_res.GetFocusedItem(), 3, 'Yes')
#                self.sampled_files_responsive[selected_doc_id][2]='Yes'
#            elif privileged_status == 'No': 
#                self._review_res.SetStringItem(self._review_res.GetFocusedItem(), 3, 'No')
#                self.sampled_files_responsive[selected_doc_id][2]='No'
#            elif privileged_status == 'Unknown': 
#                self._review_res.SetStringItem(self._review_res.GetFocusedItem(), 3, '')
#                self.sampled_files_responsive[selected_doc_id][2]=''

    def _on_click_relevant_clear_tags( self, event ):
        '''
        Clear all assigned document tags from the list control 
        '''
        try:
            for i in range(0, len(self.sampled_files_responsive)):
                self._review_res.SetStringItem(i, 2, '')
                self._review_res.SetItemBackgroundColour(i, self._get_relevancy_color('Not Reviewed'))
                self.sampled_files_responsive[i][1] = ''
                
            self._rbx_response_res.SetSelection(2)  
        except Exception, e:
            print e

    def _on_rbx_irrelevant_feeback( self, event ):
        '''
        Handles "Sample Irrelevant" tab, document irrelevancy feedback 
        radio button group updated event  
         
        '''
        selected_row_id = self._review_unres.GetFocusedItem()
        
        if selected_row_id > -1:
            
            is_irrelevant = self._rbx_response_unres.GetStringSelection() 
            seed_relevant=is_irrelevant
            if is_irrelevant in ['Yes', 'No', 'Uncertain']:
                self._review_unres.SetStringItem(selected_row_id, 2, is_irrelevant)
                self.sampled_files_unresponsive[selected_row_id][1] = is_irrelevant
                if is_irrelevant == 'Yes':
                    seed_relevant = 'No'
                elif is_irrelevant == 'No':
                    seed_relevant = 'Yes'
            else: # when not reviewed 
                self._review_unres.SetStringItem(selected_row_id, 2, '')
                self.sampled_files_unresponsive[selected_row_id][1] = ''
            
            self.add_update_seedlist(self.sampled_files_unresponsive[selected_row_id][4],self.sampled_files_unresponsive[selected_row_id][0],os.path.basename(self.sampled_files_unresponsive[selected_row_id][0]),seed_relevant)
            
            self._review_unres.SetItemBackgroundColour(selected_row_id, self._get_irrelevancy_color(is_irrelevant)) 
            
            selected_doc_id = self.sampled_files_unresponsive[selected_row_id][0]
            self._doc_true_class_ids[selected_doc_id] = self.__convert_is_irrelevant_to_id(is_irrelevant)
            
    def add_update_seedlist(self,file_id,path,name,seed_relevant):
        i = 0
        
        while i <self._seed_docs_details.__len__():
            print str(self._seed_docs_details[i][0]) + " " + str(file_id)
            if self._seed_docs_details[i][0] == file_id:
                self._seed_docs_details[i][3] = seed_relevant
                break
            i = i + 1
            
        if i >= self._seed_docs_details.__len__():
            self._seed_docs_details.append([file_id,path,name,seed_relevant])
        #print self._seed_docs_details   
        
#    def _on_rbx_privileged_updated_unres( self, event ):
#        '''
#        Handles the selected document privileged check box 
#        check and uncheck events 
#         
#        '''
#        privileged_status = self._rbx_privilage_unres.GetStringSelection() 
#        if privileged_status == 'Yes': 
#            self._review_unres.SetStringItem(self._review_unres.GetFocusedItem(), 3, 'Yes')
#        elif privileged_status == 'No': 
#            self._review_unres.SetStringItem(self._review_unres.GetFocusedItem(), 3, 'No')
#        elif privileged_status == 'Unknown': 
#            self._review_unres.SetStringItem(self._review_unres.GetFocusedItem(), 3, '')

    def _on_click_irrelevant_clear_tags( self, event ):
        '''
        Clear all assigned document tags from the list control 
        '''
        try:
            for i in range(0, len(self.sampled_files_unresponsive)):
                self._review_unres.SetStringItem(i, 2, '') 
                self._review_unres.SetItemBackgroundColour(i, self._get_irrelevancy_color('Not Reviewed'))
                self.sampled_files_unresponsive[i][1] = ''     

            self._rbx_response_unres.SetSelection(2)   
            
            self._is_rt_updated = True
        except Exception, e:
            print e
            
    def _on_click_review_gen_report_res( self, event ):
            
        self.confidence_val_rep = self.confidence_val
        self.precision_val_rep =self.precision_val
        self.file_list = self._responsive_files
        self.sampled_files = self.sampled_files_responsive
        self._gen_report(self.sampled_files_responsive, self._cbx_report_types_res.GetValue(), 
                         'responsive_sample_', 'Responsive Document Sample Review Report')
    
    def _on_click_review_gen_report_unres( self, event ):
            
        self.confidence_val_rep = self.confidence_val_unres
        self.precision_val_rep = self.precision_val_unres
        self.file_list = self._unresponsive_files
        self.sampled_files = self.sampled_files_unresponsive
        self._gen_report(self.sampled_files_unresponsive, self._cbx_report_types_unres.GetValue(),
                         'unresponsive_sample_', 'Unresponsive Document Sample Review Report')
    
    def _gen_report( self, samples_lst, report_type, file_type, report_title='Document Sample Review Report' ):
        
        def __save_html_report(html_body, file_name, report_title=report_title):
            '''
            Stores into a file 
            '''
            
            try:
                with open(file_name, "w") as hw: 
                    hw.write(unicode(
                    """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
                    <html>
                    <head>
                        <title>%s</title>
                    </head>
                    <body style="font-family:verdana,helvetica;font-size:9pt">
                    <h2>%s</h2>
                    
                    Report overview: 
                    
                    <br/><br/>
                    """ % (report_title, report_title)))
                    
                    hw.write(unicode(__gen_specifications_html()))
        
                    hw.write(unicode(html_body))
    
                    hw.write(unicode(
                    """
                    <hr/>
                    <p>Report is generated on: %s</p>
                    </body>
                    </html>""" % datetime.now().strftime("%A, %d. %B %Y %I:%M%p")))
            except Exception, e:
                print e
                
    
        def __gen_specifications_html(): 
            try:
                hrow = TableRow(cells=['Sampler Specifications', 'Entries'], bgcolor='#6E6E6E')
                setting_table = Table(header_row=hrow, border=0)
                '''
                config_cell = TableCell("Source document folder", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(self.dir_path, bgcolor = '#CEF6F5', align = 'left')
                setting_table.rows.append([config_cell, setting_cell])
                
                config_cell = TableCell("Sampled output folder", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(self.output_dir_path, bgcolor = '#CEF6F5', align = 'left')
                setting_table.rows.append([config_cell, setting_cell])
                '''
                config_cell = TableCell("Confidence level (%)", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(self.confidence_val_rep*100, bgcolor = '#CEF6F5', align = 'right')
                setting_table.rows.append([config_cell, setting_cell])
                
                config_cell = TableCell("Confidence interval (%)", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(self.precision_val_rep*100, bgcolor = '#CEF6F5', align = 'right')
                setting_table.rows.append([config_cell, setting_cell])
                
                config_cell = TableCell("Total documents in the source document folder", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(len(self.file_list), bgcolor = '#CEF6F5', align = 'right')
                setting_table.rows.append([config_cell, setting_cell])
                
                config_cell = TableCell("The sample size", bgcolor = '#CEF6F5', align = 'left')
                setting_cell = TableCell(len(self.sampled_files), bgcolor = '#CEF6F5', align = 'right')
                setting_table.rows.append([config_cell, setting_cell])
                
                return str(setting_table)
            except Exception,e:
                print e
            
        def __gen_complete_html_report(samples, responsive, privileged):
            try:
                # Generate HTML tags for all documents 
                hrow = TableRow(cells=['#', 'File Name', 'Responsive', 'Privileged','Ranking Score'], bgcolor='#6E6E6E')
                all_table = Table(header_row=hrow)
                cnt = 1
                for fs in samples:
                    
                    rc_colr = resp_colors[rstatus(fs[1])]
                    pc_colr = priv_colors[rstatus(fs[2])]
                    r_colr = row_colors[row_status(fs[1], fs[2])]
                    num_cell = TableCell(cnt, bgcolor=r_colr, align='center')
                    file_name = link(fs[0], fs[0])
                    fn_cell = TableCell(file_name, bgcolor=r_colr)
                    resp_cell = TableCell(fs[1], bgcolor=rc_colr, align='center')
                    priv_cell = TableCell(fs[2], bgcolor=pc_colr, align='center')
                    rank_cell = TableCell(fs[3], bgcolor=r_colr, align='center')
                    
                    all_table.rows.append([num_cell, fn_cell, resp_cell, priv_cell,rank_cell])
                    cnt = cnt + 1
                
                html_body = """
                %s 
        
                %s 
        
                <hr/>
                <h3>Complete Sample</h3>
                %s 
                <br/>
                """ % (__gen_responsive_html_report(responsive), __gen_privileged_html_report(privileged), str(all_table))
                
                return html_body
            except Exception,e:
                print e
           
        def __gen_responsive_html_report(responsive):
            '''
            Generate HTML tags for responsive documents 
            '''
            try:
                if len(responsive) == 0: return ''
                hrow = TableRow(cells=['#', 'File Name','Ranking Score'], bgcolor='#6E6E6E')
                resp_table = Table(header_row=hrow)
                cnt = 1
                for fs in responsive:
                    # r_colr = resp_colors['Yes']
                    num_cell = TableCell(cnt, align='center') # bgcolor=r_colr, 
                    file_name = link(fs[0], fs[0])
                    fn_cell = TableCell(file_name) # , bgcolor=r_colr
                    rank_cell = TableCell(fs[3], align='center')
                    resp_table.rows.append([num_cell, fn_cell,rank_cell])
                    cnt = cnt + 1
                    
                html_body = """
                <hr/>
                <h3>Responsive Documents</h3>
                %s 
                <br/>
                """ % str(resp_table)
                
                return html_body
            except Exception,e:
                print e
          
        def __gen_privileged_html_report(privileged):
            '''
            Generate HTML tags for privileged documents 
            '''
            try:
                if len(privileged) == 0: return ''
                
                hrow = TableRow(cells=['#', 'File Name','Ranking Score'], bgcolor='#6E6E6E')
                priv_table = Table(header_row=hrow)
                cnt = 1
                for fs in privileged:
                    # r_colr = priv_colors['Yes']
                    num_cell = TableCell(cnt, align='center') # bgcolor=r_colr, 
                    file_name = link(fs[0], fs[0])
                    fn_cell = TableCell(file_name) # , bgcolor=r_colr
                    rank_cell = TableCell(fs[3], align='center')
                    priv_table.rows.append([num_cell, fn_cell, rank_cell])
                    cnt = cnt + 1
                html_body = """
                <hr/>
                <h3>Privileged Documents</h3>
                %s 
                <br/>
                """ % str(priv_table)
                
                return html_body
            except Exception,e:
                print e

        
       
        try:
            if report_type == 'Responsive':
                file_name = os.path.join(self._project_dir_path, file_type+REPORT_RESPONSIVE)   
                responsive = []
                for fs in samples_lst: 
                    if fs[1] == 'Yes': 
                        responsive.append(fs)
                if len(responsive) == 0:
                    self._show_error_message('Report Generation', 'There are no responsive documents available.')
                    return 
                html_body = __gen_responsive_html_report(responsive)
            elif report_type == 'Privileged':
                file_name = os.path.join(self._project_dir_path, file_type+REPORT_PRIVILEGED)   
                privileged = []
                for fs in samples_lst: 
                    if fs[2] == 'Yes': 
                        privileged.append(fs)
                if len(privileged) == 0:
                    self._show_error_message('Report Generation', 'There are no privileged documents available.')
                    return 
                html_body = __gen_privileged_html_report(privileged)
            elif report_type == 'All':
                file_name = os.path.join(self._project_dir_path, file_type+REPORT_COMPLETE)   
                responsive = []
                privileged = []
                for fs in samples_lst: 
                    if fs[1] == 'Yes': 
                        responsive.append(fs)
                    if fs[2] == 'Yes': 
                        privileged.append(fs)
                html_body = __gen_complete_html_report(samples_lst, responsive, privileged)
            
            
            # Saves into a file path 
            __save_html_report(html_body, file_name)
            
            # Open the HTML report in the default web browser 
            webbrowser.open(file_name)
        except Exception,e:
            # Report generation failed 
            print e 
                    
        
    #********************************************* END Review Tab Handling *******************************************************  

    def _on_click_relevant_back(self, event):
        self._review_res.Destroy()
        self._current_page = 5
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def _on_click_irrelevant_back(self, event):
        self._review_unres.Destroy()
        self._current_page = 4
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def _on_click_sample_next( self, event ):
        self._review_res = TaggingControlSmarter(self._panel_review_res, self.sampled_files_responsive, 
                                                 self._rbx_response_res, 
                                                 self._tc_preview_tags, self._panel_doc_tag_res, 
                                                 self._get_relevancy_color)
        self._review_res._setup_review_tab('Relevant')
        self._current_page = 6
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def _on_click_show_report( self, event ):
        
        self.__setup_accuracy_grid()
        
        self._current_page = 7
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
    
    def _on_click_report_back_sample( self, event ):
        self._current_page = 6
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    def _on_click_report_exit( self, event ):
        self.__on_close()  
        
    def _btn_click_restart_search(self,event):
        self._current_page = 2
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
        
    def _on_click_export_files(self,event):
        import zipfile
        res_zip = zipfile.ZipFile(os.path.join(self._project_dir_path,"relevant.zip"),"w")
        
        for name in self._responsive_files:
            res_zip.write(name[0], os.path.basename(name[0]))
            
        unres_zip = zipfile.ZipFile(os.path.join(self._project_dir_path,"nonrelevant.zip"),"w")
        
        for name in self._unresponsive_files:
            unres_zip.write(name[0], os.path.basename(name[0]))
            
        unres_zip.close()
        dlg = wx.MessageDialog(self, "The relevant and non relevant files are zipped and can be found at location "+ self._project_dir_path, "Export files", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()

def main():
    
    '''
    The main function call 
    '''
    
    ex = wx.App()
    SMARTeR(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()

    
