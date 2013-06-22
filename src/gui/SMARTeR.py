'''
Created on Feb 23, 2013

@author: cgeorge
'''
import sys 
import wx 
import shelve
import os 
import mimetypes


from lucene import BooleanClause
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin,\
    ColumnSorterMixin
from gui.SMARTeRGUI import SMARTeRGUI, RatingControl, PreferencesDialog
from lucenesearch.lucene_index_dir import search_lucene_index, MetadataType, get_indexed_file_details
import re
import webbrowser
from const import NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS,\
    CHAR_LIMIT_IN_RESULTS_TAB_CELLS, SHELVE_CHUNK_SIZE, SHELVE_FILE_EXTENSION,\
    COLUMN_NUMBER_OF_RATING
from collections import OrderedDict
from utils.utils_file import read_config, load_file_paths_index, nexists
from tm.process_query import load_lda_variables, load_dictionary, \
    search_lda_model, load_lsi_variables, get_lda_query_td, \
    compute_topic_similarities
from const import SEARCH_RESULTS_LIMIT
from index_data import index_data


###########################################################################
# # This global dictionary is used to keep track of the query-results 
dictionary_of_rows = OrderedDict()

# Global variables to keep track of the chunk of results displayed
present_chunk = 0

# Constants 
SHELVE_DIR_NAME = 'shelf'
USER_RATINGS_CUT_OFF = 5 # TODO: this needs to be learned 

###########################################################################

###########################################################################
# # Class ResultsCheckListCtrl
###########################################################################

class ResultsCheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent_panel, parent_window):
        wx.ListCtrl.__init__(self, parent_panel, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_list_item_deselect)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_row_double_click)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_row_right_click)
        self._shelve_dir = ''
        self._parent_window = parent_window  
        
    def _set_table_headers(self):
        
        self.ClearAll()
        columnHeaders = MetadataType._types
        columnNumber = 0
        for c in columnHeaders:
            self.InsertColumn(columnNumber, c)
            columnNumber = columnNumber + 1
        self.InsertColumn(columnNumber, "file_id")
        self.InsertColumn(columnNumber+1, "file_score")
        self.InsertColumn(columnNumber+2, "rating")        
        
    
    def _set_shelve_dir(self, _dir_path):
        self._shelve_dir = _dir_path
    
    def _populate_results(self, chunk_number):
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
        
        # 1. Reads from that particular shelved-file
        shelve_file = shelve.open(os.path.join(self._shelve_dir, str(chunk_number)+SHELVE_FILE_EXTENSION))
        self.DeleteAllItems()
        global dictionary_of_rows
        dictionary_of_rows = OrderedDict()
        
        #print "Re-initialized dictionary = ", dictionary_of_rows
        for key in shelve_file.keys():
            row = shelve_file[key]
            # 2. Updates the dictionary_of_rows with this chunk of results
            dictionary_of_rows.__setitem__(key, row) 
        #print "Populated Dictionary from file: \n", dictionary_of_rows.keys()
        #print "Rows size = ", len( dictionary_of_rows.values()[0] )
        # 3. Sorts the dictionary_of_rows based on rating
        dictionary_sorted_as_list = sorted(dictionary_of_rows.items(), key=lambda (k, v): v[COLUMN_NUMBER_OF_RATING], reverse=True)
        keys = map(lambda (k,v): k, dictionary_sorted_as_list)
        values = map(lambda (k,v): v, dictionary_sorted_as_list)
        dictionary_of_rows = OrderedDict( zip(keys, values) )

        #print "Sorted Dictionary: \n", dictionary_of_rows.keys()
        #print "Rows size = ", len( dictionary_of_rows.values()[3] )
        
        # 4. Change all keys in the dictionary to correspond to row_numbers in the UI
        k_in_String = dictionary_of_rows.keys()
        k_in_ints = map(int, k_in_String)
        k = sorted(k_in_ints)
        v = dictionary_of_rows.values()
        dictionary_of_rows = OrderedDict( zip( map(str,k),v ) )
           
        # 5. Change all keys in the shelved-file to correspond to row_numbers in the UI
        for key, row in dictionary_of_rows.items():
            shelve_file[key] = row
        shelve_file.close()
        
        # 6. Displays the content in the RESULT tab of the UI
        items = dictionary_of_rows.items() 
        for key, row in items:
            index = self.InsertStringItem(sys.maxint, row[0])
            self.SetItemData(index, long(key))
            i = 0
            for cell in row:
                column_name = self.GetColumn(i).GetText()     
                cell = str(cell)        
                #Only the file_path is displayed completely.
                #The content of all other cells are restricted to 30 characters.                 
                if(column_name <> 'file_path') and len(cell) > CHAR_LIMIT_IN_RESULTS_TAB_CELLS:
                    self.SetStringItem(index, i, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
                else:
                    self.SetStringItem(index, i, cell)
                i += 1
        #self.Refresh()
    
    def _on_row_right_click(self,event):
        """Right-Clicking on a row to specify the search-relevancy of the file"""
        Rating(None,self,self._shelve_dir)
         
    def _on_row_double_click(self,event):
        focussed_item_index = self.GetFocusedItem()
        file_Name = self.GetItem(focussed_item_index,1)
        webbrowser.get().open(file_Name.GetText())
    
    def _on_list_item_select(self,event) :
        '''
        Handles the result list row select event 
        '''
        
        focussed_item_index = self.GetFocusedItem()
        file_name = self.GetItem(focussed_item_index, 1).GetText()
        _, file_ext = os.path.splitext(file_name)
        msg_text = 'Cannot open "%s" in this viewer! Please double click the row to open the file in a default system file viewer.' % file_name
        try: 
            if file_ext == '.txt' or file_ext == '':                
                with open(file_name) as fp:
                    msg_text = fp.read()            
            else:
                file_type, _ = mimetypes.guess_type(file_name, strict=True)
                msg_text = 'Cannot open "%s (type:%s)" in this viewer! Please double click the row to open the file in a default system file viewer.' % (file_name, file_type)
        except:
            pass             
            
        self._parent_window._tc_file_preview_pane.SetValue(msg_text)
    
    def _on_list_item_deselect(self,event) :
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
        
        #If the Relevance-recording window is opened again, it must show the score already given  
        relevance_score = checklist_control.GetItem(self.selected_record_index,COLUMN_NUMBER_OF_RATING)
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
        #print "Old rating = ", dictionary_of_rows[self.selected_record_index][-1]
        #print "New rating = ", rating
        
        selected_row_in_dict = present_chunk * SHELVE_CHUNK_SIZE + self.selected_record_index
        # 2. Stores this new rating in the dictionary
        dictionary_of_rows[str(selected_row_in_dict)][-1] = str(rating)

        shelve_file = shelve.open(os.path.join(self._shelve_dir, str(present_chunk)+ SHELVE_FILE_EXTENSION ) )
        row = shelve_file[str(selected_row_in_dict)]
        #print "Before SUBMIT : ", shelve_file[str(selected_row_in_dict)]
        row[-1] = str(rating)
        shelve_file[str(selected_row_in_dict)] = row
        #print "changed : ", shelve_file[str(selected_row_in_dict)] 
        shelve_file.close()
        
        self.checklist_control.itemDataMap = dictionary_of_rows
        self.Destroy()


###########################################################################
# # Class Preferences 
###########################################################################

class Preferences (PreferencesDialog):
    
    def __init__(self, parent):
        '''
        Calls the parent class's method 
        '''
        super(Preferences, self).__init__(parent) 
        
        self._parent = parent # refers to the parent object    
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

    def __init__(self, parent):

        # Calls the parent class's method 
        super(SMARTeR, self).__init__(parent) 
        self._is_lucene_index_available = False 
        self._is_tm_index_available = False
        self._current_page = 0
        
        self._shelve_dir = ''
        self._shelve_file_names = [] # this keeps all of the shelf files path 
        
        self._build_query_results_panel()
        self._populate_metadata_fields()
        self._reset_defaults_indexing_preferences()    
        
        self._lda_num_topics = self._num_topics     
        
        self.Center()
        self.Show(True)
        
    def _reset_defaults_indexing_preferences(self):
        
        self._num_topics = 50
        self._num_passes = 1
        self._min_token_freq = 1 
        self._min_token_len = 2
        

    def _on_menu_sel_preferences( self, event ):
        '''
        
        '''
        Preferences(parent = self)
        


    def _populate_metadata_fields(self):
        '''
        This function will populate the metadata combo box 
        dynamically at the time of file loading. This will help
        to accommodate new metadata types as and when they are needed. 
        '''
        meta_data_types = MetadataType._types
        self._cbx_meta_type.Append(MetadataType.ALL) # adds the all field to the combo box 
        for l in meta_data_types :
            self._cbx_meta_type.Append(l) 
        self._cbx_meta_type.SetSelection(0)


    def _build_query_results_panel(self):
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        _panel_left = wx.Panel(self._panel_query_results, -1)
        _panel_right = wx.Panel(self._panel_query_results, -1)

        self._st_file_preview_header = wx.StaticText(_panel_right, -1, 'File Review Pane (Text Files)')
        self._tc_file_preview_pane = wx.TextCtrl(_panel_right, -1, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(-1, 200))
        self._lc_results = ResultsCheckListCtrl(_panel_right, self)
        self._lc_results._set_table_headers() # Populate the column names using the metadata types from MetadataType_types &RB

       
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        self._btn_sel_all = wx.Button(_panel_left, -1, 'Select All', size=(100, -1))
        self._btn_desel_all = wx.Button(_panel_left, -1, 'Deselect All', size=(100, -1))
        self._btn_log_files = wx.Button(_panel_left, -1, 'Log', size=(100, -1))
        self._btn_load_next_chunk = wx.Button(_panel_left, -1, 'Next >', size=(100, -1))
        self._btn_load_previous_chunk = wx.Button(_panel_left, -1, '< Previous', size=(100, -1))
        self._btn_update_results = wx.Button(_panel_left, -1, 'Update Results', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self._on_click_sel_all, id=self._btn_sel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_desel_all, id=self._btn_desel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_log_files, id=self._btn_log_files.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_next, id=self._btn_load_next_chunk.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_previous, id=self._btn_load_previous_chunk.GetId())        
        self.Bind(wx.EVT_BUTTON, self._on_click_update_results, id=self._btn_update_results.GetId())  

        vbox2.Add(self._btn_sel_all, 0, wx.TOP, 5)
        vbox2.Add(self._btn_desel_all)
        vbox2.Add(self._btn_log_files)
        vbox2.Add(self._btn_load_next_chunk);
        vbox2.Add(self._btn_load_previous_chunk);
        vbox2.Add(self._btn_update_results);
        
        _panel_left.SetSizer(vbox2)

        vbox.Add(self._lc_results, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))
        vbox.Add(self._st_file_preview_header, 0.5, wx.EXPAND)
        vbox.Add((-1, 5))
        vbox.Add(self._tc_file_preview_pane, 0.5, wx.EXPAND)
        vbox.Add((-1, 10))

        _panel_right.SetSizer(vbox)

        hbox.Add(_panel_left, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(_panel_right, 1, wx.EXPAND)
        hbox.Add((3, -1))

        self._panel_query_results.SetSizer(hbox)



        
    def _on_menu_sel_exit(self, event):

        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()        
        
    def _on_notebook_page_changed( self, event ):
        '''
        Handles the note book page change event 
        '''
        
        self._current_page = event.Selection
        self._notebook.ChangeSelection(self._current_page)


        
    
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
        for key,row in items:
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
            os.remove( file_name ) 
        global num_of_chunks
        num_of_chunks = 0
    
    def _on_click_next(self,event):
        global present_chunk
        current_chunk = present_chunk;
        
        if(current_chunk <> num_of_chunks-1): 
            current_chunk += 1
            self._lc_results._populate_results(current_chunk)
            present_chunk = current_chunk
    
    def _on_click_previous(self,event):
        global present_chunk
        current_chunk = present_chunk;
        current_chunk -= 1
        if(current_chunk >= 0): 
            self._lc_results._populate_results(current_chunk)
            present_chunk = current_chunk    
    
    def _on_click_sel_all(self, event):
        num = self._lc_results.GetItemCount()
        for i in range(num):
            self._lc_results.CheckItem(i)

    def _on_click_desel_all(self, event):
        num = self._lc_results.GetItemCount()
        for i in range(num):
            self._lc_results.CheckItem(i, False)

    def _on_click_log_files(self, event):
#        num = self._lc_results.GetItemCount()
#        for i in range(num):
#            if i == 0: self._tc_files_log.Clear()
#            if self._lc_results.IsChecked(i):
#                self._tc_files_log.AppendText(self._lc_results.GetItemText(i) + '\n')
        pass 
    
    def _on_file_change_mdl(self, event):
        '''
        Handles the model file change event  
        '''
        
        file_name = self._file_picker_mdl.GetPath()
        self._load_model(file_name)

        if self._is_tm_index_available or self._is_lucene_index_available:
            self.SetStatusText("The %s model is loaded." % self.mdl_cfg['DATA']['name'])
        else: 
            self._show_error_message("Model Error", "Please select a valid model.")
            self._file_picker_mdl.SetPath("")
            self.mdl_cfg = None 
            
        
    def _load_model(self, model_cfg_file):
        '''
        Loads the models specified in the model configuration file  
        
        Arguments: 
            model_cfg_file - the model configuration file  
        
        '''
        
        self.mdl_cfg = read_config(model_cfg_file)
        
        self._shelve_dir = os.path.join( self.mdl_cfg['DATA']['project_dir'], SHELVE_DIR_NAME)
        if not os.path.exists(self._shelve_dir): 
            os.makedirs(self._shelve_dir)
        
        # Retrieve topic model file names 
        
        dictionary_file = self.mdl_cfg['CORPUS']['dict_file']
        path_index_file = self.mdl_cfg['CORPUS']['path_index_file']
        lda_mdl_file = self.mdl_cfg['LDA']['lda_model_file']
        lda_cos_index_file = self.mdl_cfg['LDA']['lda_cos_index_file']
        lda_num_topics = self.mdl_cfg['LDA']['num_topics']
#        lsi_mdl_file = self.mdl_cfg['LSI']['lsi_model_file']
#        lsi_cos_index_file = self.mdl_cfg['LSI']['lsi_cos_index_file']
        

        # Loads learned topic models and file details 
        if nexists(dictionary_file) and nexists(path_index_file):
                
            self.lda_file_path_index = load_file_paths_index(path_index_file)
            self.lda_dictionary = load_dictionary(dictionary_file)
            self.lda_num_files = len(self.lda_file_path_index)
            self.lda_vocab_size = len(self.lda_dictionary)        
            
            # loads LDA model details 
            if nexists(lda_mdl_file) and nexists(lda_cos_index_file): 
                self.lda_mdl, self.lda_index = load_lda_variables(lda_mdl_file, lda_cos_index_file)
                self._lda_num_topics = int(lda_num_topics)
                self._is_tm_index_available = True  
                self._tc_available_mdl.AppendText('[LDA] ')    
                    
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
            self._tc_available_mdl.AppendText('[LUCENE] ')  
         


        
        
    def _on_click_add_to_query(self, event):
        metadataSelected = self._cbx_meta_type.GetValue()
        queryBoxText = self._tc_query_input.GetValue()
        # Uncomment the below lines if it is decided that the conjunctions AND OR NOT should be there. 
        #if(self._rbtn_conjunction.Enabled) :
        #self._tc_query.AppendText(self._rbtn_compulsion_level.GetStringSelection() + " " + metadataSelected + ":" + queryBoxText + " ");
        #else :
        #self._tc_query.AppendText(metadataSelected + ":" + queryBoxText + ":");
        #    self._rbtn_conjunction.Enable()   
        self._tc_query.AppendText(metadataSelected + ":" + queryBoxText + ":" + self._rbtn_compulsion_level.GetStringSelection() + ' ')
    
    def _show_error_message(self, _header, _message):
        '''
        Shows error messages in a pop up 
        '''
        
        dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
    
    def _on_click_run_query(self, event):
        """
        Actions to be done when the "Run Query" button is clicked
        0. Validations 
        1. Parse the query
        2. Run Lucene query 
        3. Put the results to the dictionary_of_rows
        
        
        Note: According to our current logic we do search on the 
        lucene index to retrieve documents 
        """
        
#        facet_search = self._chbx_facet_search.GetValue()
#        topic_search = self._chbx_topic_search.GetValue()
#        
#        print facet_search, topic_search
        
        # 1. Parse the query
        
        global dictionary_of_rows
        dictionary_of_rows = OrderedDict()
        queryText = self._tc_query.GetValue().strip() 

        # 0. Validations 
        if not self._is_lucene_index_available:
            # Lucene index is mandatory 
            self._show_error_message('Run Query Error!', 'Please select a valid index for searching.')
            return  
#        elif not facet_search and not topic_search:
#            self._show_error_message('Run Query Error!', 'Please select a search type.')
#            return 
        elif queryText == '':
            self._show_error_message('Run Query Error!', 'Please enter a valid query.')
            return 
#        elif topic_search and not self._is_tm_index_available:
#            self._show_error_message('Run Query Error!', 'Topic model is not available for topic search.')
#            return 
#        elif facet_search and not self._is_lucene_index_available:
#            self._show_error_message('Run Query Error!', 'Lucene index is not available for facet search.')
#            return
        
        #queryText has Queries, Fields, BooleanClauses
        queries = []
        fields = []
        clauses = []
        filteredQuery = re.split(' ', queryText)
        
        for l in filteredQuery:
            res = re.split(':', l )
            print res 
            if len(res) > 1:
                fields.append(res[0])
                queries.append(res[1])
                if res[2] is 'MUST':
                    clauses.append(BooleanClause.Occur.MUST)
                elif res[2] is 'MUST_NOT':
                    clauses.append(BooleanClause.Occur.MUST_NOT)
                else:
                    clauses.append(BooleanClause.Occur.SHOULD)
        
        queryList = []
        queryList.append(queries)
        queryList.append(fields)
        queryList.append(clauses)

#        rows = [] 
#        fs_results = []
#        ts_results = [] 
        rows = search_lucene_index(self.lucene_index_dir, queryList, SEARCH_RESULTS_LIMIT)
        
#        if facet_search:
#            fs_results = search_lucene_index(self.lucene_index_dir, queryList, SEARCH_RESULTS_LIMIT)
#            
#        if topic_search: 
#            query_text = ' '.join(queries) # combines all the text in a query model 
#            ts_results = search_lda_model(query_text, self.lda_dictionary, self.lda_mdl, self.lda_index, self.lda_file_path_index, SEARCH_RESULTS_LIMIT)
#            ## ts_results are in this format  [doc_id, doc_dir_path, doc_name, score] 
#            ts_results = get_indexed_file_details(ts_results, self.lucene_index_dir) # grabs the files details from the index 
#            
#        if facet_search and not topic_search: 
#            # 2. Run Lucene query
#            rows = fs_results
#        elif not facet_search and topic_search: 
#            rows = ts_results
#        elif facet_search and topic_search: 
#            # Combine results  
#            rows = self._combine_lucene_tm_results(fs_results, ts_results)
            
        if len(rows) == 0: 
            self.SetStatusText('No documents found.')
            return 
        
        # 3. Put the results to the dictionary_of_rows
        
        key = 0 
        for row in rows:
            # file_id = row[9] # key is obtained from the lucene index
            # print retrieve_document_details(file_id, self.lucene_index_dir).get('email_subject')
            file_details = row # values of the defined MetadataTypes 
            file_details.append('0') # Add a 'relevance' value of '0' to each search-result
        
            dictionary_of_rows.__setitem__(str(key), file_details)
            key += 1
            

        self._lc_results._set_shelve_dir(self._shelve_dir)
        self._lc_results.itemDataMap = dictionary_of_rows
        self._lc_results.Bind(wx.EVT_LIST_COL_CLICK, self._lc_results._on_header_column_click)

        
        items = dictionary_of_rows.items()
        self._reset_persistent_shelves()
        self._create_persistent_shelves(items)
        global present_chunk
        present_chunk = 0
        self._lc_results._populate_results(present_chunk)
        self._tc_file_preview_pane.SetValue('')
        
        
        # Goes to the results tab 
        self._current_page = 2
        self._notebook.ChangeSelection(self._current_page)
        self.SetStatusText('')
        
    
    def _on_click_update_results( self, event ):
        '''
        This function incorporates the user ratings into 
        the ranked list. Here, we combine the highly rated 
        documents, represent it in topic modeling space, 
        and search for similar documents.  
        
        ''' 
        
        # step 1: gets highly rated documents 
        
        
        selected_docs = []  
        excluded_docs = []
        
        for shelf_file_name in self._shelve_file_names:
            sd = shelve.open(shelf_file_name)
            for k in sd.keys():
                row = sd[k]
                if int(row[-1]) > USER_RATINGS_CUT_OFF:
                    selected_docs.append(row) 
                else: 
                    excluded_docs.append(row) 
            sd.close()
            
        # step 2: combine all email bodies to a single document 
        # row index 5 is for the body field 
        
        bag_of_words = ''
        for sdoc in selected_docs:
            bag_of_words += sdoc[5]
        
        # bag_of_words_td = get_lda_query_td(bag_of_words, self.lda_dictionary, self.lda_mdl)
        
        # step 3: compute the distances between bag_of_words and 
        # all other documents 
        
        excluded_docs = compute_topic_similarities(bag_of_words, selected_docs + excluded_docs, self.lda_dictionary, self.lda_mdl, self._lda_num_topics)
        
        
        # TODO: need to figure out a good way to combine topic modeling 
        #       similarity score and lucene scores      
        
        
        
            
        
        
        
    
    

        
    
      
    def _on_click_index_data( self, event ):
        '''
        Handles the data folder files' indexing and topic modeling 
         
         
        TODO: 
            1. validations to be done 
        
        '''
        
        project_name = self._tc_project_name.GetValue()
        data_folder = self._data_dir_picker.GetPath()
        output_folder = self._application_dir_picker.GetPath()
        
        # print project_name, data_folder, output_folder, self._num_topics, self._num_passes, self._min_token_freq, self._min_token_len
        
        index_data(data_folder, output_folder, project_name, self._num_topics, self._num_passes, self._min_token_freq, self._min_token_len, log_to_file=True)

        # TODO need to show a status bar with execution status 
        
        
    def _on_click_clear_project_details(self, event):
        '''
        Clears the project details 
        
        '''
        
        self._tc_project_name.SetValue('')
        self._data_dir_picker.SetPath('')
        self._application_dir_picker.SetPath('')
        
        

    
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
        
def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    SMARTeR(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()

    