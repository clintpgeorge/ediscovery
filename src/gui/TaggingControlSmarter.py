'''
Created on Oct 21, 2013

@author: Sail
'''

import wx
import os
import webbrowser 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class TaggingControlSmarter(wx.ListCtrl, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, review_docs, rbx_feedback, tc_preview, panel_tagging, get_row_color):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size(410, 160), style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.ALIGN_TOP)
        ListCtrlAutoWidthMixin.__init__(self)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_review_list_item_activated)
        #self.Bind(wx.EVT_CONTEXT_MENU, rs.on_right_click_menu)

        self._review_docs = review_docs
        self._rbx_feedback = rbx_feedback
        self._tc_preview = tc_preview
        self._panel_tagging = panel_tagging
        self._get_row_color = get_row_color
        
        self.Layout()
        
    def _setup_review_tab(self, feedback='Relevant'):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        # Sets the list control headers 
        
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self.InsertColumn(1, 'Document Name', width=200)
        self.InsertColumn(2, feedback, wx.LIST_FORMAT_CENTRE)
        
        # Add all documents to the list control 
        
        for row_id, fs in enumerate(self._review_docs):
            self.InsertStringItem(row_id, str(row_id + 1))
            self.SetStringItem(row_id, 1, fs[0])
            self.SetStringItem(row_id, 2, fs[1])
            self.SetItemBackgroundColour(row_id, self._get_row_color(fs[1]))           
          
        
    def __update_feedback(self, feedback_label):
        
        if feedback_label == 'Yes':
            self._rbx_feedback.SetSelection(0)
        elif feedback_label == 'No':
            self._rbx_feedback.SetSelection(1)
        elif feedback_label == 'Uncertain':
            self._rbx_feedback.SetSelection(2)
        else: 
            self._rbx_feedback.SetSelection(3)
            
        # Shows the tags panel 
        
        self._panel_tagging.Show()
        self._panel_tagging.GetParent().GetSizer().Layout()
            
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
       
        self.selected_doc_id = self.GetFocusedItem()
        if self.selected_doc_id < 0: return 
        
        feedback_label = self.GetItem(self.selected_doc_id, 2).Text
        selected_doc_path = self._review_docs[self.selected_doc_id][0]
        
        # Handles the document tags check boxes 
        
        self.__update_feedback(feedback_label)

        # Show the preview
        
        doc_text = ''
        try:
            _, fileExtension = os.path.splitext(selected_doc_path)
            if fileExtension == "" or fileExtension == ".txt":
                with open(selected_doc_path) as fp:
                    doc_text = fp.read()
        except:
            None 
            
        try:
            self._tc_preview.SetValue(doc_text)
        except:
            self._tc_preview.SetValue("Document encoding is not supported. Please double click on the document to open it in a system viewer.")
            
                

    def _on_review_list_item_activated(self, event):
        '''
        Handles the list control row double click event 
        
        '''
        # Gets the selected row's details 
        
        self.selected_doc_id = self.GetFocusedItem()
        if self.selected_doc_id < 0: return 
        feedback_label = self.GetItem(self.selected_doc_id, 2).Text
        
        # Handles the document tag radio buttons  
        
        self.__update_feedback(feedback_label)
        
        # Open the file in a system viewer 
        
        selected_doc_path = self._review_docs[self.selected_doc_id][0]
        if os.path.exists(selected_doc_path):
            try:
                
                webbrowser.open(selected_doc_path)
                # _, file_name = os.path.split(selected_doc_path)
                # self.make_tag_popup(file_name, feedback_label, privileged_status)
            except Exception as anyException:
                print anyException
                self._smarter._show_error_message("Open Document Error!", "The document could not be opened with the default application.")
        else: 
            self._smarter._show_error_message("Open Document Error!", "The selected document does not exist!")
            
            
            
            

#    def make_tag_popup(self, file_name, responsive_status, privileged_status):
#        # Creates a document tagging dialog 
#                
#            dlg = TagDocument(self, file_name, responsive_status, privileged_status)
#            
#            # Gets the tag selections from the dialog
#            
#            if dlg.ShowModal() == wx.ID_OK:
#                responsive_status = dlg._rbx_responsive.GetStringSelection()  
#                privileged_status = dlg._rbx_privileged.GetStringSelection()
#                
#                # Sets the selections to the parent window 
#
#                self._rbx_feedback.SetStringSelection(responsive_status)
#                if responsive_status == 'Yes': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
#                elif responsive_status == 'No': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
#                elif responsive_status == 'Unknown': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 2, '')
#                
#                self._rbx_privileged.SetStringSelection(privileged_status)
#                if privileged_status == 'Yes': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
#                elif privileged_status == 'No': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
#                elif privileged_status == 'Unknown': 
#                    self._lc_review.SetStringItem(self.selected_doc_id, 3, '')
#                    
#                self._is_rt_updated = True 
#                
#            # Destroys the dialog object 
#            
#            dlg.Destroy()    
#
#    def GetListCtrl(self):
#        return self
#    
#class TagDocument():
#    '''
#    Tag document custom dialog implementation 
#    '''
#
#
#    def __init__(self, parent, file_name, responsive, privileged):
#        '''
#        Constructor
#        '''
#        
#        # Calls the parent class's method 
#        
#        super(TagDocument, self).__init__(parent) 
#        
#        # Sets the dialog controls based on the selected document value 
#        
#        self.SetTitle('Tag %s' % file_name)
#        self._rbx_privileged.SetStringSelection(responsive)
#        self._rbx_feedback.SetStringSelection(privileged)
#        
#        
#    def _on_click_add_tags( self, event ):
#        '''
#        Returns the numeric code 'ID_OK' to caller
#        '''
#        
#        self.EndModal(wx.ID_OK) 
#        
#    def _show_error_message(self, _header, _message):
#        '''
#        Shows error messages in a pop up 
#        '''
#        
#        dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
#        dlg.ShowModal()
#
#    def _on_click_clear_tags( self, event ):
#        '''
#        Clears the check box values 
#        '''
#        
#        self._rbx_privileged.SetStringSelection("Unknown")
#        self._rbx_feedback.SetStringSelection("Unknown")        