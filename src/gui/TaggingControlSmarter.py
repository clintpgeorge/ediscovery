
import wx
import os
import webbrowser 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from file_utils import get_destination_file_path

class TaggingControlSmarter ( wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, sm):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size( 420,200 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
        ListCtrlAutoWidthMixin.__init__(self)
        self.smarter = sm
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        #self.Bind(wx.EVT_LEFT_DCLICK, self._on_review_list_item_activated)
        #self.Bind(wx.EVT_CONTEXT_MENU, rs.on_right_click_menu)
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
        for fs in sm.ts_results:
            self.InsertStringItem(file_id, str(file_id + 1))
            self.SetStringItem(file_id, 1, fs[0])
            self.SetStringItem(file_id, 2, fs[2])           
            file_id += 1            
        
            
        
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
        sm = self.smarter
        selected_doc_id = self.GetFocusedItem()
        
        if selected_doc_id < 0: return 
        
        responsive = sm.ts_results[selected_doc_id][2]    
        # Handles the document tags check boxes 
        
        if responsive == 'Responsive':
            sm._rbx_responsive.SetSelection(0)
            sm.ts_results[selected_doc_id][2] = 'Responsive'
        elif responsive == 'Unresponsive':
            sm._rbx_responsive.SetSelection(1)
            sm.ts_results[selected_doc_id][2] = 'Unresponsive'
        else:
            sm._rbx_responsive.SetSelection(2)
            sm.ts_results[selected_doc_id][2] = ''
                         
        
        #Show the preview
        msg_text = ''
        is_message_opened = False
        src_file_path = sm.ts_results[selected_doc_id][1]
        _, fileExtension = os.path.splitext(src_file_path)
        if fileExtension=="" or fileExtension==".txt":
            import unicodedata
            with open(src_file_path) as fp:
                for line in fp:
                    msg_text = msg_text+line
                #msg_text = unicodedata.normalize('NFKD', msg_text).encode('ascii','ignore') # converts to ascii 
            is_message_opened = True
        
        if is_message_opened:
            sm._doc_feedback_preview.SetValue(str(msg_text))
        else:
            sm._doc_feedback_preview.SetValue('')
        