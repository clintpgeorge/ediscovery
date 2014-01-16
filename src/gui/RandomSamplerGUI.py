# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class RandomSamplerGUI
###########################################################################

class RandomSamplerGUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Random Sampler", pos = wx.DefaultPosition, size = wx.Size( 1100,700 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.HSCROLL|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 1100,500 ), wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self._statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_appln = wx.Menu()
		self._mitem_about = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_about )
		
		self._mitem_license  = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"License", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_license  )
		
		self._mitem_help = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_help )
		
		self._mitem_exit = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_exit )
		
		self._menubar.Append( self._menu_appln, u"Application" ) 
		
		self.SetMenuBar( self._menubar )
		
		bsizer_main = wx.BoxSizer( wx.VERTICAL )
		
		self._bitmap_uf_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"res/uflaw-edisc11.jpg", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 160,50 ), 0 )
		bsizer_main.Add( self._bitmap_uf_logo, 0, wx.ALIGN_RIGHT|wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.nb_config_sampler = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nb_config_sampler.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		self._panel_io = wx.Panel( self.nb_config_sampler, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbsizer_io = wx.StaticBoxSizer( wx.StaticBox( self._panel_io, wx.ID_ANY, u"Sampler" ), wx.VERTICAL )
		
		gbsizer_io = wx.GridBagSizer( 2, 5 )
		gbsizer_io.SetFlexibleDirection( wx.BOTH )
		gbsizer_io.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_header1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Select the Source Document Folder and the desired Sampled Output Folder. \n\nThe Source Document Folder is the folder which contains the document population to be sampled. The Sampled Output Folder indicates a location where the Random Sampler will store the sampled documents based of the confidence level provided by you in the next tab.", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header1.Wrap( 1050 )
		self._st_header1.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header1.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		self._st_header1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_io.Add( self._st_header1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header1 = wx.StaticLine( self._panel_io, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_io.Add( self._sl_header1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		self._st_project_title = wx.StaticText( self._panel_io, wx.ID_ANY, u"Project Title", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_project_title.Wrap( -1 )
		gbsizer_io.Add( self._st_project_title, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_project_titleChoices = []
		self._cbx_project_title = wx.ComboBox( self._panel_io, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_project_titleChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.TE_PROCESS_ENTER )
		self._cbx_project_title.SetMinSize( wx.Size( 300,20 ) )
		
		gbsizer_io.Add( self._cbx_project_title, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self._st_data_folder1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Source Document Folder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_data_folder1.Wrap( -1 )
		self._st_data_folder1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_io.Add( self._st_data_folder1, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chk_io_new_project = wx.CheckBox( self._panel_io, wx.ID_ANY, u"Check the box to create a new project ", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_io.Add( self._chk_io_new_project, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText24 = wx.StaticText( self._panel_io, wx.ID_ANY, u"OR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		gbsizer_io.Add( self.m_staticText24, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText251 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Select an existing project from the drop down list", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText251.Wrap( -1 )
		gbsizer_io.Add( self.m_staticText251, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_io_new_project = wx.TextCtrl( self._panel_io, wx.ID_ANY, u"Title of the new project...", wx.DefaultPosition, wx.Size( 300,-1 ), wx.TE_LEFT )
		self._tc_io_new_project.Enable( False )
		
		gbsizer_io.Add( self._tc_io_new_project, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_data_dir = wx.TextCtrl( self._panel_io, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_READONLY )
		self._tc_data_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		self._tc_data_dir.SetMinSize( wx.Size( 300,25 ) )
		
		gbsizer_io.Add( self._tc_data_dir, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_io_sel_data_dir = wx.Button( self._panel_io, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_io.Add( self._btn_io_sel_data_dir, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_output_dir1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Sampled Output Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_output_dir1.Wrap( -1 )
		self._st_output_dir1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self._st_output_dir1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_io.Add( self._st_output_dir1, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_output_dir = wx.TextCtrl( self._panel_io, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,25 ), wx.TE_LEFT|wx.TE_READONLY )
		self._tc_output_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_io.Add( self._tc_output_dir, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_io_sel_output_dir = wx.Button( self._panel_io, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_io.Add( self._btn_io_sel_output_dir, wx.GBPosition( 9, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_data_dir_files = wx.StaticText( self._panel_io, wx.ID_ANY, u"0 documents", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_num_data_dir_files.Wrap( -1 )
		self._st_num_data_dir_files.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_data_dir_files.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_io.Add( self._st_num_data_dir_files, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._st_new_project_title = wx.StaticText( self._panel_io, wx.ID_ANY, u"Enter New Project Title", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_new_project_title.Wrap( -1 )
		self._st_new_project_title.Enable( False )
		self._st_new_project_title.Hide()
		
		gbsizer_io.Add( self._st_new_project_title, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._sl_tailer1 = wx.StaticLine( self._panel_io, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_io.Add( self._sl_tailer1, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		_bsizer_io_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_io_next = wx.Button( self._panel_io, wx.ID_ANY, u"Next ( Set confidence levels )", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_io_buttons.Add( self._btn_io_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_io.Add( _bsizer_io_buttons, wx.GBPosition( 11, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		_bsizer_io_clrbtns = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_io_clear = wx.Button( self._panel_io, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_io_clrbtns.Add( self._btn_io_clear, 0, wx.ALL, 5 )
		
		
		gbsizer_io.Add( _bsizer_io_clrbtns, wx.GBPosition( 11, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT, 5 )
		
		
		sbsizer_io.Add( gbsizer_io, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		self._panel_io.SetSizer( sbsizer_io )
		self._panel_io.Layout()
		sbsizer_io.Fit( self._panel_io )
		self.nb_config_sampler.AddPage( self._panel_io, u"Data and Ouput", True )
		self._panel_confidence = wx.Panel( self.nb_config_sampler, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bsizer_confidence = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_confidence = wx.StaticBoxSizer( wx.StaticBox( self._panel_confidence, wx.ID_ANY, u"Sampler" ), wx.VERTICAL )
		
		gbsizer_confidence = wx.GridBagSizer( 2, 5 )
		gbsizer_confidence.SetFlexibleDirection( wx.BOTH )
		gbsizer_confidence.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_header2 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Select the Confidence Level and the Confidence Interval to compute sample size. The selected Confidence Interval and Confidence Level determines the sample size.", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header2.Wrap( -1 )
		self._st_header2.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header2.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		self._st_header2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_confidence.Add( self._st_header2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 6 ), wx.ALL, 5 )
		
		self._sl_header2 = wx.StaticLine( self._panel_confidence, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_confidence.Add( self._sl_header2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_confidence_level1 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Confidence Level (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_level1.Wrap( -1 )
		self._st_confidence_level1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_confidence.Add( self._st_confidence_level1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_confidence_levelsChoices = []
		self._cbx_confidence_levels = wx.ComboBox( self._panel_confidence, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 90,-1 ), _cbx_confidence_levelsChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self._cbx_confidence_levels.SetSelection( 0 )
		self._cbx_confidence_levels.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_confidence.Add( self._cbx_confidence_levels, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.TOP, 5 )
		
		_cbx_confidence_intervalChoices = [ u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10" ]
		self._cbx_confidence_interval = wx.ComboBox( self._panel_confidence, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 90,-1 ), _cbx_confidence_intervalChoices, wx.CB_READONLY )
		gbsizer_confidence.Add( self._cbx_confidence_interval, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_interval1 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Confidence Interval (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_interval1.Wrap( -1 )
		self._st_confidence_interval1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_confidence.Add( self._st_confidence_interval1, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_samples = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"0 samples found out of 0 files", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_num_samples.Wrap( -1 )
		self._st_num_samples.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_samples.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_confidence.Add( self._st_num_samples, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT|wx.TOP, 5 )
		
		self.m_staticText26 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Sample Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		gbsizer_confidence.Add( self.m_staticText26, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._sl_tailer2 = wx.StaticLine( self._panel_confidence, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_confidence.Add( self._sl_tailer2, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		_bsizer_cl_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_cl_goback = wx.Button( self._panel_confidence, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_cl_buttons.Add( self._btn_cl_goback, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_cl_next = wx.Button( self._panel_confidence, wx.ID_ANY, u"Next ( Review Sample Creation Parameters)", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_cl_buttons.Add( self._btn_cl_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_confidence.Add( _bsizer_cl_buttons, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		
		sbsizer_confidence.Add( gbsizer_confidence, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		bsizer_confidence.Add( sbsizer_confidence, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self._panel_confidence.SetSizer( bsizer_confidence )
		self._panel_confidence.Layout()
		bsizer_confidence.Fit( self._panel_confidence )
		self.nb_config_sampler.AddPage( self._panel_confidence, u"Confidence", False )
		self._panel_create_sample = wx.Panel( self.nb_config_sampler, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbsizer_sampler = wx.StaticBoxSizer( wx.StaticBox( self._panel_create_sample, wx.ID_ANY, u"Sampler" ), wx.VERTICAL )
		
		gbsizer_sampler1 = wx.GridBagSizer( 2, 5 )
		gbsizer_sampler1.SetFlexibleDirection( wx.BOTH )
		gbsizer_sampler1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_header = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Below are your Randam Sampler specifications", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header.Wrap( -1 )
		self._st_header.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		self._st_header.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler1.Add( self._st_header, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header = wx.StaticLine( self._panel_create_sample, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler1.Add( self._sl_header, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_project_title = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Project Title", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_project_title.Wrap( -1 )
		gbsizer_sampler1.Add( self._st_project_title, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_project_title = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		gbsizer_sampler1.Add( self._tc_project_title, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), 0, 5 )
		
		self._st_data_folder = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Source Document Folder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_data_folder.Wrap( -1 )
		self._st_data_folder.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_data_folder, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_data_dir = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_data_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		self._tc_out_data_dir.SetMinSize( wx.Size( 300,20 ) )
		
		gbsizer_sampler1.Add( self._tc_out_data_dir, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_output_dir = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Sampled Output Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_output_dir.Wrap( -1 )
		self._st_output_dir.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self._st_output_dir.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler1.Add( self._st_output_dir, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_output_dir = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_output_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_output_dir, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_level = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Confidence Level (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_level.Wrap( -1 )
		self._st_confidence_level.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_confidence_level, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_confidence_levels = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_confidence_levels.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_confidence_levels, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_confidence_interval = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 30,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_confidence_interval.SetMaxLength( 2 ) 
		self._tc_out_confidence_interval.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_confidence_interval, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_interval = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Confidence Interval (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_interval.Wrap( -1 )
		self._st_confidence_interval.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_confidence_interval, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_out_num_samples = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"0 samples found", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_out_num_samples.Wrap( -1 )
		self._st_out_num_samples.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_out_num_samples.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler1.Add( self._st_out_num_samples, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT|wx.TOP, 5 )
		
		self.m_staticText29 = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Documents in sample", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		gbsizer_sampler1.Add( self.m_staticText29, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_out_num_data_dir_files = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"0 documents", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_out_num_data_dir_files.Wrap( -1 )
		self._st_out_num_data_dir_files.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_out_num_data_dir_files.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler1.Add( self._st_out_num_data_dir_files, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT|wx.TOP, 5 )
		
		self._sl_tailer = wx.StaticLine( self._panel_create_sample, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler1.Add( self._sl_tailer, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		bsizer_cg = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_copy_files = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Next (Create Sample)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_cg.Add( self._btn_copy_files, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_out_go_to_review = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Next ( Go to Review )", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._btn_out_go_to_review.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )
		self._btn_out_go_to_review.Hide()
		
		bsizer_cg.Add( self._btn_out_go_to_review, 0, wx.ALL, 5 )
		
		
		gbsizer_sampler1.Add( bsizer_cg, wx.GBPosition( 10, 3 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
		
		bsizer_ge = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_out_goback = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_ge.Add( self._btn_out_goback, 0, wx.ALL, 5 )
		
		self._btn_out_exit = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_ge.Add( self._btn_out_exit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler1.Add( bsizer_ge, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
		
		self.m_staticText28 = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Documents in source folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		gbsizer_sampler1.Add( self.m_staticText28, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_sampler.Add( gbsizer_sampler1, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		self._panel_create_sample.SetSizer( sbsizer_sampler )
		self._panel_create_sample.Layout()
		sbsizer_sampler.Fit( self._panel_create_sample )
		self.nb_config_sampler.AddPage( self._panel_create_sample, u"Create Sample", False )
		self._panel_review = wx.Panel( self.nb_config_sampler, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbsizer_review = wx.StaticBoxSizer( wx.StaticBox( self._panel_review, wx.ID_ANY, u"Samples" ), wx.VERTICAL )
		
		gbsizer_review = wx.GridBagSizer( 0, 0 )
		gbsizer_review.SetFlexibleDirection( wx.BOTH )
		gbsizer_review.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText33 = wx.StaticText( self._panel_review, wx.ID_ANY, u"The documents can be reviewed by two methods:\n1. Single click on the document: If it is an email or a text document you will be able to review the document in Document Preview pane.\n2. Double click on the document: A window will ask you for a document viewer installed on your computer. To view the document you must have a software installed that can open the document.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( 900 )
		self.m_staticText33.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_review.Add( self.m_staticText33, wx.GBPosition( 2, 0 ), wx.GBSpan( 2, 8 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self._btn_review_clear_all_tags = wx.Button( self._panel_review, wx.ID_ANY, u"Clear All Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_review.Add( self._btn_review_clear_all_tags, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.TOP, 5 )
		
		self._panel_doc_tags = wx.Panel( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bsizer_doc_tags = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_responsiveChoices = [ u"Valid", u"Invalid", u"Further Review Required" ]
		self._rbx_responsive = wx.RadioBox( self._panel_doc_tags, wx.ID_ANY, u"Feedback", wx.DefaultPosition, wx.DefaultSize, _rbx_responsiveChoices, 3, wx.RA_SPECIFY_ROWS )
		self._rbx_responsive.SetSelection( 2 )
		bsizer_doc_tags.Add( self._rbx_responsive, 0, wx.ALL, 5 )
		
		_rbx_privilegedChoices = [ u"Yes", u"No", u"Unknown" ]
		self._rbx_privileged = wx.RadioBox( self._panel_doc_tags, wx.ID_ANY, u"Privileged", wx.DefaultPosition, wx.DefaultSize, _rbx_privilegedChoices, 2, wx.RA_SPECIFY_ROWS )
		self._rbx_privileged.SetSelection( 2 )
		self._rbx_privileged.Enable( False )
		self._rbx_privileged.Hide()
		
		bsizer_doc_tags.Add( self._rbx_privileged, 0, wx.ALL, 5 )
		
		
		self._panel_doc_tags.SetSizer( bsizer_doc_tags )
		self._panel_doc_tags.Layout()
		bsizer_doc_tags.Fit( self._panel_doc_tags )
		gbsizer_review.Add( self._panel_doc_tags, wx.GBPosition( 4, 7 ), wx.GBSpan( 2, 2 ), wx.ALL|wx.EXPAND, 5 )
		
		bsizer_review_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_review_goback = wx.Button( self._panel_review, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_review_buttons.Add( self._btn_review_goback, 0, wx.ALL, 5 )
		
		self._btn_review_exit = wx.Button( self._panel_review, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_review_buttons.Add( self._btn_review_exit, 0, wx.ALL, 5 )
		
		
		gbsizer_review.Add( bsizer_review_buttons, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )
		
		self.m_staticText21 = wx.StaticText( self._panel_review, wx.ID_ANY, u"This tab shows the documents selected by the Random Sampler for review based on your specifications.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.m_staticText21.SetForegroundColour( wx.Colour( 0, 0, 255 ) )
		
		gbsizer_review.Add( self.m_staticText21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self._sl_header3 = wx.StaticLine( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_review.Add( self._sl_header3, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 12 ), wx.EXPAND |wx.ALL, 5 )
		
		self._panel_review_tag = wx.Panel( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_review_tag.SetMinSize( wx.Size( 315,270 ) )
		
		gbsizer_review.Add( self._panel_review_tag, wx.GBPosition( 4, 0 ), wx.GBSpan( 3, 3 ), wx.EXPAND, 5 )
		
		self._tc_preview = wx.TextCtrl( self._panel_review, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self._tc_preview.SetMinSize( wx.Size( 420,255 ) )
		
		gbsizer_review.Add( self._tc_preview, wx.GBPosition( 5, 3 ), wx.GBSpan( 4, 5 ), wx.LEFT, 20 )
		
		self.m_staticText25 = wx.StaticText( self._panel_review, wx.ID_ANY, u"Document Preview (Only Emails and Text)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		gbsizer_review.Add( self.m_staticText25, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 2 ), wx.LEFT|wx.RIGHT, 20 )
		
		self._sl_header31 = wx.StaticLine( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_review.Add( self._sl_header31, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 12 ), wx.EXPAND |wx.ALL, 5 )
		
		bsizer_generate_reports = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText34 = wx.StaticText( self._panel_review, wx.ID_ANY, u"Select a Tag", wx.Point( -1,-1 ), wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText34.Wrap( -1 )
		self.m_staticText34.Hide()
		
		bsizer_generate_reports.Add( self.m_staticText34, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		_cbx_report_typesChoices = [ u"Responsive", u"Privileged", u"All" ]
		self._cbx_report_types = wx.ComboBox( self._panel_review, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_report_typesChoices, wx.CB_READONLY|wx.CB_SORT )
		self._cbx_report_types.SetSelection( 0 )
		self._cbx_report_types.Hide()
		
		bsizer_generate_reports.Add( self._cbx_report_types, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self._btn_review_gen_report = wx.Button( self._panel_review, wx.ID_ANY, u"Generate Report", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_generate_reports.Add( self._btn_review_gen_report, 0, wx.ALL, 5 )
		
		
		gbsizer_review.Add( bsizer_generate_reports, wx.GBPosition( 10, 7 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
		
		
		sbsizer_review.Add( gbsizer_review, 0, wx.BOTTOM|wx.EXPAND, 5 )
		
		
		self._panel_review.SetSizer( sbsizer_review )
		self._panel_review.Layout()
		sbsizer_review.Fit( self._panel_review )
		self.nb_config_sampler.AddPage( self._panel_review, u"Sample Review", False )
		
		bsizer_main.Add( self.nb_config_sampler, 1, wx.EXPAND |wx.ALL, 5 )
		
		self._lbl_about = wx.StaticText( self, wx.ID_ANY, u" © 2013 University of Florida.  All rights reserved. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._lbl_about.Wrap( -1 )
		bsizer_main.Add( self._lbl_about, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.SetSizer( bsizer_main )
		self.Layout()
		self.menu_open = wx.Menu()
		self.menu_open_folder = wx.MenuItem( self.menu_open, wx.ID_ANY, u"Open Containing Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_open.AppendItem( self.menu_open_folder )
		
		self.menu_open_file_other = wx.MenuItem( self.menu_open, wx.ID_ANY, u"Open file with ..", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_open.AppendItem( self.menu_open_file_other )
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.RandomSamplerGUIOnContextMenu ) 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self._on_appln_close )
		self.Bind( wx.EVT_MENU, self._on_mitem_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_click_license, id = self._mitem_license .GetId() )
		self.Bind( wx.EVT_MENU, self._on_mitem_help, id = self._mitem_help.GetId() )
		self.Bind( wx.EVT_MENU, self._on_mitem_exit, id = self._mitem_exit.GetId() )
		self.nb_config_sampler.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_nb_page_changed )
		self._cbx_project_title.Bind( wx.EVT_COMBOBOX, self._on_set_existing_project )
		self._cbx_project_title.Bind( wx.EVT_TEXT_ENTER, self._on_update_project_name )
		self._chk_io_new_project.Bind( wx.EVT_CHECKBOX, self._on_click_io_sel_new_project )
		self._tc_io_new_project.Bind( wx.EVT_KILL_FOCUS, self._update_project_new_name )
		self._btn_io_sel_data_dir.Bind( wx.EVT_BUTTON, self._on_click_io_sel_data_dir )
		self._btn_io_sel_output_dir.Bind( wx.EVT_BUTTON, self._on_click_io_sel_output_dir )
		self._btn_io_next.Bind( wx.EVT_BUTTON, self._on_click_io_next )
		self._btn_io_clear.Bind( wx.EVT_BUTTON, self._on_click_io_clear )
		self._cbx_confidence_levels.Bind( wx.EVT_COMBOBOX, self._on_confidence_changed )
		self._cbx_confidence_interval.Bind( wx.EVT_COMBOBOX, self._on_precision_changed )
		self._btn_cl_goback.Bind( wx.EVT_BUTTON, self._on_click_cl_goback )
		self._btn_cl_next.Bind( wx.EVT_BUTTON, self._on_click_cl_next )
		self._btn_copy_files.Bind( wx.EVT_BUTTON, self._on_click_copy_files )
		self._btn_out_go_to_review.Bind( wx.EVT_BUTTON, self._on_click_out_go_to_review )
		self._btn_out_goback.Bind( wx.EVT_BUTTON, self._on_click_out_goback )
		self._btn_out_exit.Bind( wx.EVT_BUTTON, self._on_click_out_exit )
		self._btn_review_clear_all_tags.Bind( wx.EVT_BUTTON, self._on_click_clear_all_doc_tags )
		self._rbx_responsive.Bind( wx.EVT_RADIOBOX, self._on_rbx_responsive_updated )
		self._rbx_privileged.Bind( wx.EVT_RADIOBOX, self._on_rbx_privileged_updated )
		self._btn_review_goback.Bind( wx.EVT_BUTTON, self._on_click_review_goback )
		self._btn_review_exit.Bind( wx.EVT_BUTTON, self._on_click_review_exit )
		self._btn_review_gen_report.Bind( wx.EVT_BUTTON, self._on_click_review_gen_report )
		self.Bind( wx.EVT_MENU, self.on_popup_open_folder, id = self.menu_open_folder.GetId() )
		self.Bind( wx.EVT_MENU, self.on_popup_open_file_other, id = self.menu_open_file_other.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_appln_close( self, event ):
		event.Skip()
	
	def _on_mitem_about( self, event ):
		event.Skip()
	
	def _on_click_license( self, event ):
		event.Skip()
	
	def _on_mitem_help( self, event ):
		event.Skip()
	
	def _on_mitem_exit( self, event ):
		event.Skip()
	
	def _on_nb_page_changed( self, event ):
		event.Skip()
	
	def _on_set_existing_project( self, event ):
		event.Skip()
	
	def _on_update_project_name( self, event ):
		event.Skip()
	
	def _on_click_io_sel_new_project( self, event ):
		event.Skip()
	
	def _update_project_new_name( self, event ):
		event.Skip()
	
	def _on_click_io_sel_data_dir( self, event ):
		event.Skip()
	
	def _on_click_io_sel_output_dir( self, event ):
		event.Skip()
	
	def _on_click_io_next( self, event ):
		event.Skip()
	
	def _on_click_io_clear( self, event ):
		event.Skip()
	
	def _on_confidence_changed( self, event ):
		event.Skip()
	
	def _on_precision_changed( self, event ):
		event.Skip()
	
	def _on_click_cl_goback( self, event ):
		event.Skip()
	
	def _on_click_cl_next( self, event ):
		event.Skip()
	
	def _on_click_copy_files( self, event ):
		event.Skip()
	
	def _on_click_out_go_to_review( self, event ):
		event.Skip()
	
	def _on_click_out_goback( self, event ):
		event.Skip()
	
	def _on_click_out_exit( self, event ):
		event.Skip()
	
	def _on_click_clear_all_doc_tags( self, event ):
		event.Skip()
	
	def _on_rbx_responsive_updated( self, event ):
		event.Skip()
	
	def _on_rbx_privileged_updated( self, event ):
		event.Skip()
	
	def _on_click_review_goback( self, event ):
		event.Skip()
	
	def _on_click_review_exit( self, event ):
		event.Skip()
	
	def _on_click_review_gen_report( self, event ):
		event.Skip()
	
	def on_popup_open_folder( self, event ):
		event.Skip()
	
	def on_popup_open_file_other( self, event ):
		event.Skip()
	
	def RandomSamplerGUIOnContextMenu( self, event ):
		self.PopupMenu( self.menu_open, event.GetPosition() )
		

###########################################################################
## Class TagDocumentDialog
###########################################################################

class TagDocumentDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Tag the Document", pos = wx.DefaultPosition, size = wx.Size( 250,227 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bsizer_doc_tags = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_responsiveChoices = [ u"Yes", u"No", u"Unknown" ]
		self._rbx_responsive = wx.RadioBox( self, wx.ID_ANY, u"Responsive", wx.DefaultPosition, wx.DefaultSize, _rbx_responsiveChoices, 2, wx.RA_SPECIFY_ROWS )
		self._rbx_responsive.SetSelection( 2 )
		bsizer_doc_tags.Add( self._rbx_responsive, 0, wx.ALL, 5 )
		
		_rbx_privilegedChoices = [ u"Yes", u"No", u"Unknown" ]
		self._rbx_privileged = wx.RadioBox( self, wx.ID_ANY, u"Privileged", wx.DefaultPosition, wx.DefaultSize, _rbx_privilegedChoices, 2, wx.RA_SPECIFY_ROWS )
		self._rbx_privileged.SetSelection( 2 )
		bsizer_doc_tags.Add( self._rbx_privileged, 0, wx.ALL, 5 )
		
		gsizer_buttons = wx.GridSizer( 1, 2, 0, 0 )
		
		self._btn_add_tags = wx.Button( self, wx.ID_ANY, u"Add Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gsizer_buttons.Add( self._btn_add_tags, 0, wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self._btn_clear_doc_tags = wx.Button( self, wx.ID_ANY, u"Clear Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gsizer_buttons.Add( self._btn_clear_doc_tags, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bsizer_doc_tags.Add( gsizer_buttons, 1, wx.ALIGN_BOTTOM|wx.EXPAND, 10 )
		
		
		self.SetSizer( bsizer_doc_tags )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self._rbx_responsive.Bind( wx.EVT_RADIOBOX, self._on_rbx_responsive_updated )
		self._btn_add_tags.Bind( wx.EVT_BUTTON, self._on_click_add_tags )
		self._btn_clear_doc_tags.Bind( wx.EVT_BUTTON, self._on_click_clear_tags )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_rbx_responsive_updated( self, event ):
		event.Skip()
	
	def _on_click_add_tags( self, event ):
		event.Skip()
	
	def _on_click_clear_tags( self, event ):
		event.Skip()
	

###########################################################################
## Class LicenseDialog
###########################################################################

class LicenseDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"License", pos = wx.DefaultPosition, size = wx.Size( 408,465 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bsizer_license_txt = wx.BoxSizer( wx.VERTICAL )
		
		self._tc_license = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,1 ), wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self._tc_license.SetMinSize( wx.Size( -1,435 ) )
		
		bsizer_license_txt.Add( self._tc_license, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bsizer_license_txt )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class HelpDialog
###########################################################################

class HelpDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Help", pos = wx.DefaultPosition, size = wx.Size( 408,465 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bsizer_help_txt = wx.BoxSizer( wx.VERTICAL )
		
		self._tc_help = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,1 ), wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self._tc_help.SetMinSize( wx.Size( -1,435 ) )
		
		bsizer_help_txt.Add( self._tc_help, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bsizer_help_txt )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

