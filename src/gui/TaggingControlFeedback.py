import wx
import os
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin



class TaggingControlFeedback(wx.ListCtrl, ListCtrlAutoWidthMixin):
    '''
    This control handles the seed documents table in 
    the 'Document Feedback' tab   
    
    '''
    
    
    def __init__(self, parent, sm):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size( 420,200 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
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
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self.InsertColumn(1, 'File Name', width=200)
        self.InsertColumn(2, 'Responsive', wx.LIST_FORMAT_CENTRE)
        #self.InsertColumn(3, 'Privileged', wx.LIST_FORMAT_CENTRE)
        #rs._lc_review_loaded = True
        # Initializes from the shelf 
        
        #samples_lst = rs.shelf['samples']
        file_id = 0
        for fs in sm._seed_docs_details:
            self.InsertStringItem(file_id, str(file_id + 1))
            self.SetStringItem(file_id, 1, str(fs[2]))
            self.SetStringItem(file_id, 2, str(fs[4]))           
            file_id += 1            
        
            
        
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
        sm = self.smarter
        selected_doc_id = self.GetFocusedItem()
        
        if selected_doc_id < 0: return 
        
        responsive = sm._seed_docs_details[selected_doc_id][4]    
        
        # Handles the document tags check boxes 
        # TODO: Need to verify whether the following 
        # code snippet is necessary 
        
        if responsive == 'Yes':
            sm._rbx_responsive.SetSelection(0)
            sm._seed_docs_details[selected_doc_id][4] = 'Yes'
            sm._doc_true_class_ids[selected_doc_id] = sm.RESPONSIVE_CLASS_ID
        elif responsive == 'No':
            sm._rbx_responsive.SetSelection(1)
            sm._seed_docs_details[selected_doc_id][4] = 'No'
            sm._doc_true_class_ids[selected_doc_id] = sm.UNRESPONSIVE_CLASS_ID
        else:
            sm._rbx_responsive.SetSelection(2)
            sm._seed_docs_details[selected_doc_id][4] = ''
            sm._doc_true_class_ids[selected_doc_id] = sm.NEUTRAL_CLASS_ID
                         
        
        # Show the preview of the selected file in the Text Window  

        msg_text = ''
        is_message_opened = False
        
        try:  
            src_file_path = sm._seed_docs_details[selected_doc_id][1]
            file_extension = os.path.splitext(src_file_path)[1]
            if file_extension == "" or file_extension == ".txt":
                with open(src_file_path) as fp:
                    # TODO: fp.read() returns entire contents of the file; 
                    #       there will be a problem if the file is twice as 
                    #       large as the machine's memory
                    msg_text = fp.read()
                is_message_opened = True
        except: 
            print 'File open failed!' 
        
        if is_message_opened:
            sm._doc_feedback_preview.SetValue(msg_text)
        else:
            sm._doc_feedback_preview.SetValue('')
            
            