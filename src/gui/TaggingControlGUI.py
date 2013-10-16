import wx
import os
import webbrowser 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from file_utils import get_destination_file_path

class TaggingControlGUI ( wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, smt):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size( 420,200 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
        ListCtrlAutoWidthMixin.__init__(self)
        self.smarter = smt
        #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        #self.Bind(wx.EVT_LEFT_DCLICK, self._on_review_list_item_activated)
        #self.Bind(wx.EVT_CONTEXT_MENU, smt.on_right_click_menu)
        self._setup_review_tab("")
        self.Layout()
        
    def _setup_review_tab(self, sampled_files):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        smt = self.smarter
        #if rs._lc_review_loaded: 
        #    return 
        
        # Sets the list control headers 
        
         
        #if rs._lc_review_loaded==True:
        #    self.ClearAll()
            
        
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self.InsertColumn(1, 'File Name', width=200)
        self.InsertColumn(2, 'Responsive', wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(3, 'Privileged', wx.LIST_FORMAT_CENTRE)
        #rs._lc_review_loaded = True
