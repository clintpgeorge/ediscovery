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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SMARTeR"), pos = wx.DefaultPosition, size = wx.Size( 1000,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.FRAME_SHAPED|wx.ICONIZE|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL, name = u"SMARTeR" )
		
		self.SetSizeHintsSz( wx.Size( 1000,600 ), wx.DefaultSize )
		
		self._satusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_query = wx.Menu()
		self._mitem_sel_mdl_path = wx.MenuItem( self._menu_query, wx.ID_ANY, _(u"Select Model"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_query.AppendItem( self._mitem_sel_mdl_path )
		
		self._mitem_exit = wx.MenuItem( self._menu_query, wx.ID_ANY, _(u"Exit"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_query.AppendItem( self._mitem_exit )
		
		self._menubar.Append( self._menu_query, _(u"Query") ) 
		
		self._menu_index = wx.Menu()
		self._mitem_sel_dir = wx.MenuItem( self._menu_index, wx.ID_ANY, _(u"Select directory to index"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_index.AppendItem( self._mitem_sel_dir )
		
		self._menubar.Append( self._menu_index, _(u"Index") ) 
		
		self._menu_help = wx.Menu()
		self._mitem_about = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_about )
		
		self._mitem_help = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_help )
		
		self._menubar.Append( self._menu_help, _(u"Help") ) 
		
		self.SetMenuBar( self._menubar )
		
		self._toolbar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self._toolbar.AddLabelTool( wx.ID_ANY, _(u"Select"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, _(u"Select Model"), wx.EmptyString, None ) 
		
		self._toolbar.AddLabelTool( wx.ID_ANY, _(u"Exit"), wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, _(u"Exit"), wx.EmptyString, None ) 
		
		self._toolbar.Realize() 
		
		_bsizer_main = wx.BoxSizer( wx.VERTICAL )
		
		self._notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._panel_query = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._panel_query.SetMinSize( wx.Size( 950,300 ) )
		
		_bsizer_query = wx.BoxSizer( wx.VERTICAL )
		
		_sbsizer_sel_mdl = wx.StaticBoxSizer( wx.StaticBox( self._panel_query, wx.ID_ANY, _(u"Model") ), wx.VERTICAL )
		
		_gbsizer_mdl = wx.GridBagSizer( 5, 5 )
		_gbsizer_mdl.SetFlexibleDirection( wx.BOTH )
		_gbsizer_mdl.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_select_mdl = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Select Model"), wx.Point( -1,-1 ), wx.DefaultSize, wx.ALIGN_LEFT )
		self._st_select_mdl.Wrap( -1 )
		_gbsizer_mdl.Add( self._st_select_mdl, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._file_picker_mdl = wx.FilePickerCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, _(u"Select Model"), u"*.ini", wx.DefaultPosition, wx.Size( 300,-1 ), wx.FLP_OPEN )
		self._file_picker_mdl.SetMinSize( wx.Size( 300,30 ) )
		
		_gbsizer_mdl.Add( self._file_picker_mdl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_available_mdl = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Available indices"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_available_mdl.Wrap( -1 )
		_gbsizer_mdl.Add( self._st_available_mdl, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_available_mdl = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.STATIC_BORDER|wx.SUNKEN_BORDER )
		self._tc_available_mdl.SetMinSize( wx.Size( 300,-1 ) )
		
		_gbsizer_mdl.Add( self._tc_available_mdl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_mdl.AddGrowableCol( 3 )
		_gbsizer_mdl.AddGrowableRow( 2 )
		
		_sbsizer_sel_mdl.Add( _gbsizer_mdl, 1, wx.EXPAND, 10 )
		
		
		_bsizer_query.Add( _sbsizer_sel_mdl, 0, wx.ALL|wx.EXPAND, 10 )
		
		_sbsizer_query_model = wx.StaticBoxSizer( wx.StaticBox( self._panel_query, wx.ID_ANY, _(u"Query") ), wx.VERTICAL )
		
		_gbsizer_query = wx.GridBagSizer( 5, 5 )
		_gbsizer_query.SetFlexibleDirection( wx.BOTH )
		_gbsizer_query.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_query = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Enter query"), wx.DefaultPosition, wx.DefaultSize, 0 )
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
		self._cbx_meta_type = wx.ComboBox( self._panel_query, wx.ID_ANY, _(u"Select Type"), wx.DefaultPosition, wx.DefaultSize, _cbx_meta_typeChoices, wx.CB_SORT )
		_gbsizer_query.Add( self._cbx_meta_type, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,50 ), wx.TE_MULTILINE )
		_gbsizer_query.Add( self._tc_query, wx.GBPosition( 2, 1 ), wx.GBSpan( 2, 2 ), wx.ALL, 5 )
		
		self._btn_run_query = wx.Button( self._panel_query, wx.ID_ANY, _(u"Run Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._btn_run_query, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chbx_topic_mdl = wx.CheckBox( self._panel_query, wx.ID_ANY, _(u"topic model"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._chbx_topic_mdl, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chbx_meta_data = wx.CheckBox( self._panel_query, wx.ID_ANY, _(u"metadata"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query.Add( self._chbx_meta_data, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_use_model = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Search type"), wx.DefaultPosition, wx.DefaultSize, 0 )
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
		self._panel_index = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		_bsizer_index = wx.BoxSizer( wx.VERTICAL )
		
		
		self._panel_index.SetSizer( _bsizer_index )
		self._panel_index.Layout()
		_bsizer_index.Fit( self._panel_index )
		self._notebook.AddPage( self._panel_index, _(u"Index files"), False )
		self._panel_query_results = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._notebook.AddPage( self._panel_query_results, _(u"Results"), False )
		
		_bsizer_main.Add( self._notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( _bsizer_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self._on_menu_sel_mdl_path, id = self._mitem_sel_mdl_path.GetId() )
		self.Bind( wx.EVT_MENU, self._on_menu_sel_exit, id = self._mitem_exit.GetId() )
		self.Bind( wx.EVT_MENU, self._on_menu_sel_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_men_sel_help, id = self._mitem_help.GetId() )
		self._file_picker_mdl.Bind( wx.EVT_FILEPICKER_CHANGED, self._on_file_change_mdl )
		self._btn_add_to_query.Bind( wx.EVT_BUTTON, self._on_click_add_to_query )
		self._btn_run_query.Bind( wx.EVT_BUTTON, self._on_click_run_query )
		self._chbx_topic_mdl.Bind( wx.EVT_CHECKBOX, self._on_sel_topic_mdl )
		self._chbx_meta_data.Bind( wx.EVT_CHECKBOX, self._on_sel_metadata )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_menu_sel_mdl_path( self, event ):
		event.Skip()
	
	def _on_menu_sel_exit( self, event ):
		event.Skip()
	
	def _on_menu_sel_about( self, event ):
		event.Skip()
	
	def _on_men_sel_help( self, event ):
		event.Skip()
	
	def _on_file_change_mdl( self, event ):
		event.Skip()
	
	def _on_click_add_to_query( self, event ):
		event.Skip()
	
	def _on_click_run_query( self, event ):
		event.Skip()
	
	def _on_sel_topic_mdl( self, event ):
		event.Skip()
	
	def _on_sel_metadata( self, event ):
		event.Skip()
	

