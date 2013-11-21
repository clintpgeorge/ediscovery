import wx
import os
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin



class TaggingControlFeedback(wx.ListCtrl, ListCtrlAutoWidthMixin):
    '''
    This control handles the seed documents table in 
    the 'Document Feedback' tab   
    
    '''
    
    
    def __init__(self, parent, sm):
        
        wx.ListCtrl.__init__(self, parent, id = wx.ID_ANY, size = wx.Size( 600,200 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
        ListCtrlAutoWidthMixin.__init__(self)
        self.smarter = sm
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        self.Layout()
        
    def _setup_review_tab(self):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        sm = self.smarter
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=40)
        self.InsertColumn(1, 'Document Name', width=450)
        self.InsertColumn(2, 'Relevant', wx.LIST_FORMAT_CENTRE, width=60)

        for row_id, fs in enumerate(sm._seed_docs_details):
            self.InsertStringItem(row_id, str(row_id + 1))
            self.SetStringItem(row_id, 1, str(fs[2]))
            self.SetStringItem(row_id, 2, str(fs[3]))      
            self.SetItemBackgroundColour(row_id, sm._get_relevancy_color(fs[3]))     
        
            
        
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
        sm = self.smarter
        selected_row_id = self.GetFocusedItem()
        
        if selected_row_id < 0: return 
        
        is_relevant = sm._seed_docs_details[selected_row_id][3]  
        selected_doc_path = sm._seed_docs_details[selected_row_id][1]
        
        # Handles the document tags check boxes 
        
        if is_relevant == 'Yes':
            sm._rbx_doc_feedback.SetSelection(0)
        elif is_relevant == 'No':
            sm._rbx_doc_feedback.SetSelection(1)
        elif is_relevant == 'Uncertain':
            sm._rbx_doc_feedback.SetSelection(2)
        else:
            sm._rbx_doc_feedback.SetSelection(3)
                         
        
        # Show the preview of the selected file in the Text Window  

        msg_text = ''
        
        try:  
            file_extension = os.path.splitext(selected_doc_path)[1]
            if file_extension == "" or file_extension == ".txt":
                with open(selected_doc_path) as fp:
                    # TODO: fp.read() returns entire contents of the file; 
                    #       there will be a problem if the file is twice as 
                    #       large as the machine's memory
                    msg_text = fp.read()
        except: 
            print 'File open failed!' 

        sm._doc_feedback_preview.SetValue(msg_text)
            
        
            