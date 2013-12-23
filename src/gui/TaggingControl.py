'''
Created on Apr 22, 2013

@author: abhiramj
'''
import wx
import os
import webbrowser 
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from file_utils import get_destination_file_path

class TaggingControl ( wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, rs):
        
        wx.ListCtrl.__init__(self, parent , id = wx.ID_ANY, size = wx.Size( 315,270 ), style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.EXPAND)
        ListCtrlAutoWidthMixin.__init__(self)
        self.random_sampler = rs
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected)
        self.Bind(wx.EVT_LEFT_DCLICK, self._on_review_list_item_activated)
        self.Bind(wx.EVT_CONTEXT_MENU, rs.on_right_click_menu)
        self.Layout()
        
    def _setup_review_tab(self, sampled_files):
        '''
        This functions sets up the review tab 
        and its components 
        
        '''
        rs = self.random_sampler
        #if rs._lc_review_loaded: 
        #    return 
        
        # Sets the list control headers 
        
         
        if rs._lc_review_loaded==True:
            self.ClearAll()
            
        
        self.InsertColumn(0, '#', wx.LIST_FORMAT_CENTRE, width=30)
        self.InsertColumn(1, 'File Name', width=200)
        self.InsertColumn(2, 'Valid?', wx.LIST_FORMAT_CENTRE)
        #self.InsertColumn(3, 'Privileged', wx.LIST_FORMAT_CENTRE)
        rs._lc_review_loaded = True
        # Initializes from the shelf 
        
        samples_lst = rs.shelf['samples']
        file_id = 0
        for fs in samples_lst:
            self.InsertStringItem(file_id, str(file_id + 1))
            self.SetStringItem(file_id, 1, fs[1])
            self.SetStringItem(file_id, 2, fs[4])
            #self.SetStringItem(file_id, 3, fs[5])           
            file_id += 1            
        
    def _on_review_list_item_selected(self, event):
        
        # Gets the selected row's details 
        
        rs = self.random_sampler
        rs.selected_doc_id = self.GetFocusedItem()
        if rs.selected_doc_id < 0: return 
        
        responsive = self.GetItem(rs.selected_doc_id, 2)
        #privileged = self.GetItem(rs.selected_doc_id, 3)

        # Handles the document tags check boxes 
        
        if responsive.Text == 'Yes':
            rs._rbx_responsive.SetStringSelection('Valid')
        elif responsive.Text == 'No':
            rs._rbx_responsive.SetStringSelection('Invalid')
        elif responsive.Text == '':
            rs._rbx_responsive.SetStringSelection('Unknown')
            
        '''
        if privileged.Text == 'Yes':
            rs._rbx_privileged.SetStringSelection('Yes')
        elif privileged.Text == 'No':
            rs._rbx_privileged.SetStringSelection('No')
        elif privileged.Text == '':
            rs._rbx_privileged.SetStringSelection('Unknown')
        '''
        # Shows the tags panel 
        rs._panel_doc_tags.Show()
        rs._panel_doc_tags.GetParent().GetSizer().Layout()
        
        #Show the preview
        print_message = ''
        is_message_opened = False
        try:
            
            src_file_path = rs.sampled_files[rs.selected_doc_id]
            file_path = get_destination_file_path(rs.dir_path,rs._tempdir, src_file_path, rs.output_dir_path)
            _, fileExtension = os.path.splitext(file_path)
            if fileExtension=="" or fileExtension==".txt":
                with open(file_path,'r') as content:
                    print_message+=content.read()
                is_message_opened = True
        except Exception as anyException:
            is_message_opned = False;
            
        if is_message_opened:
            rs._tc_preview.SetValue(str(print_message))
        else:
            rs._tc_preview.SetValue('Preview is not available for this document.')
            
                

    def _on_review_list_item_activated(self, event):
        '''
        Handles the list control row double click event 
        
        '''
        # Gets the selected row's details 
        rs = self.random_sampler
        rs.selected_doc_id = self.GetFocusedItem()
        
        if rs.selected_doc_id < 0: return 
        
        responsive = self.GetItem(rs.selected_doc_id, 2)
        #privileged = self.GetItem(rs.selected_doc_id, 3)
        src_file_path = rs.sampled_files[rs.selected_doc_id]
        dest_file_path = get_destination_file_path(rs.dir_path,rs._tempdir, src_file_path, rs.output_dir_path)
        #print rs._tempdir+"\n"
        
        _, file_name = os.path.split(src_file_path)
        
        responsive_status = rs._rbx_responsive.GetStringSelection()
        privileged_status = rs._rbx_privileged.GetStringSelection()

   
        if os.path.exists(dest_file_path):
                  
            try:
                
                # Open a file
                webbrowser.open(dest_file_path)
                self.make_tag_popup(file_name,responsive_status, privileged_status)


            except Exception as anyException:
                pass
                print anyException
                #rs._show_error_message("Open File Error!", "The file could not be opened with the default application.")
        
        else: 
            rs._show_error_message("Open File Error!", "The file does not exist!")

    def make_tag_popup(self, file_name, responsive_status, privileged_status):
        # Creates a document tagging dialog 
                
            dlg = TagDocument(self, file_name, responsive_status, privileged_status)
            
            # Gets the tag selections from the dialog
            
            if dlg.ShowModal() == wx.ID_OK:
                responsive_status = dlg._rbx_responsive.GetStringSelection()  
                privileged_status = dlg._rbx_privileged.GetStringSelection()
                
                # Sets the selections to the parent window 

                self._rbx_responsive.SetStringSelection(responsive_status)
                if responsive_status == 'Valid': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'Yes')
                elif responsive_status == 'Invalid': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, 'No')
                elif responsive_status == 'Unknown': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 2, '')
                '''
                self._rbx_privileged.SetStringSelection(privileged_status)
                if privileged_status == 'Yes': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'Yes')
                elif privileged_status == 'No': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, 'No')
                elif privileged_status == 'Unknown': 
                    self._lc_review.SetStringItem(self.selected_doc_id, 3, '')
                ''' 
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
    
    def _on_click_clear_tags( self, event ):
        '''
        Clears the check box values 
        '''
        
        self._rbx_privileged.SetStringSelection("Unknown")
        self._rbx_responsive.SetStringSelection("Unknown")
        
        
#class PDFViewer(sc.SizedFrame):
#    def __init__(self, parent, **kwds):
#        super(PDFViewer, self).__init__(parent, **kwds)
#
#        paneCont = self.GetContentsPane()
#        self.buttonpanel = pdfButtonPanel(paneCont, wx.NewId(),
#                                wx.DefaultPosition, wx.DefaultSize, 0)
#        self.buttonpanel.SetSizerProps(expand=True)
#        self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition,
#                                wx.DefaultSize,
#                                wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
#        self.viewer.UsePrintDirect = ``False``
#        self.viewer.SetSizerProps(expand=True, proportion=1)
#
#        # introduce buttonpanel and viewer to each other
#        self.buttonpanel.viewer = self.viewer
#        self.viewer.buttonpanel = self.buttonpanel
#        
#    def load_file(self, file):
#        self.viewer.LoadFile(file)
