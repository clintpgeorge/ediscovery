'''
Created on Feb 23, 2013

@author: cgeorge
'''
import sys 
import wx 
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from gui.SMARTeRGUI import SMARTeRGUI



###########################################################################
## Class SMARTeR
###########################################################################

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

packages = [('abiword', '5.8M', 'base'), ('adie', '145k', 'base'),
    ('airsnort', '71k', 'base'), ('ara', '717k', 'base'), ('arc', '139k', 'base'),
    ('asc', '5.8M', 'base'), ('ascii', '74k', 'base'), ('ash', '74k', 'base')]

###########################################################################
## Class SMARTeR
###########################################################################

class SMARTeR ( SMARTeRGUI ):
    
    def __init__( self, parent ):

        # Calls the parent class's method 
        super(SMARTeR, self).__init__(parent) 
        
        self._add_query_results_panel()

        self.Center()
        self.Show(True)
        
    def _on_menu_sel_exit( self, event ):
        super(SMARTeR, self)._on_menu_sel_exit(event) 
    
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
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
        self._lc_results.InsertColumn(0, 'Package', width=140)
        self._lc_results.InsertColumn(1, 'Size')
        self._lc_results.InsertColumn(2, 'Repository')

        for i in packages:
            index = self._lc_results.InsertStringItem(sys.maxint, i[0])
            self._lc_results.SetStringItem(index, 1, i[1])
            self._lc_results.SetStringItem(index, 2, i[2])

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


def main():
    '''
    The main function call 
    '''
    
    ex = wx.App()
    SMARTeR(None)
    ex.MainLoop()    


if __name__ == '__main__':
    
    main()
    



