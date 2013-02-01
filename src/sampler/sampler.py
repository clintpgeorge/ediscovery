import wx
import os
from file_utils import find_files_in_folder
from random_sampler2 import random_sampler

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = os.getcwd()
        self.outname = os.getcwd()
        self.confidence_val = 0.75
        self.precision_val = 0.01
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(1024,768))
        
        
        self.banner = wx.StaticText(self, id=wx.ID_ABOUT, label="Random Sampler for E-Discovery", size=(400,100), style=wx.TE_AUTO_SCROLL)
        
        # Input folder section
        self.input_folder_label = wx.StaticText(self,label="Input folder = ")
        self.input_folder = wx.TextCtrl(self, style=wx.TE_BESTWRAP)
        self.input_folder.SetEditable(False)
        #self.input_folder.Disable()
        self.input_folder.SetValue(self.dirname)
        self.input_folder_button = wx.Button(self,wx.ID_OPEN,"Open Folder")
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.input_folder_button)
        self.line = wx.StaticLine(self)
        
        # Setting out[ut folder section
        self.output_folder_label = wx.StaticText(self,label="Output folder = ")
        self.output_folder = wx.TextCtrl(self, style=wx.TE_BESTWRAP)
        self.output_folder.SetEditable(False)
        #self.output_folder.Disable()
        self.output_folder.SetValue(self.outname)
        self.output_folder_button = wx.Button(self,wx.ID_ANY,"Set Output Folder")
        self.Bind(wx.EVT_BUTTON, self.OnOpenOutput, self.output_folder_button)
        
        # Setting run and exit buttons
        self.exit = wx.Button(self,wx.ID_EXIT,"EXIT")
        self.run = wx.Button(self,wx.ID_ANY,"RUN")
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.exit)
        self.Bind(wx.EVT_BUTTON, self.OnRun, self.run)
        
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a folder to sample")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        
        
        # Setting parameters
        self.confidence_text = wx.StaticText(self,label="Confidence")
        self.precision_text = wx.StaticText(self,label="Precision")
        self.confidence = wx.Slider(self, -1, 75, 75, 99, wx.DefaultPosition, (250, -1),\
                                   wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.precision = wx.Slider(self, -1, 1, 1, 5, wx.DefaultPosition, (250, -1),\
                                   wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER, self.OnAdjust, self.confidence)
        self.Bind(wx.EVT_SLIDER, self.OnAdjust, self.precision)
        
        
        # Layouts 
        
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.input_folder_label, 1, wx.EXPAND | wx.ALL, border=5, )
        self.sizer2.Add(self.input_folder, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer2.Add(self.input_folder_button, 1, wx.EXPAND | wx.ALL, border=5)
        
        
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3.Add(self.output_folder_label, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer3.Add(self.output_folder, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer3.Add(self.output_folder_button, 1, wx.EXPAND | wx.ALL, border=5)
        
        
        self.sizer4 = wx.BoxSizer(wx.VERTICAL)
        self.sizer4.Add(self.confidence_text, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer4.Add(self.confidence, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer4.Add(self.precision_text, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer4.Add(self.precision, 1, wx.EXPAND | wx.ALL, border=5)
        
        
        self.sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer5.Add(self.exit, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer5.Add(self.run, 1, wx.EXPAND | wx.ALL, border=5)
        
        
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.banner, 0, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.sizer3, 0, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.line, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.sizer4, 0, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.line, 1, wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.sizer5, 1, wx.EXPAND | wx.ALL, border=5)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()
        
        # Event handlers
    def OnAdjust(self, event):
        self.confidence_val = float(self.confidence.GetValue())/100
        self.precision_val = float(self.precision.GetValue())/100
            

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " A random sampler \n for eDiscovery", "About Random Sampler", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a folder for input"""
        #FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        dlg = wx.DirDialog(self,"Choose the input folder to sample",self.dirname,wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
        dlg.Destroy()
        self.input_folder.SetValue(self.dirname)
        
    def OnOpenOutput(self,e):
        """ Open a folder for input"""
        #FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        dlg = wx.DirDialog(self,"Choose the Output folder to save",self.outname,wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.outname = dlg.GetPath()
        dlg.Destroy()
        self.output_folder.SetValue(self.outname)
        
    def OnRun(self,e):
        try:
            file_list = find_files_in_folder(os.path.abspath(self.dirname))
            #print file_list
            #confidence = self.confidence.GetValue()/100
            #precision = self.precision.GetValue()/100
            random_sampler(file_list, self.confidence_val, self.precision_val, 2013)
        except Exception as anyException:
            dlg = wx.MessageDialog(self,str(anyException),"Error",wx.ICON_ERROR)
            dlg.ShowModal()
        return     

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()