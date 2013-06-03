# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class SMARTeRGUI
###########################################################################

class SMARTeRGUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SMARTeR"), pos = wx.DefaultPosition, size = wx.Size( 1044,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.FRAME_SHAPED|wx.ICONIZE|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL, name = u"SMARTeR" )
		
		self.SetSizeHintsSz( wx.Size( 1000,600 ), wx.DefaultSize )
		
		self._satusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_help = wx.Menu()
		self._mitem_about = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_about )
		
		self._mitem_help = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_help )
		
		self._menubar.Append( self._menu_help, _(u"Application") ) 
		
		self.SetMenuBar( self._menubar )
		
		_bsizer_main = wx.BoxSizer( wx.VERTICAL )
		
		self._notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._panel_index = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_project = wx.StaticBoxSizer( wx.StaticBox( self._panel_index, wx.ID_ANY, _(u"Project Details") ), wx.VERTICAL )
		
		gbsizer_project = wx.GridBagSizer( 0, 0 )
		gbsizer_project.SetFlexibleDirection( wx.BOTH )
		gbsizer_project.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self._panel_index, wx.ID_ANY, _(u"Project Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_project_name = wx.TextCtrl( self._panel_index, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		gbsizer_project.Add( self._tc_project_name, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self._panel_index, wx.ID_ANY, _(u"Input Data Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText6, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self._panel_index, wx.ID_ANY, _(u"Project Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText7, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._application_dir_picker = wx.DirPickerCtrl( self._panel_index, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		gbsizer_project.Add( self._application_dir_picker, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._data_dir_picker = wx.DirPickerCtrl( self._panel_index, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE )
		gbsizer_project.Add( self._data_dir_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self._panel_index, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_project.Add( self.m_staticline3, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		self._btn_clear_project_details = wx.Button( self._panel_index, wx.ID_ANY, _(u"Clear"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_clear_project_details, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_index_data = wx.Button( self._panel_index, wx.ID_ANY, _(u"Index Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_index_data, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_project.Add( gbsizer_project, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( sbsizer_project, 0, wx.ALL, 10 )
		
		
		self._panel_index.SetSizer( bSizer5 )
		self._panel_index.Layout()
		self._notebook.AddPage( self._panel_index, _(u"Index Data"), False )
		self._panel_query = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._panel_query.SetMinSize( wx.Size( 950,300 ) )
		
		_bsizer_query = wx.BoxSizer( wx.VERTICAL )
		
		_sbsizer_sel_mdl = wx.StaticBoxSizer( wx.StaticBox( self._panel_query, wx.ID_ANY, _(u"Project Selection") ), wx.VERTICAL )
		
		_gbsizer_mdl = wx.GridBagSizer( 5, 5 )
		_gbsizer_mdl.SetFlexibleDirection( wx.BOTH )
		_gbsizer_mdl.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_select_mdl = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Select a Project"), wx.Point( -1,-1 ), wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_select_mdl.Wrap( -1 )
		_gbsizer_mdl.Add( self._st_select_mdl, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._file_picker_mdl = wx.FilePickerCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, _(u"Select Project"), u"*.cfg", wx.DefaultPosition, wx.Size( 300,-1 ), wx.FLP_OPEN )
		self._file_picker_mdl.SetMinSize( wx.Size( 300,30 ) )
		
		_gbsizer_mdl.Add( self._file_picker_mdl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_available_mdl = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Available indices"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_available_mdl.Wrap( -1 )
		_gbsizer_mdl.Add( self._st_available_mdl, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_available_mdl = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self._tc_available_mdl.SetMinSize( wx.Size( 300,-1 ) )
		
		_gbsizer_mdl.Add( self._tc_available_mdl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_mdl.AddGrowableCol( 3 )
		_gbsizer_mdl.AddGrowableRow( 2 )
		
		_sbsizer_sel_mdl.Add( _gbsizer_mdl, 1, wx.EXPAND, 10 )
		
		
		_bsizer_query.Add( _sbsizer_sel_mdl, 0, wx.ALL|wx.EXPAND, 10 )
		
		_sbsizer_query_model = wx.StaticBoxSizer( wx.StaticBox( self._panel_query, wx.ID_ANY, _(u"Query Processing") ), wx.VERTICAL )
		
		_gbsizer_query = wx.GridBagSizer( 5, 5 )
		_gbsizer_query.SetFlexibleDirection( wx.BOTH )
		_gbsizer_query.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_query = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Enter Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_query.Wrap( -1 )
		_gbsizer_query.Add( self._st_query, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query_input = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		_gbsizer_query.Add( self._tc_query_input, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_add_to_query = wx.Button( self._panel_query, wx.ID_ANY, _(u"Add To Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._btn_add_to_query, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_rbtn_compulsion_levelChoices = [ _(u"MUST"), _(u"MAY"), _(u"MUST_NOT") ]
		self._rbtn_compulsion_level = wx.RadioBox( self._panel_query, wx.ID_ANY, _(u"Compulsion Level"), wx.DefaultPosition, wx.DefaultSize, _rbtn_compulsion_levelChoices, 1, 0 )
		self._rbtn_compulsion_level.SetSelection( 0 )
		_gbsizer_query.Add( self._rbtn_compulsion_level, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_meta_typeChoices = []
		self._cbx_meta_type = wx.ComboBox( self._panel_query, wx.ID_ANY, _(u"Select Type"), wx.DefaultPosition, wx.DefaultSize, _cbx_meta_typeChoices, wx.CB_READONLY|wx.CB_SORT )
		_gbsizer_query.Add( self._cbx_meta_type, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,50 ), wx.TE_MULTILINE )
		_gbsizer_query.Add( self._tc_query, wx.GBPosition( 2, 1 ), wx.GBSpan( 2, 2 ), wx.ALL, 5 )
		
		self._btn_run_query = wx.Button( self._panel_query, wx.ID_ANY, _(u"Run Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._btn_run_query, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chbx_topic_search = wx.CheckBox( self._panel_query, wx.ID_ANY, _(u"Topic Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._chbx_topic_search, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chbx_facet_search = wx.CheckBox( self._panel_query, wx.ID_ANY, _(u"Facet Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._chbx_facet_search, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_use_model = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Select Search Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_use_model.Wrap( -1 )
		_gbsizer_query.Add( self._st_use_model, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_query.AddGrowableCol( 4 )
		_gbsizer_query.AddGrowableRow( 5 )
		
		_sbsizer_query_model.Add( _gbsizer_query, 1, wx.EXPAND, 10 )
		
		
		_bsizer_query.Add( _sbsizer_query_model, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		self._panel_query.SetSizer( _bsizer_query )
		self._panel_query.Layout()
		_bsizer_query.Fit( self._panel_query )
		self._notebook.AddPage( self._panel_query, _(u"Query"), True )
		self._panel_query_results = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._notebook.AddPage( self._panel_query_results, _(u"Results"), False )
		self._panel_preferences  = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_indexing = wx.StaticBoxSizer( wx.StaticBox( self._panel_preferences , wx.ID_ANY, _(u"Indexing Preferences") ), wx.VERTICAL )
		
		gbsizer_indexing = wx.GridBagSizer( 0, 0 )
		gbsizer_indexing.SetFlexibleDirection( wx.BOTH )
		gbsizer_indexing.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText8 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Number of Topics"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_num_topics = wx.TextCtrl( self._panel_preferences , wx.ID_ANY, _(u"50"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_num_topics.SetMaxLength( 3 ) 
		gbsizer_indexing.Add( self._tc_num_topics, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Number of Passes"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText9, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_num_passes = wx.TextCtrl( self._panel_preferences , wx.ID_ANY, _(u"1"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_num_passes.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_num_passes, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Minimum Token Frequency"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_min_token_freq = wx.TextCtrl( self._panel_preferences , wx.ID_ANY, _(u"1"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_min_token_freq.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_min_token_freq, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Minimum Token Length"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText11, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_min_token_len = wx.TextCtrl( self._panel_preferences , wx.ID_ANY, _(u"2"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_min_token_len.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_min_token_len, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"The below configurations are used for indexing and analysis of the documents given in the Data Folder \n(Index Data section). For indexing and analysis, we use Apache Lucene and the topic modeling methods \nsuch as TF-IDF, Latent Semantic Indexing, and Latent Dirichlet Allocation. Warning! Both of these \nmethods are highly time consuming."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		self.m_staticText12.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_indexing.Add( self.m_staticText12, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Tips"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_indexing.Add( self.m_staticText14, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self._panel_preferences , wx.ID_ANY, _(u"Number of Topics: This is a predefined value used for the topic modeling based analysis. \nIf the given documents are from very diverse backgrounds, use a higher value (> 50).\n\nNumber of Passes: It's a parameter used for the topic modeling algorithm. A higher value \ncan increase the quality of the determined topics, but it can increase the execution time. \n\nMinimum Token Frequency: The topic modeling algorithm ignores the tokens (unique words\nin the corpus) with a token count (in the whole document collection) less than this value. \n\nMinimum Token Length: The topic modeling algorithm ignores the tokens with a token length \nless than this value.   \n\n"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		self.m_staticText13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.m_staticText13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_indexing.Add( self.m_staticText13, wx.GBPosition( 1, 3 ), wx.GBSpan( 6, 1 ), wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self._panel_preferences , wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		gbsizer_indexing.Add( self.m_staticline2, wx.GBPosition( 0, 2 ), wx.GBSpan( 10, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self._panel_preferences , wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_indexing.Add( self.m_staticline1, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self._btn_reset_defaults = wx.Button( self._panel_preferences , wx.ID_ANY, _(u"Reset Defaults"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_indexing.Add( self._btn_reset_defaults, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_save_indexing_preferences = wx.Button( self._panel_preferences , wx.ID_ANY, _(u"Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_indexing.Add( self._btn_save_indexing_preferences, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_indexing.Add( gbsizer_indexing, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( sbsizer_indexing, 0, wx.ALL, 10 )
		
		
		self._panel_preferences .SetSizer( bSizer6 )
		self._panel_preferences .Layout()
		bSizer6.Fit( self._panel_preferences  )
		self._notebook.AddPage( self._panel_preferences , _(u"Preferences"), False )
		
		_bsizer_main.Add( self._notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( _bsizer_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self._on_menu_sel_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_men_sel_help, id = self._mitem_help.GetId() )
		self._notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_notebook_page_changed )
		self._btn_clear_project_details.Bind( wx.EVT_BUTTON, self._on_click_clear_project_details )
		self._btn_index_data.Bind( wx.EVT_BUTTON, self._on_click_index_data )
		self._file_picker_mdl.Bind( wx.EVT_FILEPICKER_CHANGED, self._on_file_change_mdl )
		self._btn_add_to_query.Bind( wx.EVT_BUTTON, self._on_click_add_to_query )
		self._btn_run_query.Bind( wx.EVT_BUTTON, self._on_click_run_query )
		self._chbx_topic_search.Bind( wx.EVT_CHECKBOX, self._on_chbx_topic_search )
		self._chbx_facet_search.Bind( wx.EVT_CHECKBOX, self._on_chbx_facet_search )
		self._btn_reset_defaults.Bind( wx.EVT_BUTTON, self._on_click_reset_defaults_indexing_preferences )
		self._btn_save_indexing_preferences.Bind( wx.EVT_BUTTON, self._on_click_save_indexing_preferences )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_menu_sel_about( self, event ):
		event.Skip()
	
	def _on_men_sel_help( self, event ):
		event.Skip()
	
	def _on_notebook_page_changed( self, event ):
		event.Skip()
	
	def _on_click_clear_project_details( self, event ):
		event.Skip()
	
	def _on_click_index_data( self, event ):
		event.Skip()
	
	def _on_file_change_mdl( self, event ):
		event.Skip()
	
	def _on_click_add_to_query( self, event ):
		event.Skip()
	
	def _on_click_run_query( self, event ):
		event.Skip()
	
	def _on_chbx_topic_search( self, event ):
		event.Skip()
	
	def _on_chbx_facet_search( self, event ):
		event.Skip()
	
	def _on_click_reset_defaults_indexing_preferences( self, event ):
		event.Skip()
	
	def _on_click_save_indexing_preferences( self, event ):
		event.Skip()
	

###########################################################################
## Class RatingControl
###########################################################################

class RatingControl ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Document Relevancy"), pos = wx.DefaultPosition, size = wx.Size( 361,167 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		_bsizer_rating_control = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Mark Document Ratings") ), wx.VERTICAL )
		
		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.btn_Submit = wx.Button( self, wx.ID_ANY, _(u"Submit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.btn_Submit, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self._rating_slider = wx.Slider( self, wx.ID_ANY, 0, 0, 10, wx.DefaultPosition, wx.Size( 300,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
		gbSizer5.Add( self._rating_slider, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbSizer5.Add( gbSizer5, 1, wx.EXPAND, 5 )
		
		
		_bsizer_rating_control.Add( sbSizer5, 1, wx.ALL|wx.EXPAND, 10 )
		
		
		self.SetSizer( _bsizer_rating_control )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btn_Submit.Bind( wx.EVT_BUTTON, self._on_btn_click_submit )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_btn_click_submit( self, event ):
		event.Skip()
	

