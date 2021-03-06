timport wx
import os
import tempfile
from wx.lib.masked import NumCtrl
from file_utils import find_files_in_folder, copy_files_with_dir_tree
from sampler.random_sampler import random_sampler, SUPPORTED_CONFIDENCES, DEFAULT_CONFIDENCE_INTERVAL, DEFAULT_CONFIDENCE_LEVEL
from gui.file_list_control import file_list_control
from decimal import Decimal

class RandomSamplerGUI(wx.Frame):
    
    def __init__(self, parent):
        
        wx.Frame.__init__(self, parent)        
        
        self.dir_path = tempfile.gettempdir() # a cross-platform way of getting the path to the temp directory
        self.output_dir_path = tempfile.gettempdir()
        self.confidence_val = 0.75
        self.precision_val = 0.01
        self.SEED = 2013 

        # Setting up the menu.
        
        self._create_menu_bar()


        # Sets the banner text 
        
        banner_text = """Random sampler: 
        This application randomly samples the files given in the input directory 
        and copies them to the output directory. The sample size is calculated by 
        the given confidence interval."""
        self.banner = wx.StaticText(self, id=wx.ID_ABOUT, label=banner_text, style=wx.TE_AUTO_SCROLL)
        
        # A Status bar in the bottom of the window
        
        self.CreateStatusBar() 
        
        # Layout sizers

        self._create_layout()
        
        # Handles the basic window events 
        
        self.Bind(wx.EVT_CLOSE, self._on_exit)

        # Sets the main window properties 
        self.SetTitle('Random Sampler')
        self.Center()
        self.SetSize((800,600))
        self.Show(True)


                            

    def _create_layout(self):
        '''Creates the main window layout
        '''
        
        # Input folder section
        self.input_folder_label = wx.StaticText(self, label="Data folder")
        self.input_folder_control = wx.TextCtrl(self, style=wx.TE_BESTWRAP, size=(400, -1))
        self.input_folder_control.SetEditable(False)
        self.input_folder_control.SetValue(self.dir_path)
        self.input_folder_button = wx.Button(self, wx.ID_OPEN, "Select")
        self.Bind(wx.EVT_BUTTON, self._on_select_input_folder, self.input_folder_button)
        self.line = wx.StaticLine(self)
        
        # Setting output folder section
        self.output_folder_label = wx.StaticText(self, label="Sampled output")
        self.output_folder_control = wx.TextCtrl(self, style=wx.TE_BESTWRAP, size=(400, -1))
        self.output_folder_control.SetEditable(False)
        self.output_folder_control.SetValue(self.output_dir_path)
        self.output_folder_button = wx.Button(self, wx.ID_ANY, "Select")
        self.Bind(wx.EVT_BUTTON, self._on_select_output_folder, self.output_folder_button)
        
        # Setting run and exit buttons
        self.button_exit = wx.Button(self, wx.ID_EXIT, "Exit")
        self.button_run = wx.Button(self, wx.ID_ANY, "Run Sampler")        
        self.Bind(wx.EVT_BUTTON, self._on_exit, self.button_exit)
        self.Bind(wx.EVT_BUTTON, self._on_run_sampler, self.button_run)
        
        # Setting parameters
        self.confidence_text = wx.StaticText(self, label="Confidence Level (%)")
        self.precision_text = wx.StaticText(self, label="Confidence Interval (%)")
        
        confidence_levels = ['%.3f' % (w * Decimal('100')) for w in  SUPPORTED_CONFIDENCES.keys()]
        confidence_levels.sort()
        self.confidence = wx.ComboBox(self, -1, str(DEFAULT_CONFIDENCE_LEVEL), size=(150, -1), choices=confidence_levels, style=wx.CB_READONLY) 
        self.precision = wx.lib.masked.NumCtrl(self, size=(20,1), fractionWidth=0, integerWidth=2, allowNegative=False, min=1, max=99, value=DEFAULT_CONFIDENCE_INTERVAL) 

        # Layouts 
        sizer_input_output = wx.GridBagSizer(2,2)
        sizer_input_output.Add(self.input_folder_label,pos = (0,0), flag =  wx.ALIGN_LEFT | wx.ALL, border=5 )
        sizer_input_output.Add(self.input_folder_control,pos = (0,1), flag = wx.EXPAND | wx.ALL, border=5)
        sizer_input_output.Add(self.input_folder_button,pos = (0,2), flag = wx.EXPAND | wx.ALL, border=5)
        sizer_input_output.Add(self.output_folder_label,pos = (1,0), flag = wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=5)
        sizer_input_output.Add(self.output_folder_control,pos = (1,1), flag = wx.EXPAND | wx.ALL, border=5)
        sizer_input_output.Add(self.output_folder_button,pos = (1,2), flag = wx.EXPAND | wx.ALL, border=5)
        sizer_input_output.Add(self.confidence_text,pos=(2,0), flag = wx.ALL, border=5)
        sizer_input_output.Add(self.confidence,pos=(2,1), flag = wx.ALL, border=5)
        sizer_input_output.Add(self.precision_text,pos=(3,0), flag = wx.ALL, border=5)
        sizer_input_output.Add(self.precision,pos=(3,1), flag = wx.ALL, border=5)
       
        sizer_process_files = wx.BoxSizer(wx.HORIZONTAL)
        self.process_files_tree = file_list_control(self, 0,self.output_dir_path)
        sizer_process_files.Add(self.process_files_tree, 0, wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self._on_update_mark, self.process_files_tree)
        self.Bind(wx.EVT_ACTIVATE, self._on_save_mark_file_status, self.process_files_tree)
        # Not showing the file_list_control initially
        self.process_files_tree.Show(False) 

        sizer_btn = wx.BoxSizer( wx.HORIZONTAL ) 
        sizer_btn.Add(self.button_run, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)
        sizer_btn.Add(self.button_exit, proportion=0, flag=wx.ALL | wx.ALIGN_RIGHT, border=5) 

        sizer_main = wx.GridBagSizer(5,5)
        sizer_main.Add(self.banner,pos = (0,0), span = (1,3), flag =  wx.ALL | wx.EXPAND, border=5)
        sizer_main.Add(sizer_input_output,pos = (1,0), span = (1,3), flag =  wx.ALL, border=5)
        sizer_main.Add(sizer_btn, pos = (2,0), span = (1,3), flag = wx.ALIGN_CENTER | wx.ALL, border=5)
        sizer_main.Add(sizer_process_files,pos = (3,0), span = (3,3), flag = wx.EXPAND | wx.ALL, border=5)
        
        self.SetSizerAndFit(sizer_main)
        self.Layout()
        
    def _create_menu_bar(self):
        
        # Setting up the menu.
        menu_file = wx.Menu()
        mitem_about = menu_file.Append(wx.ID_ABOUT, "&About", " Information about this program")
        mitem_exit = menu_file.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # Creating the menubar.
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_file,"&File") # Adding the "menu_file" to the MenuBar

        # Set events.
        self.Bind(wx.EVT_MENU, self._on_about, mitem_about)
        self.Bind(wx.EVT_MENU, self._on_exit, mitem_exit)    

        self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.

        
    # Event handlers
  

    def _on_about(self, e):
        '''Create a message dialog box
        
        '''
        
        about_text = """Random sampler: 
        This application randomly samples the files 
        given in the input directory and copies them to the output 
        directory. The sample size is calculated by the given 
        confidence interval."""
        dlg = wx.MessageDialog(self, about_text, "About Random Sampler", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def _on_exit(self,e):
        '''Handles the application exits EVENT 
        
        '''
        
        dlg = wx.MessageDialog(self, "Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def _on_select_input_folder(self, e):
        """Open a folder for input
        
        """

        dlg = wx.DirDialog(self, "Choose the input folder to sample",self.dir_path,wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dir_path = dlg.GetPath()
        dlg.Destroy()
        self.input_folder_control.SetValue(self.dir_path)
        self.SetStatusText("The selected input folder is %s" % self.dir_path)
        
    def _on_select_output_folder(self, e):
        """ Open a folder for output 
        
        """
        dlg = wx.DirDialog(self,"Choose the Output folder to save",self.output_dir_path,wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_path = dlg.GetPath()
        dlg.Destroy()
        self.output_folder_control.SetValue(self.output_dir_path)
        self.SetStatusText("The selected output folder is %s" % self.output_dir_path)
        
    def _on_run_sampler(self, e):
        '''Handles the run sampler button click event 

        '''
        try:
            
            self.confidence_val = Decimal(self.confidence.GetValue()) / Decimal('100')
            self.precision_val = float(self.precision.GetValue()) / 100.0 
            
            if not os.path.exists(self.dir_path) or not os.path.exists(self.output_dir_path):
                dlg = wx.MessageDialog(self, "Please enter a valid input/output directory", "Error", wx.ICON_ERROR)
                dlg.ShowModal()
                return 
            
            file_list = find_files_in_folder(self.dir_path)
            self.SetStatusText('%d files found in %s.' % (len(file_list), self.dir_path) )
            
            sampled_files = random_sampler(file_list, self.confidence_val, self.precision_val, self.SEED)
            self.SetStatusText('%d files are sampled out of %d files.' % (len(sampled_files), len(file_list)))
            
            copy_files_with_dir_tree(self.dir_path, sampled_files, self.output_dir_path)
            self.SetStatusText('%d randomly sampled files (from %d files) are copied to the output folder.' % (len(sampled_files), len(file_list)))

            
            # shows the tree list control 
            self.process_files_tree.on_changed_output_dir(self.output_folder_control.GetValue())
            self.process_files_tree.Show(True)
            self.GetSizer().Layout()
            self.Refresh()

        
        
        except Exception as anyException:
            dlg = wx.MessageDialog(self, str(anyException), "Error", wx.ICON_ERROR)
            dlg.ShowModal()

    
    def _on_update_mark(self, e):
        '''
        Handles status update to upper control on new file marked/unmarked
        '''
        file_count = e.GetClientData()
        self.SetStatusText("Number of files selected %s." %file_count)
        
    def _on_save_mark_file_status(self, e):
        '''
        Handles status update to upper control on saving marked file
        '''
        update_message = e.GetClientData()
        self.SetStatusText("Saved " + str(update_message) + " files at " + os.path.basename(self.output_dir_path))


def main():
    
    app = wx.App(False)
    RandomSamplerGUI(None)
    app.MainLoop()  


if __name__ == '__main__':    
    main()
    