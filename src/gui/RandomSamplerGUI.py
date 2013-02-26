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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Random Sampler", pos = wx.DefaultPosition, size = wx.Size( 1000,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.HSCROLL|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 1000,500 ), wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self._statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_appln = wx.Menu()
		self._mitem_about = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_about )
		
		self._mitem_help = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_help )
		
		self._mitem_exit = wx.MenuItem( self._menu_appln, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_appln.AppendItem( self._mitem_exit )
		
		self._menubar.Append( self._menu_appln, u"Application" ) 
		
		self.SetMenuBar( self._menubar )
		
		bsizer_main = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_sampler = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Sampler" ), wx.VERTICAL )
		
		gbsizer_sampler = wx.GridBagSizer( 2, 5 )
		gbsizer_sampler.SetFlexibleDirection( wx.BOTH )
		gbsizer_sampler.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_header = wx.StaticText( self, wx.ID_ANY, u"This application randomly samples the files inside the data folder and copies them to the sampled output folder. \nSample size is calculated by the given confidence interval and level. ", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
		self._st_header.Wrap( -1 )
		self._st_header.SetFont( wx.Font( 9, 72, 90, 91, False, wx.EmptyString ) )
		self._st_header.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self._st_header.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler.Add( self._st_header, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 3 ), wx.ALL, 5 )
		
		self._sl_header = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler.Add( self._sl_header, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_data_folder = wx.StaticText( self, wx.ID_ANY, u"Data folder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_data_folder.Wrap( -1 )
		self._st_data_folder.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler.Add( self._st_data_folder, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_data_dir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._tc_data_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		self._tc_data_dir.SetMinSize( wx.Size( 300,30 ) )
		
		gbsizer_sampler.Add( self._tc_data_dir, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_sel_data_dir = wx.Button( self, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_sampler.Add( self._btn_sel_data_dir, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_output_dir = wx.StaticText( self, wx.ID_ANY, u"Sampled output", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_output_dir.Wrap( -1 )
		self._st_output_dir.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self._st_output_dir.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_sampler.Add( self._st_output_dir, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_output_dir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,30 ), 0 )
		self._tc_output_dir.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler.Add( self._tc_output_dir, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_sel_output_dir = wx.Button( self, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_sampler.Add( self._btn_sel_output_dir, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_level = wx.StaticText( self, wx.ID_ANY, u"Confidence level (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_level.Wrap( -1 )
		self._st_confidence_level.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler.Add( self._st_confidence_level, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_confidence_levelsChoices = []
		self._cbx_confidence_levels = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_confidence_levelsChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT )
		self._cbx_confidence_levels.SetSelection( 0 )
		self._cbx_confidence_levels.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler.Add( self._cbx_confidence_levels, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.TOP, 5 )
		
		self._tc_confidence_interval = wx.TextCtrl( self, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 30,25 ), 0 )
		self._tc_confidence_interval.SetMaxLength( 2 ) 
		self._tc_confidence_interval.SetFont( wx.Font( 9, 70, 90, 90, False, wx.EmptyString ) )
		
		gbsizer_sampler.Add( self._tc_confidence_interval, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_confidence_interval = wx.StaticText( self, wx.ID_ANY, u"Confidence interval (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_confidence_interval.Wrap( -1 )
		self._st_confidence_interval.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		gbsizer_sampler.Add( self._st_confidence_interval, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_samples = wx.StaticText( self, wx.ID_ANY, u"0 samples found", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_num_samples.Wrap( -1 )
		self._st_num_samples.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_samples.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler.Add( self._st_num_samples, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._st_num_data_dir_files = wx.StaticText( self, wx.ID_ANY, u"0 files found", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_num_data_dir_files.Wrap( -1 )
		self._st_num_data_dir_files.SetFont( wx.Font( 8, 72, 94, 90, False, wx.EmptyString ) )
		self._st_num_data_dir_files.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_sampler.Add( self._st_num_data_dir_files, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALIGN_TOP|wx.LEFT, 5 )
		
		self._sl_tailer = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_sampler.Add( self._sl_tailer, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )
		
		_bsizer_sampler_buttons = wx.BoxSizer( wx.HORIZONTAL )
		
		self._btn_run_sampler = wx.Button( self, wx.ID_ANY, u"Run sampler", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_sampler_buttons.Add( self._btn_run_sampler, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self._btn_copy_files = wx.Button( self, wx.ID_ANY, u"Copy files", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_sampler_buttons.Add( self._btn_copy_files, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_exit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_sampler_buttons.Add( self._btn_exit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler.Add( _bsizer_sampler_buttons, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler.AddGrowableCol( 3 )
		gbsizer_sampler.AddGrowableRow( 7 )
		
		sbsizer_sampler.Add( gbsizer_sampler, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		bsizer_main.Add( sbsizer_sampler, 0, wx.ALL|wx.EXPAND, 10 )
		
		sbsizer_samples = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Samples" ), wx.VERTICAL )
		
		self._panel_samples = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 950,300 ), wx.TAB_TRAVERSAL )
		sbsizer_samples.Add( self._panel_samples, 0, wx.EXPAND |wx.ALL, 10 )
		
		
		bsizer_main.Add( sbsizer_samples, 1, wx.ALL|wx.EXPAND, 10 )
		
		
		self.SetSizer( bsizer_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self._on_appln_close )
		self.Bind( wx.EVT_MENU, self._on_mitem_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_mitem_help, id = self._mitem_help.GetId() )
		self.Bind( wx.EVT_MENU, self._on_mitem_exit, id = self._mitem_exit.GetId() )
		self._btn_sel_data_dir.Bind( wx.EVT_BUTTON, self._on_click_sel_data_dir )
		self._btn_sel_output_dir.Bind( wx.EVT_BUTTON, self._on_click_sel_output_dir )
		self._btn_run_sampler.Bind( wx.EVT_BUTTON, self._on_click_run_sampler )
		self._btn_copy_files.Bind( wx.EVT_BUTTON, self._on_click_copy_files )
		self._btn_exit.Bind( wx.EVT_BUTTON, self._on_click_exit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_appln_close( self, event ):
		event.Skip()
	
	def _on_mitem_about( self, event ):
		event.Skip()
	
	def _on_mitem_help( self, event ):
		event.Skip()
	
	def _on_mitem_exit( self, event ):
		event.Skip()
	
	def _on_click_sel_data_dir( self, event ):
		event.Skip()
	
	def _on_click_sel_output_dir( self, event ):
		event.Skip()
	
	def _on_click_run_sampler( self, event ):
		event.Skip()
	
	def _on_click_copy_files( self, event ):
		event.Skip()
	
	def _on_click_exit( self, event ):
		event.Skip()
	

