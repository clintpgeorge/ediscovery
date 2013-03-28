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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Random Sampler", pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.HSCROLL|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 900,450 ), wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self._statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_appln = wx.Menu()
		self._mitem_about = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_about )
		
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
		
		self._st_header1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Select Source Document Folder and desired Sampled Output Folder. \n\nSource Document Folder is the folder you want to sample. Sampled Output Folder contains the produced sample. You may need to create this folder. ", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header1.Wrap( -1 )
		self._st_header1.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self._st_header1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_io.Add( self._st_header1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header1 = wx.StaticLine( self._panel_io, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_io.Add( self._sl_header1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_data_folder1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Source Document Folder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_data_folder1.Wrap( -1 )
		self._st_data_folder1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_io.Add( self._st_data_folder1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_data_dir = wx.TextCtrl( self._panel_io, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_READONLY )
		self._tc_data_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		self._tc_data_dir.SetMinSize( wx.Size( 300,25 ) )
		
		gbsizer_io.Add( self._tc_data_dir, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_io_sel_data_dir = wx.Button( self._panel_io, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_io.Add( self._btn_io_sel_data_dir, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_output_dir1 = wx.StaticText( self._panel_io, wx.ID_ANY, u"Sampled Output Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_output_dir1.Wrap( -1 )
		self._st_output_dir1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self._st_output_dir1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_io.Add( self._st_output_dir1, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_output_dir = wx.TextCtrl( self._panel_io, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,25 ), wx.TE_LEFT|wx.TE_READONLY )
		self._tc_output_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_io.Add( self._tc_output_dir, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_io_sel_output_dir = wx.Button( self._panel_io, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_io.Add( self._btn_io_sel_output_dir, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_data_dir_files = wx.StaticText( self._panel_io, wx.ID_ANY, u"0 documents available", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_num_data_dir_files.Wrap( -1 )
		self._st_num_data_dir_files.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_data_dir_files.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_io.Add( self._st_num_data_dir_files, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._sl_tailer1 = wx.StaticLine( self._panel_io, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_io.Add( self._sl_tailer1, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		_bsizer_io_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_io_next = wx.Button( self._panel_io, wx.ID_ANY, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_io_buttons.Add( self._btn_io_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_io.Add( _bsizer_io_buttons, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		
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
		
		self._st_header2 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Select Confidence Interval and Confidence Level to compute sample size. ", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header2.Wrap( -1 )
		self._st_header2.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self._st_header2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_confidence.Add( self._st_header2, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header2 = wx.StaticLine( self._panel_confidence, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_confidence.Add( self._sl_header2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_confidence_level1 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Confidence Level (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_level1.Wrap( -1 )
		self._st_confidence_level1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_confidence.Add( self._st_confidence_level1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_confidence_levelsChoices = []
		self._cbx_confidence_levels = wx.ComboBox( self._panel_confidence, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_confidence_levelsChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self._cbx_confidence_levels.SetSelection( 0 )
		self._cbx_confidence_levels.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_confidence.Add( self._cbx_confidence_levels, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.TOP, 5 )
		
		self._tc_confidence_interval = wx.TextCtrl( self._panel_confidence, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 30,25 ), 0 )
		self._tc_confidence_interval.SetMaxLength( 2 ) 
		self._tc_confidence_interval.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_confidence.Add( self._tc_confidence_interval, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_interval1 = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"Confidence Interval (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_interval1.Wrap( -1 )
		self._st_confidence_interval1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_confidence.Add( self._st_confidence_interval1, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_samples = wx.StaticText( self._panel_confidence, wx.ID_ANY, u"0 samples found out of 0 files", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_num_samples.Wrap( -1 )
		self._st_num_samples.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_samples.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_confidence.Add( self._st_num_samples, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._sl_tailer2 = wx.StaticLine( self._panel_confidence, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_confidence.Add( self._sl_tailer2, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )
		
		_bsizer_cl_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_cl_goback = wx.Button( self._panel_confidence, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_cl_buttons.Add( self._btn_cl_goback, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_cl_next = wx.Button( self._panel_confidence, wx.ID_ANY, u"Next", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_cl_buttons.Add( self._btn_cl_next, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_confidence.Add( _bsizer_cl_buttons, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		
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
		
		self._st_header = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Below are your sampler specifications", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header.Wrap( -1 )
		self._st_header.SetFont( wx.Font( 8, 70, 90, 91, False, wx.EmptyString ) )
		self._st_header.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		self._st_header.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler1.Add( self._st_header, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header = wx.StaticLine( self._panel_create_sample, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler1.Add( self._sl_header, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_data_folder = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Data Folder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_data_folder.Wrap( -1 )
		self._st_data_folder.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_data_folder, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_data_dir = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_data_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		self._tc_out_data_dir.SetMinSize( wx.Size( 300,20 ) )
		
		gbsizer_sampler1.Add( self._tc_out_data_dir, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_output_dir = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Sampled Output", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_output_dir.Wrap( -1 )
		self._st_output_dir.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self._st_output_dir.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler1.Add( self._st_output_dir, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_output_dir = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_output_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_output_dir, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_level = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Confidence Level (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_level.Wrap( -1 )
		self._st_confidence_level.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_confidence_level, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_confidence_levels = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_confidence_levels.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_confidence_levels, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_out_confidence_interval = wx.TextCtrl( self._panel_create_sample, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 30,20 ), wx.TE_LEFT|wx.TE_READONLY|wx.NO_BORDER )
		self._tc_out_confidence_interval.SetMaxLength( 2 ) 
		self._tc_out_confidence_interval.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler1.Add( self._tc_out_confidence_interval, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_interval = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"Confidence Interval (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_interval.Wrap( -1 )
		self._st_confidence_interval.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler1.Add( self._st_confidence_interval, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_out_num_samples = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"0 samples found", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_out_num_samples.Wrap( -1 )
		self._st_out_num_samples.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_out_num_samples.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler1.Add( self._st_out_num_samples, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._st_out_num_data_dir_files = wx.StaticText( self._panel_create_sample, wx.ID_ANY, u"0 documents available", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_out_num_data_dir_files.Wrap( -1 )
		self._st_out_num_data_dir_files.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_out_num_data_dir_files.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler1.Add( self._st_out_num_data_dir_files, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._sl_tailer = wx.StaticLine( self._panel_create_sample, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler1.Add( self._sl_tailer, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 6 ), wx.ALL|wx.EXPAND, 5 )
		
		bsizer_cg = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_copy_files = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Create Sample", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_cg.Add( self._btn_copy_files, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_out_go_to_review = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Go to Review", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_cg.Add( self._btn_out_go_to_review, 0, wx.ALL, 5 )
		
		
		gbsizer_sampler1.Add( bsizer_cg, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
		
		bsizer_ge = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_out_goback = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_ge.Add( self._btn_out_goback, 0, wx.ALL, 5 )
		
		self._btn_out_exit = wx.Button( self._panel_create_sample, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_ge.Add( self._btn_out_exit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler1.Add( bsizer_ge, wx.GBPosition( 9, 3 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
		
		
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
		
		self.m_staticText33 = wx.StaticText( self._panel_review, wx.ID_ANY, u"Documents to be Reviewed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		self.m_staticText33.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_review.Add( self.m_staticText33, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self._btn_review_clear_all_tags = wx.Button( self._panel_review, wx.ID_ANY, u"Clear All Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_review.Add( self._btn_review_clear_all_tags, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT, 5 )
		
		self._lc_review = wx.ListCtrl( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		self._lc_review.SetMinSize( wx.Size( 600,200 ) )
		
		gbsizer_review.Add( self._lc_review, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self._panel_doc_tags = wx.Panel( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_doc_tags.SetMinSize( wx.Size( 180,100 ) )
		
		bsizer_doc_tags = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_doc_tags = wx.StaticBoxSizer( wx.StaticBox( self._panel_doc_tags, wx.ID_ANY, u"Select document tags" ), wx.VERTICAL )
		
		self._chbx_doc_relevant = wx.CheckBox( self._panel_doc_tags, wx.ID_ANY, u"Responsive", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbsizer_doc_tags.Add( self._chbx_doc_relevant, 0, wx.ALL, 5 )
		
		self._chbx_doc_privileged = wx.CheckBox( self._panel_doc_tags, wx.ID_ANY, u"Privileged", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbsizer_doc_tags.Add( self._chbx_doc_privileged, 0, wx.ALL, 5 )
		
		
		bsizer_doc_tags.Add( sbsizer_doc_tags, 0, wx.EXPAND, 5 )
		
		
		bsizer_doc_tags.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )
		
		sbsizer_reports = wx.StaticBoxSizer( wx.StaticBox( self._panel_doc_tags, wx.ID_ANY, u"Generate Reports" ), wx.VERTICAL )
		
		gbsizer_reports = wx.GridBagSizer( 0, 0 )
		gbsizer_reports.SetFlexibleDirection( wx.BOTH )
		gbsizer_reports.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText34 = wx.StaticText( self._panel_doc_tags, wx.ID_ANY, u"Select a Tag", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		gbsizer_reports.Add( self.m_staticText34, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		_cbx_report_typesChoices = [ u"Responsive", u"Privileged", u"All" ]
		self._cbx_report_types = wx.ComboBox( self._panel_doc_tags, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_report_typesChoices, wx.CB_READONLY|wx.CB_SORT )
		self._cbx_report_types.SetSelection( 0 )
		gbsizer_reports.Add( self._cbx_report_types, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_review_gen_report = wx.Button( self._panel_doc_tags, wx.ID_ANY, u"Generate Report", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_reports.Add( self._btn_review_gen_report, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		sbsizer_reports.Add( gbsizer_reports, 1, wx.EXPAND, 5 )
		
		
		bsizer_doc_tags.Add( sbsizer_reports, 0, wx.EXPAND, 5 )
		
		
		self._panel_doc_tags.SetSizer( bsizer_doc_tags )
		self._panel_doc_tags.Layout()
		bsizer_doc_tags.Fit( self._panel_doc_tags )
		gbsizer_review.Add( self._panel_doc_tags, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline11 = wx.StaticLine( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_review.Add( self.m_staticline11, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 4 ), wx.EXPAND |wx.ALL, 5 )
		
		bsizer_review_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_review_goback = wx.Button( self._panel_review, wx.ID_ANY, u"Go Back", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_review_buttons.Add( self._btn_review_goback, 0, wx.ALL, 5 )
		
		self._btn_review_exit = wx.Button( self._panel_review, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsizer_review_buttons.Add( self._btn_review_exit, 0, wx.ALL, 5 )
		
		
		gbsizer_review.Add( bsizer_review_buttons, wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )
		
		self.m_staticText21 = wx.StaticText( self._panel_review, wx.ID_ANY, u"This tab shows the documents samples produced based on your sampler specifications. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		self.m_staticText21.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVECAPTION ) )
		
		gbsizer_review.Add( self.m_staticText21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self._sl_header3 = wx.StaticLine( self._panel_review, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_review.Add( self._sl_header3, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 4 ), wx.EXPAND |wx.ALL, 5 )
		
		
		sbsizer_review.Add( gbsizer_review, 0, wx.EXPAND, 5 )
		
		
		self._panel_review.SetSizer( sbsizer_review )
		self._panel_review.Layout()
		sbsizer_review.Fit( self._panel_review )
		self.nb_config_sampler.AddPage( self._panel_review, u"Document Review", False )
		self.sw_sampling = wx.ScrolledWindow( self.nb_config_sampler, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.sw_sampling.SetScrollRate( 5, 5 )
		bsizer_sampling = wx.BoxSizer( wx.VERTICAL )
		
		bsizer_samples = wx.BoxSizer( wx.VERTICAL )
		
		self._panel_samples = wx.Panel( self.sw_sampling, wx.ID_ANY, wx.DefaultPosition, wx.Size( 950,300 ), wx.TAB_TRAVERSAL )
		self._panel_samples.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		sbsizer_samples = wx.StaticBoxSizer( wx.StaticBox( self._panel_samples, wx.ID_ANY, u"Samples" ), wx.VERTICAL )
		
		gbsizer_sampler = wx.GridBagSizer( 0, 10 )
		gbsizer_sampler.SetFlexibleDirection( wx.BOTH )
		gbsizer_sampler.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_docs_to_be_reviewed = wx.StaticText( self._panel_samples, wx.ID_ANY, u"Documents to be Reviewed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_docs_to_be_reviewed.Wrap( -1 )
		self._st_docs_to_be_reviewed.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_sampler.Add( self._st_docs_to_be_reviewed, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self._tc_results = wx.TreeCtrl( self._panel_samples, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_LINES_AT_ROOT|wx.TR_SINGLE|wx.HSCROLL|wx.SUNKEN_BORDER )
		self._tc_results.SetMinSize( wx.Size( 500,250 ) )
		
		gbsizer_sampler.Add( self._tc_results, wx.GBPosition( 1, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
		
		self._tag_list = wx.ListCtrl( self._panel_samples, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER )
		self._tag_list.SetMinSize( wx.Size( 220,150 ) )
		
		gbsizer_sampler.Add( self._tag_list, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_csizer_tags = wx.BoxSizer( wx.HORIZONTAL )
		
		self._lbl_tag = wx.StaticText( self._panel_samples, wx.ID_ANY, u"File Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._lbl_tag.Wrap( -1 )
		self._lbl_tag.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		_csizer_tags.Add( self._lbl_tag, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self._btn_add_tag = wx.Button( self._panel_samples, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size( 20,20 ), 0|wx.SUNKEN_BORDER )
		_csizer_tags.Add( self._btn_add_tag, 0, wx.ALL, 5 )
		
		self._btn_remove_tag = wx.Button( self._panel_samples, wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 20,20 ), 0|wx.SUNKEN_BORDER )
		_csizer_tags.Add( self._btn_remove_tag, 0, wx.ALL, 5 )
		
		
		gbsizer_sampler.Add( _csizer_tags, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.LEFT, 0 )
		
		gbsizer_logger = wx.GridBagSizer( 0, 0 )
		gbsizer_logger.SetFlexibleDirection( wx.BOTH )
		gbsizer_logger.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText11 = wx.StaticText( self._panel_samples, wx.ID_ANY, u"Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( 9, 72, 93, 90, False, wx.EmptyString ) )
		
		gbsizer_logger.Add( self.m_staticText11, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )
		
		self._btn_log_files = wx.Button( self._panel_samples, wx.ID_ANY, u"Save Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_logger.Add( self._btn_log_files, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_tag_typeChoices = [ u"Reviewed", u"Responsive", u"All" ]
		self._cbx_tag_type = wx.ComboBox( self._panel_samples, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_tag_typeChoices, wx.CB_READONLY|wx.CB_SORT )
		self._cbx_tag_type.SetSelection( 0 )
		gbsizer_logger.Add( self._cbx_tag_type, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_clear_tags = wx.Button( self._panel_samples, wx.ID_ANY, u"Clear All Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_logger.Add( self._btn_clear_tags, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		gbsizer_sampler.Add( gbsizer_logger, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 0 )
		
		
		sbsizer_samples.Add( gbsizer_sampler, 0, wx.EXPAND, 5 )
		
		
		self._panel_samples.SetSizer( sbsizer_samples )
		self._panel_samples.Layout()
		bsizer_samples.Add( self._panel_samples, 0, wx.EXPAND |wx.ALL, 10 )
		
		
		bsizer_sampling.Add( bsizer_samples, 0, wx.EXPAND, 5 )
		
		
		self.sw_sampling.SetSizer( bsizer_sampling )
		self.sw_sampling.Layout()
		bsizer_sampling.Fit( self.sw_sampling )
		self.nb_config_sampler.AddPage( self.sw_sampling, u"Sampled Output", False )
		
		bsizer_main.Add( self.nb_config_sampler, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bsizer_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self._on_appln_close )
		self.Bind( wx.EVT_MENU, self._on_mitem_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_mitem_exit, id = self._mitem_exit.GetId() )
		self.nb_config_sampler.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_nb_page_changed )
		self._btn_io_sel_data_dir.Bind( wx.EVT_BUTTON, self._on_click_io_sel_data_dir )
		self._btn_io_sel_output_dir.Bind( wx.EVT_BUTTON, self._on_click_io_sel_output_dir )
		self._btn_io_next.Bind( wx.EVT_BUTTON, self._on_click_io_next )
		self._cbx_confidence_levels.Bind( wx.EVT_COMBOBOX, self._on_confidence_changed )
		self._tc_confidence_interval.Bind( wx.EVT_KEY_UP, self._on_precision_changed )
		self._btn_cl_goback.Bind( wx.EVT_BUTTON, self._on_click_cl_goback )
		self._btn_cl_next.Bind( wx.EVT_BUTTON, self._on_click_cl_next )
		self._btn_copy_files.Bind( wx.EVT_BUTTON, self._on_click_copy_files )
		self._btn_out_go_to_review.Bind( wx.EVT_BUTTON, self._on_click_out_go_to_review )
		self._btn_out_goback.Bind( wx.EVT_BUTTON, self._on_click_out_goback )
		self._btn_out_exit.Bind( wx.EVT_BUTTON, self._on_click_out_exit )
		self._btn_review_clear_all_tags.Bind( wx.EVT_BUTTON, self._on_click_clear_all_doc_tags )
		self._lc_review.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self._on_review_list_item_activated )
		self._lc_review.Bind( wx.EVT_LIST_ITEM_SELECTED, self._on_review_list_item_selected )
		self._chbx_doc_relevant.Bind( wx.EVT_CHECKBOX, self._on_check_box_doc_relevant )
		self._chbx_doc_privileged.Bind( wx.EVT_CHECKBOX, self._on_check_box_doc_privileged )
		self._btn_review_gen_report.Bind( wx.EVT_BUTTON, self._on_click_review_gen_report )
		self._btn_review_goback.Bind( wx.EVT_BUTTON, self._on_click_review_goback )
		self._btn_review_exit.Bind( wx.EVT_BUTTON, self._on_click_review_exit )
		self._tc_results.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self._on_activated_file )
		self._tc_results.Bind( wx.EVT_TREE_SEL_CHANGED, self._on_select_file )
		self._tag_list.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_edit_status )
		self._btn_add_tag.Bind( wx.EVT_BUTTON, self._on_add_tag )
		self._btn_remove_tag.Bind( wx.EVT_BUTTON, self._on_remove_tag )
		self._btn_log_files.Bind( wx.EVT_BUTTON, self._on_click_log_details )
		self._btn_clear_tags.Bind( wx.EVT_BUTTON, self._on_clear_tags )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_appln_close( self, event ):
		event.Skip()
	
	def _on_mitem_about( self, event ):
		event.Skip()
	
	def _on_mitem_exit( self, event ):
		event.Skip()
	
	def _on_nb_page_changed( self, event ):
		event.Skip()
	
	def _on_click_io_sel_data_dir( self, event ):
		event.Skip()
	
	def _on_click_io_sel_output_dir( self, event ):
		event.Skip()
	
	def _on_click_io_next( self, event ):
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
	
	def _on_review_list_item_activated( self, event ):
		event.Skip()
	
	def _on_review_list_item_selected( self, event ):
		event.Skip()
	
	def _on_check_box_doc_relevant( self, event ):
		event.Skip()
	
	def _on_check_box_doc_privileged( self, event ):
		event.Skip()
	
	def _on_click_review_gen_report( self, event ):
		event.Skip()
	
	def _on_click_review_goback( self, event ):
		event.Skip()
	
	def _on_click_review_exit( self, event ):
		event.Skip()
	
	def _on_activated_file( self, event ):
		event.Skip()
	
	def _on_select_file( self, event ):
		event.Skip()
	
	def _on_edit_status( self, event ):
		event.Skip()
	
	def _on_add_tag( self, event ):
		event.Skip()
	
	def _on_remove_tag( self, event ):
		event.Skip()
	
	def _on_click_log_details( self, event ):
		event.Skip()
	
	def _on_clear_tags( self, event ):
		event.Skip()
	

###########################################################################
## Class TagDocumentDialog
###########################################################################

class TagDocumentDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Tag the Document", pos = wx.DefaultPosition, size = wx.Size( 250,150 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bsizer_doc_tags = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_doc_tags = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Select document tags" ), wx.VERTICAL )
		
		self._chbx_doc_relevant = wx.CheckBox( self, wx.ID_ANY, u"Relevant", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbsizer_doc_tags.Add( self._chbx_doc_relevant, 0, wx.ALL, 5 )
		
		self._chbx_doc_privileged = wx.CheckBox( self, wx.ID_ANY, u"Privileged", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbsizer_doc_tags.Add( self._chbx_doc_privileged, 0, wx.ALL, 5 )
		
		
		bsizer_doc_tags.Add( sbsizer_doc_tags, 1, wx.EXPAND, 10 )
		
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
		self._btn_add_tags.Bind( wx.EVT_BUTTON, self._on_click_add_tags )
		self._btn_clear_doc_tags.Bind( wx.EVT_BUTTON, self._on_click_clear_tags )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_click_add_tags( self, event ):
		event.Skip()
	
	def _on_click_clear_tags( self, event ):
		event.Skip()
	

