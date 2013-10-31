'''
Created on Oct 21, 2013

@author: Sail
'''

import wx
import os
import webbrowser 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from file_utils import get_destination_file_path

class TaggingControlSmarter ( wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, doc_list,responsive, privileged,preview,tags):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size( 420,200 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
        ListCtrlAutoWidthMixin.__init__(self)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_review_list_item_activated)
        #self.Bind(wx.EVT_CONTEXT_MENU, rs.on_right_click_menu)
        self._sampled_files=doc_list
        self._doc=doc_list
        self._rbx_responsive=responsive
        self._rbx_privileged=privileged
        self._tc_preview=preview
        self._panel_doc_tags=tags
        self.Layout()
        
    def _setup_review_tab(self):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        #if rs._lc_review_loaded: 
        #    return 
        
        # Sets the list control headers 
        
         
        #if rs._lc_review_loaded==True:
        #    self.ClearAll()
            
        
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self.InsertColumn(1, 'File Name', width=200)
        self.InsertColumn(2, 'Responsive', wx.LIST_FORMAT_CENTRE)
        self.InsertColumn(3, 'Privileged', wx.LIST_FORMAT_CENTRE)
        
        # Initializes from the shelf 
        
        
        file_id = 0
        
        for fs in self._doc:
            self.InsertStringItem(file_id, str(file_id + 1))
            self.SetStringItem(file_id, 1, fs[0])
            self.SetStringItem(file_id, 2, fs[1])
            self.SetStringItem(file_id, 3, fs[2])           
            file_id += 1            
        
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
        
       # rs = self.random_sampler
       
        self.selected_doc_id = self.GetFocusedItem()
        if self.selected_doc_id < 0: return 
        
        responsive = self.GetItem(self.selected_doc_id, 2)
        privileged = self.GetItem(self.selected_doc_id, 3)

        # Handles the document tags check boxes 
        
        if responsive.Text == 'Yes':
            self._rbx_responsive.SetStringSelection('Yes')
        elif responsive.Text == 'No':
            self._rbx_responsive.SetStringSelection('No')
        elif responsive.Text == '':
            self._rbx_responsive.SetStringSelection('Unknown')
            
        if privileged.Text == 'Yes':
            self._rbx_privileged.SetStringSelection('Yes')
        elif privileged.Text == 'No':
            self._rbx_privileged.SetStringSelection('No')
        elif privileged.Text == '':
            self._rbx_privileged.SetStringSelection('Unknown')
        
        # Shows the tags panel 
        self._panel_doc_tags.Show()
        self._panel_doc_tags.GetParent().GetSizer().Layout()
        
        #Show the preview
        print_message = ''
        is_message_opened = False
        try:
            
            src_file_path = self._doc[self.selected_doc_id][0]
            #file_path = get_destination_file_path(rs.dir_path,rs._tempdir, src_file_path, rs.output_dir_path)
            _, fileExtension = os.path.splitext(src_file_path)
            if fileExtension=="" or fileExtension==".txt":
                with open(src_file_path,'r') as content:
                    print_message+=content.read()
                is_message_opened = True
        except Exception as anyException:
            is_message_opned = False;
            
        if is_message_opened:
            try:
                self._tc_preview.SetValue(print_message)
            except:
                self._tc_preview.SetValue("File Encoding not supported. Double click to open.")
        else:
            self._tc_preview.SetValue('')
            
                

    def _on_review_list_item_activated(self, event):
        '''
        Handles the list control row double click event 
        
        '''
        # Gets the selected row's details 
        #rs = self.random_sampler
        self.selected_doc_id = self.GetFocusedItem()
        
        if self.selected_doc_id < 0: return 
        
        responsive = self.GetItem(self.selected_doc_id, 2)
        privileged = self.GetItem(self.selected_doc_id, 3)
        src_file_path = self._doc[self.selected_doc_id][0]
        
        #print rs._tempdir+"\n"
        
        _, file_name = os.path.split(src_file_path)
        
        responsive_status = self._rbx_responsive.GetStringSelection()
        privileged_status = self._rbx_privileged.GetStringSelection()

   
        if os.path.exists(src_file_path):
                  
            try:
                
                # Open a file
                webbrowser.open(src_file_path)
                self.make_tag_popup(file_name,responsive_status, privileged_status)


            except Exception as anyException:
                pass
                print anyException
                #self._show_error_message("Open File Error!", "The file could not be opened with the default application.")
        
        else: 
            self._show_error_message("Open File Error!", "The file does not exist!")

    def make_tag_popup(self, file_name, responsive_status, privileged_status):
        # Creates a document tagging dialog 
                
            dlg = TagDocument(self, file_name, responsive_status, privileged_status)
            
            # Gets the tag selections from the dialog
            
            if dlg.ShowModal() == wx.ID_OK:
                responsive_status = dlg._rbx_responsive.GetStringSelection()  
                privileged_status = dlg._rbx_privileged.GetStringSelection()
                
                # Sets the selections to the parent window 

                self._rbx_responsive.SetStringSelection(responsive_status)
                if responsive_status == 'Yes': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
                elif responsive_status == 'No': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
                elif responsive_status == 'Unknown': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, '')
                
                self._rbx_privileged.SetStringSelection(privileged_status)
                if privileged_status == 'Yes': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
                elif privileged_status == 'No': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
                elif privileged_status == 'Unknown': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, '')
                    
                self._is_rt_updated = True 
                
            # Destroys the dialog object 
            
            dlg.Destroy()    

    def GetListCtrl(self):
        return self
    
class TagDocument():
    '''
    Tag document custom dialog implementation 
    '''


    def __init__(self, parent, file_name, responsive, privileged):
        '''
        Constructor
        '''
        
        # Calls the parent class's method 
        
        super(TagDocument, self).__init__(parent) 
        
        # Sets the dialog controls based on the selected document value 
        
        self.SetTitle('Tag %s' % file_name)
        self._rbx_privileged.SetStringSelection(responsive)
        self._rbx_responsive.SetStringSelection(privileged)
        
        
    def _on_click_add_tags( self, event ):
        '''
        Returns the numeric code 'ID_OK' to caller
        '''
        
        self.EndModal(wx.ID_OK) 
        
    def _show_error_message(self, _header, _message):
        '''
        Shows error messages in a pop up 
        '''
        
        dlg = wx.MessageDialog(self, _message, _header, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()

    def _on_click_clear_tags( self, event ):
        '''
        Clears the check box values 
        '''
        
        self._rbx_privileged.SetStringSelection("Unknown")
        self._rbx_responsive.SetStringSelection("Unknown")        