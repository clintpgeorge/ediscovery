'''
Created on Feb 23, 2013

@author: cgeorge
'''
import sys 
import wx 
import lucenesearch
from lucene import BooleanClause
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from gui.SMARTeRGUI import SMARTeRGUI
from lucenesearch.lucene_index_dir import search_for_query, MetadataType
import re
import webbrowser


###########################################################################
# # Class SMARTeR
###########################################################################

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDeSelect)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        
    def  OnDoubleClick(self,event):
        focussed_item_index = self.GetFocusedItem()
        file_Name = self.GetItem(focussed_item_index,1)
        webbrowser.get().open(file_Name.GetText())
    def OnSelect(self,event) :
        pass
    def OnDeSelect(self,event) :
        pass
    packages = [('abiword', '5.8M', 'base'), ('adie', '145k', 'base'),
    ('airsnort', '71k', 'base'), ('ara', '717k', 'base'), ('arc', '139k', 'base'),
    ('asc', '5.8M', 'base'), ('ascii', '74k', 'base'), ('ash', '74k', 'base')]

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
            self._lc_results.InsertColumn(columnNumber, ''+c )
            columnNumber = columnNumber + 1
        
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


        self.Bind(wx.EVT_BUTTON, self._on_click_sel_all, id=self._btn_sel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_desel_all, id=self._btn_desel_all.GetId())
        self.Bind(wx.EVT_BUTTON, self._on_click_log_files, id=self._btn_log_files.GetId())
        

        vbox2.Add(self._btn_sel_all, 0, wx.TOP, 5)
        vbox2.Add(self._btn_desel_all)
        vbox2.Add(self._btn_log_files)

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
    
    def _populate_query_results(self, rows):
        for r in rows:
            index = self._lc_results.InsertStringItem(sys.maxint, r[0])
            i = 0
            for cell in r:
                column_name = self._lc_results.GetColumn(i).GetText()
                if(column_name is not 'file_path'):
                    self._lc_results.SetStringItem(index, i, cell[:20])
                else: 
                    self._lc_results.SetStringItem(index, i, cell)
                i = i + 1
            
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
        #Actions to be done when the "Run Query" button is clicked
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
        
        #searchResults = lucene_search("/home/rahul/workspace/SelectedMails/lucene", 1000, queryText)
        lucene_index_dir = self.root_dir_from_model +"/lucene"
        rows = search_for_query(lucene_index_dir, queryList)
        self._populate_query_results(rows)
        #print searchResults
        
   
        
        
def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    SMARTeR(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()

    