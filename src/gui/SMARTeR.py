'''
Created on Feb 23, 2013

@author: cgeorge
'''
import sys 
import wx 
import lucenesearch
import gui
from lucene import BooleanClause
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin,\
    ColumnSorterMixin
from gui.SMARTeRGUI import SMARTeRGUI,RatingControl
from lucenesearch.lucene_index_dir import search_for_query, MetadataType
import re
import webbrowser
from const import NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS,\
    CHAR_LIMIT_IN_RESULTS_TAB_CELLS, SHELVE_CHUNK_SIZE, SHELVE_FILE_EXTENSION
from mako.runtime import _populate_self_namespace
from collections import OrderedDict
import shelve

###########################################################################
# # This global dictionary is used to keep track of the query-results 
dictionary_of_rows = OrderedDict()

# Global variables to keep track of the chunk of results displayed
present_chunk = 0
###########################################################################

###########################################################################
# # Class SMARTeR
###########################################################################

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, NUMBER_OF_COLUMNS_IN_UI_FOR_EMAILS)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeSelect)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.onRightClick)
    
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
        # 1. Reads from that particular shelved-file
        shelve_file = shelve.open(str(chunk_number)+SHELVE_FILE_EXTENSION)
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
        dictionary_sorted_as_list = sorted(dictionary_of_rows.items(), key=lambda (k, v): v[9], reverse=True)
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
                #Only the file_path is displayed completely.
                #The content of all other cells are restricted to 30 characters.                 
                if(column_name <> 'file_path'):
                    #if(type(cell) is not int):
                    self.SetStringItem(index, i, cell[:CHAR_LIMIT_IN_RESULTS_TAB_CELLS])
                else:
                    self.SetStringItem(index, i, cell)
                i = i + 1
        #self.Refresh()
    
    def onRightClick(self,event):
        """Right-Clicking on a row to specify the search-relevancy of the file"""
        #print "Right Click called .... "
        Rating(None,self)
         
    def  OnDoubleClick(self,event):
        focussed_item_index = self.GetFocusedItem()
        file_Name = self.GetItem(focussed_item_index,1)
        webbrowser.get().open(file_Name.GetText())
    
    def OnSelect(self,event) :
        pass
    
    def OnDeSelect(self,event) :
        pass
    
    def GetListCtrl(self):
        return self
    
    def OnColClick(self, event):
        """
        This method is used to sort the rows in the RESULTS CheckListCtrl
        """
        ''' Have commented the below block since 'sorting' has been implemented
            inside the populate_results
        
            #self.itemDataMap = dictionary_of_rows
            oldCol = self._col
            self._col = col = event.GetColumn()
            print "Clicked on column ", self._col
            #self._colSortFlag[col] = int(not self._colSortFlag[col])
            #self.GetListCtrl().SortItems(self.GetColumnSorter        
            #self.SortListItems(col, 0)  # 0 => descending order        
            # Once the contents of the listCtrl are sorted, update the dictionary too (to preserve the order)        
            #print dictionary_of_rows.keys()
            
            if col == 9: # 9 is the column number of Rating
                global dictionary_of_rows
                dictionary_sorted_as_list = sorted(dictionary_of_rows.items(), key=lambda (k, v): v[9], reverse=True)
                keys = map(lambda (k,v): k, dictionary_sorted_as_list)
                values = map(lambda (k,v): v, dictionary_sorted_as_list)
                dictionary_of_rows = OrderedDict( zip(keys, values) )
                
                print dictionary_of_rows.keys()
                ratings = []
                for v in dictionary_of_rows.values():
                    ratings.append(v[9])
                print ratings
                # Must now rewrite the shelved-file-chunk with the sorted dictionary_of_rows
                items = dictionary_of_rows.items()
                
                fileName = str(present_chunk)
                fileName = fileName + SHELVE_FILE_EXTENSION
                shelve_file = shelve.open(fileName)
                # First, delete the contents of the shelved-file
                for key,value in items:
                    print "Deleting key = ", key
                    del shelve_file[str(key)]
                # Then fill the file with the sorted dictionary contents
                for key,row in items:
                    shelve_file[str(key)] = row;
                shelve_file.close()
                
                self._populate_results(present_chunk)
                self.Refresh()
        '''
        
        # For now, just call _populate_results since it internally does the sorting 
        self._populate_results(present_chunk)
        
    packages = [('abiword', '5.8M', 'base'), ('adie', '145k', 'base'),
    ('airsnort', '71k', 'base'), ('ara', '717k', 'base'), ('arc', '139k', 'base'),
    ('asc', '5.8M', 'base'), ('ascii', '74k', 'base'), ('ash', '74k', 'base')]

###########################################################################
# # Class Rating
###########################################################################

class Rating (RatingControl):
    selected_record_index = None
    checklist_control = None
    column_index_of_rating = 9
    
    def __init__(self, parent, checklist_control):
        """ Calls the parent class's method """ 
        super(Rating, self).__init__(parent) 
        self.Center()
        self.Show(True)
        self.checklist_control = checklist_control
        self.selected_record_index = checklist_control.GetFocusedItem()
        #print self.selected_record_index
        
        #If the Relevance-recording window is opened again, it must show the score already given  
        relevance_score = checklist_control.GetItem(self.selected_record_index,self.column_index_of_rating)
        self.radio_control.SetSelection( int(relevance_score.GetText()) )
        
    def _on_btn_click_submit(self, event):
        """
        1. Updates the Relevance column with the given rating
        2. Stores this new rating in the dictionary
        3. Stores this new rating in the shelved-file
        """

        # 1. Updates the Relevance column with the given rating
        rating = self.radio_control.GetSelection()
        self.checklist_control.SetStringItem(self.selected_record_index,self.column_index_of_rating, str(rating))
        
        # Statements to just debug
        #print "Old rating = ", dictionary_of_rows[self.selected_record_index][-1]
        #print "New rating = ", rating
        
        selected_row_in_dict = present_chunk * SHELVE_CHUNK_SIZE + self.selected_record_index
        # 2. Stores this new rating in the dictionary
        dictionary_of_rows[str(selected_row_in_dict)][-1] = str(rating)

        shelve_file = shelve.open( str(present_chunk)+ SHELVE_FILE_EXTENSION )
        row = shelve_file[str(selected_row_in_dict)]
        #print "Before SUBMIT : ", shelve_file[str(selected_row_in_dict)]
        row[-1] = str(rating)
        shelve_file[str(selected_row_in_dict)] = row
        #print "changed : ", shelve_file[str(selected_row_in_dict)] 
        shelve_file.close()
        
        self.checklist_control.itemDataMap = dictionary_of_rows
        self.Destroy()


###########################################################################
# # Class SMARTeR
###########################################################################

class SMARTeR (SMARTeRGUI):
    root_dir_from_model = None
    def __init__(self, parent):

        # Calls the parent class's method 
        super(SMARTeR, self).__init__(parent) 
        
        self._add_query_results_panel()
        self._populate_comboBox()
        self.Center()
        self.Show(True)
    '''
    This function will populate the metadata combo box 
    dynamically at the time of file loading. This will help
    to accommodate new metadata types as and when they are needed. 
    '''
    def _populate_comboBox(self):
        metaDataTypes = MetadataType._types
        for l in metaDataTypes :
            self._cbx_meta_type. Append(l) 
        
    def _on_menu_sel_exit(self, event):
        super(SMARTeR, self)._on_menu_sel_exit(event) 
    
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()        
        
        
    def _add_query_results_panel(self):
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        _panel_left = wx.Panel(self._panel_query_results, -1)
        _panel_right = wx.Panel(self._panel_query_results, -1)

        self._tc_files_log = wx.TextCtrl(_panel_right, -1, style=wx.TE_MULTILINE, size=(-1, 100))
        self._lc_results = CheckListCtrl(_panel_right)
        
        '''
        self._lc_results.InsertColumn(0, 'Package', width=140)
        self._lc_results.InsertColumn(1, 'Size')
        self._lc_results.InsertColumn(2, 'Repository')
        '''
        
        # Populate the column names using the metadata types from MetadataType_types &RB
        columnHeaders = MetadataType._types
        columnNumber = 0
        for c in columnHeaders:
            self._lc_results.InsertColumn(columnNumber,c )
            columnNumber = columnNumber + 1
        self._lc_results.InsertColumn(columnNumber,"rating")
        
        '''
        # Commented the below lines so that results can be populated AFTER the search         
        for i in packages:
            index = self._lc_results.InsertStringItem(sys.maxint, i[0])
            self._lc_results.SetStringItem(index, 1, i[1])
            self._lc_results.SetStringItem(index, 2, i[2])
        '''
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        self._btn_sel_all = wx.Button(_panel_left, -1, 'Select All', size=(100, -1))
        self._btn_desel_all = wx.Button(_panel_left, -1, 'Deselect All', size=(100, -1))
        self._btn_log_files = wx.Button(_panel_left, -1, 'Log', size=(100, -1))
        self._btn_load_next_chunk = wx.Button(_panel_left, -1, 'Next >', size=(100, -1))
        self._btn_load_previous_chunk = wx.Button(_panel_left, -1, '< Previous', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self._on_click_sel_all, id=self._btn_sel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_desel_all, id=self._btn_desel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_log_files, id=self._btn_log_files.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_next, id=self._btn_load_next_chunk.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_previous, id=self._btn_load_previous_chunk.GetId())        

        vbox2.Add(self._btn_sel_all, 0, wx.TOP, 5)
        vbox2.Add(self._btn_desel_all)
        vbox2.Add(self._btn_log_files)
        vbox2.Add(self._btn_load_next_chunk);
        vbox2.Add(self._btn_load_previous_chunk);
        
        _panel_left.SetSizer(vbox2)

        vbox.Add(self._lc_results, 1, wx.EXPAND | wx.TOP, 3)
        vbox.Add((-1, 10))
        vbox.Add(self._tc_files_log, 0.5, wx.EXPAND)
        vbox.Add((-1, 10))

        _panel_right.SetSizer(vbox)

        hbox.Add(_panel_left, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(_panel_right, 1, wx.EXPAND)
        hbox.Add((3, -1))

        self._panel_query_results.SetSizer(hbox)
    
    def _create_persistent_shelves(self,items):
        """
            Stores the query-results into shelves. 
            *** Currently, the shelved files are named chunkNumber.shelve ***
            *** Come up with a logic to name files so that they represent 
                the query string
            ***
        """
        chunk_number = -1;
        shelve_file = None
        for key,row in items:
            if(int(key) % SHELVE_CHUNK_SIZE == 0):
                chunk_number = chunk_number + 1 
                fileName = str(chunk_number)
                fileName = fileName + SHELVE_FILE_EXTENSION
                if shelve_file is not None: 
                    shelve_file.close()
                shelve_file = shelve.open(fileName)
            shelve_file[str(key)] = row;
        global num_of_chunks
        num_of_chunks = chunk_number+1
        shelve_file.close()
    
    def _on_click_next(self,event):
        global present_chunk
        current_chunk = present_chunk;
        
        if(current_chunk <> num_of_chunks -1): 
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
        num = self._lc_results.GetItemCount()
        for i in range(num):
            if i == 0: self._tc_files_log.Clear()
            if self._lc_results.IsChecked(i):
                self._tc_files_log.AppendText(self._lc_results.GetItemText(i) + '\n')
    
    def _on_file_change_mdl(self, event):
        fileName = self._file_picker_mdl.GetPath()
        pattern = re.compile('\[.+\]')
        fileInstance = open(fileName)
        matchedList = [];
        
        for line in fileInstance :
            firstList = pattern.findall(line);
            for word in firstList :
                matchedList.append(word)
        
        while(matchedList.__len__() > 0) : 
            value = matchedList.pop()
            if(value != '[DATA]') :
                self._tc_available_mdl.AppendText(value)
        
        fileInstance = open(fileName)
        for line in fileInstance :
            filesDir = re.search(r'(files_dir=)(.*)',line)
            if filesDir is not None:
                self.root_dir_from_model = filesDir.group(2)
        
        
    def _on_click_add_to_query(self, event):
        metadataSelected = self._cbx_meta_type.GetValue()
        queryBoxText = self._tc_query_input.GetValue()
        # Uncomment the below lines if it is decided that the conjunctions AND OR NOT should be there. 
        #if(self._rbtn_conjunction.Enabled) :
        #self._tc_query.AppendText(self._rbtn_compulsion_level.GetStringSelection() + " " + metadataSelected + ":" + queryBoxText + " ");
        #else :
        #self._tc_query.AppendText(metadataSelected + ":" + queryBoxText + ":");
        #    self._rbtn_conjunction.Enable()   
        self._tc_query.AppendText(metadataSelected + ":" + queryBoxText + ":" + self._rbtn_compulsion_level.GetStringSelection()+ ' ')
    
    def _on_click_run_query(self, event):
        """
        Actions to be done when the "Run Query" button is clicked
        1. Parse the query
        2. Run Lucene query 
        3. Put the results to the dictionary_of_rows
        """

        # 1. Parse the query
        
        global dictionary_of_rows
        queryText = self._tc_query.GetValue() #'email_body:senorita:MUST'
        #queryTest has Queries, Fields, BooleanClauses
        queries = []
        fields = []
        clauses = []
        filteredQuery = re.split(' ', queryText)
        
        for l in filteredQuery:
            res = re.split(':', l )
            if len(res) > 1:
                fields.append(res[0])
                queries.append(res[1])
                if res[2] is 'MUST':
                    clauses.append(BooleanClause.Occur.MUST)
                elif res[2] is 'MUST_NOT':
                    clauses.append(BooleanClause.Occur.MUST_NOT)
                else:
                    clauses.append(BooleanClause.Occur.SHOULD)
        
        #print 'Clauses is\n',clauses
        
        queryList = []
        queryList.append(queries)
        queryList.append(fields)
        queryList.append(clauses)
        
        # 2. Run Lucene query         
        lucene_index_dir = self.root_dir_from_model +"/lucene"
        rows = search_for_query(lucene_index_dir, queryList)

        # 3. Put the results to the dictionary_of_rows
        key = 0
        for r in rows:
            # Add a 'relevance' value of '0' to each search-result
            r.append('0')
            dictionary_of_rows.__setitem__(str(key), r)
            key = key + 1
        #print "---------------------------\n", rows, "\n---------------\n"

        self._lc_results.itemDataMap = dictionary_of_rows
        self._lc_results.Bind(wx.EVT_LIST_COL_CLICK, self._lc_results.OnColClick)

        items = dictionary_of_rows.items()
        self._create_persistent_shelves(items)
        global present_chunk
        present_chunk = 0
        self._lc_results._populate_results(present_chunk)
        
def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    SMARTeR(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()

    