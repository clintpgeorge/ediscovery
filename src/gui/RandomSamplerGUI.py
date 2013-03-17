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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Random Sampler", pos = wx.DefaultPosition, size = wx.Size( 1024,800 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.HSCROLL|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 1024,800 ), wx.DefaultSize )
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
		self._cbx_confidence_levels = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_confidence_levelsChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
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
		
		self._btn_copy_files = wx.Button( self, wx.ID_ANY, u"Copy files", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_sampler_buttons.Add( self._btn_copy_files, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self._btn_exit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		_bsizer_sampler_buttons.Add( self._btn_exit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler.Add( _bsizer_sampler_buttons, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		gbsizer_sampler.AddGrowableCol( 3 )
		gbsizer_sampler.AddGrowableRow( 7 )
		
		sbsizer_sampler.Add( gbsizer_sampler, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		bsizer_main.Add( sbsizer_sampler, 0, wx.ALL|wx.EXPAND, 10 )
		
		bsizer_samples = wx.BoxSizer( wx.VERTICAL )
		
		self._panel_samples = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 950,300 ), wx.TAB_TRAVERSAL )
		self._panel_samples.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		
		sbsizer_samples = wx.StaticBoxSizer( wx.StaticBox( self._panel_samples, wx.ID_ANY, u"Samples" ), wx.VERTICAL )
		
		gbsizer_sampler = wx.GridBagSizer( 0, 10 )
		gbsizer_sampler.SetFlexibleDirection( wx.BOTH )
		gbsizer_sampler.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_docs_to_be_reviewed = wx.StaticText( self._panel_samples, wx.ID_ANY, u"Documents to be Reviewed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_docs_to_be_reviewed.Wrap( -1 )
		self._st_docs_to_be_reviewed.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_sampler.Add( self._st_docs_to_be_reviewed, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self._tc_results = wx.TreeCtrl( self._panel_samples, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_LINES_AT_ROOT|wx.TR_SINGLE|wx.SUNKEN_BORDER )
		self._tc_results.SetMinSize( wx.Size( 380,250 ) )
		
		gbsizer_sampler.Add( self._tc_results, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )
		
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
		
		self.m_staticText11 = wx.StaticText( self._panel_samples, wx.ID_ANY, u"Tag Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_logger.Add( self.m_staticText11, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )
		
		self._btn_log_files = wx.Button( self._panel_samples, wx.ID_ANY, u"Log Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_logger.Add( self._btn_log_files, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_tag_typeChoices = [ u"Reviewed", u"Responsive", u"All" ]
		self._cbx_tag_type = wx.ComboBox( self._panel_samples, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_tag_typeChoices, wx.CB_READONLY|wx.CB_SORT )
		self._cbx_tag_type.SetSelection( 0 )
		gbsizer_logger.Add( self._cbx_tag_type, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_clear_tags = wx.Button( self._panel_samples, wx.ID_ANY, u"Clear All Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_logger.Add( self._btn_clear_tags, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		gbsizer_logger.AddGrowableCol( 2 )
		gbsizer_logger.AddGrowableRow( 3 )
		
		gbsizer_sampler.Add( gbsizer_logger, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		gbsizer_sampler.AddGrowableCol( 3 )
		gbsizer_sampler.AddGrowableRow( 2 )
		
		sbsizer_samples.Add( gbsizer_sampler, 0, wx.EXPAND, 5 )
		
		
		self._panel_samples.SetSizer( sbsizer_samples )
		self._panel_samples.Layout()
		bsizer_samples.Add( self._panel_samples, 0, wx.EXPAND |wx.ALL, 10 )
		
		
		bsizer_main.Add( bsizer_samples, 0, wx.EXPAND, 5 )
		
		
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
		self._cbx_confidence_levels.Bind( wx.EVT_COMBOBOX, self._on_confidence_changed )
		self._tc_confidence_interval.Bind( wx.EVT_TEXT, self._on_precision_changed )
		self._btn_copy_files.Bind( wx.EVT_BUTTON, self._on_click_copy_files )
		self._btn_exit.Bind( wx.EVT_BUTTON, self._on_click_exit )
		self._tc_results.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self._on_activated_file )
		self._tc_results.Bind( wx.EVT_TREE_SEL_CHANGED, self._on_select_file )
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
	
	def _on_mitem_help( self, event ):
		event.Skip()
	
	def _on_mitem_exit( self, event ):
		event.Skip()
	
	def _on_click_sel_data_dir( self, event ):
		event.Skip()
	
	def _on_click_sel_output_dir( self, event ):
		event.Skip()
	
	def _on_confidence_changed( self, event ):
		event.Skip()
	
	def _on_precision_changed( self, event ):
		event.Skip()
	
	def _on_click_copy_files( self, event ):
		event.Skip()
	
	def _on_click_exit( self, event ):
		event.Skip()
	
	def _on_activated_file( self, event ):
		event.Skip()
	
	def _on_select_file( self, event ):
		event.Skip()
	
	def _on_add_tag( self, event ):
		event.Skip()
	
	def _on_remove_tag( self, event ):
		event.Skip()
	
	def _on_click_log_details( self, event ):
		event.Skip()
	
	def _on_clear_tags( self, event ):
		event.Skip()
	

