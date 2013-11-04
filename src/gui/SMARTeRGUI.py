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
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self._satusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self._menubar = wx.MenuBar( 0 )
		self._menu_help = wx.Menu()
		self._mitem_preferences = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"Application Preferences"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_preferences )
		
		self._mitem_about = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_about )
		
		self._mitem_help = wx.MenuItem( self._menu_help, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
		self._menu_help.AppendItem( self._mitem_help )
		
		self._menubar.Append( self._menu_help, _(u"Application") ) 
		
		self.SetMenuBar( self._menubar )
		
		_bsizer_main = wx.BoxSizer( wx.VERTICAL )
		
		self._notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._notebook.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self._panel_index = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( 40,-1 ), wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_project = wx.StaticBoxSizer( wx.StaticBox( self._panel_index, wx.ID_ANY, _(u"Project Details") ), wx.VERTICAL )
		
		gbsizer_project = wx.GridBagSizer( 0, 0 )
		gbsizer_project.SetFlexibleDirection( wx.BOTH )
		gbsizer_project.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self._panel_index, wx.ID_ANY, _(u"Project Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self._panel_index, wx.ID_ANY, _(u"Input Data Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText6, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_data_fld = wx.TextCtrl( self._panel_index, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_READONLY )
		gbsizer_project.Add( self._tc_data_fld, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self._panel_index, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_project.Add( self.m_staticline3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		self._btn_clear_project_details = wx.Button( self._panel_index, wx.ID_ANY, _(u"Clear"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_clear_project_details, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_index_data = wx.Button( self._panel_index, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_index_data, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_project_titleChoices = []
		self._cbx_project_title = wx.ComboBox( self._panel_index, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), _cbx_project_titleChoices, wx.CB_DROPDOWN|wx.CB_READONLY|wx.TE_PROCESS_ENTER )
		gbsizer_project.Add( self._cbx_project_title, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_new_project = wx.Button( self._panel_index, wx.ID_ANY, _(u"New Project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_new_project, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_project.Add( gbsizer_project, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( sbsizer_project, 0, wx.ALL, 10 )
		
		
		self._panel_index.SetSizer( bSizer5 )
		self._panel_index.Layout()
		self._notebook.AddPage( self._panel_index, _(u"Index Data"), True )
		self._panel_query = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self._panel_query.SetMinSize( wx.Size( 950,300 ) )
		
		_bsizer_query = wx.BoxSizer( wx.VERTICAL )
		
		_sbsizer_query_model1 = wx.StaticBoxSizer( wx.StaticBox( self._panel_query, wx.ID_ANY, _(u"Query Processing") ), wx.VERTICAL )
		
		_gbsizer_query1 = wx.GridBagSizer( 5, 5 )
		_gbsizer_query1.SetFlexibleDirection( wx.BOTH )
		_gbsizer_query1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._st_query1 = wx.StaticText( self._panel_query, wx.ID_ANY, _(u"Enter Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_query1.Wrap( -1 )
		_gbsizer_query1.Add( self._st_query1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query_input1 = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		_gbsizer_query1.Add( self._tc_query_input1, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_add_to_query1 = wx.Button( self._panel_query, wx.ID_ANY, _(u"Add To Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query1.Add( self._btn_add_to_query1, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_meta_type1Choices = []
		self._cbx_meta_type1 = wx.ComboBox( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_meta_type1Choices, wx.CB_READONLY|wx.CB_SORT )
		_gbsizer_query1.Add( self._cbx_meta_type1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query1 = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,150 ), wx.TE_MULTILINE )
		_gbsizer_query1.Add( self._tc_query1, wx.GBPosition( 2, 1 ), wx.GBSpan( 2, 2 ), wx.ALL, 5 )
		
		self._btn_run_query1 = wx.Button( self._panel_query, wx.ID_ANY, _(u"Start Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_query1.Add( self._btn_run_query1, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_meta_type2Choices = [ _(u"AND"), _(u"OR"), _(u"NOT") ]
		self._cbx_meta_type2 = wx.ComboBox( self._panel_query, wx.ID_ANY, _(u"OR"), wx.DefaultPosition, wx.Size( 80,-1 ), _cbx_meta_type2Choices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self._cbx_meta_type2.SetSelection( 1 )
		_gbsizer_query1.Add( self._cbx_meta_type2, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_query = wx.TextCtrl( self._panel_query, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,50 ), wx.TE_MULTILINE )
		self._tc_query.Hide()
		
		_gbsizer_query1.Add( self._tc_query, wx.GBPosition( 5, 1 ), wx.GBSpan( 2, 2 ), wx.ALL, 5 )
		
		
		_sbsizer_query_model1.Add( _gbsizer_query1, 1, wx.EXPAND, 10 )
		
		
		_bsizer_query.Add( _sbsizer_query_model1, 0, wx.ALL|wx.EXPAND, 10 )
		
		
		self._panel_query.SetSizer( _bsizer_query )
		self._panel_query.Layout()
		_bsizer_query.Fit( self._panel_query )
		self._notebook.AddPage( self._panel_query, _(u"Query"), False )
		self._panel_feedback = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self._panel_feedback, wx.ID_ANY, _(u"Feedback") ), wx.VERTICAL )
		
		self.m_staticText32 = wx.StaticText( self._panel_feedback, wx.ID_ANY, _(u"Please review all 100 documents to increase the accuracy of document retrieval."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		self.m_staticText32.SetFont( wx.Font( 8, 74, 93, 92, False, "Tahoma" ) )
		
		sbSizer7.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._panel_feedback_doc = wx.Panel( self._panel_feedback, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,200 ), wx.TAB_TRAVERSAL )
		gbSizer8.Add( self._panel_feedback_doc, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		bSizer81 = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_responsiveChoices = [ _(u"Responsive"), _(u"Unresponsive"), _(u"Uncertain") ]
		self._rbx_responsive = wx.RadioBox( self._panel_feedback, wx.ID_ANY, _(u"Feedback"), wx.DefaultPosition, wx.DefaultSize, _rbx_responsiveChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_responsive.SetSelection( 2 )
		bSizer81.Add( self._rbx_responsive, 0, wx.ALL, 5 )
		
		self._btn_recalculate_results = wx.Button( self._panel_feedback, wx.ID_ANY, _(u"SMARTeR Ranking"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self._btn_recalculate_results, 0, wx.ALL, 5 )
		
		
		gbSizer8.Add( bSizer81, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		
		sbSizer7.Add( gbSizer8, 1, wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self._doc_feedback_preview = wx.TextCtrl( self._panel_feedback, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self._doc_feedback_preview.SetMinSize( wx.Size( 1010,225 ) )
		
		bSizer10.Add( self._doc_feedback_preview, 0, wx.ALL, 5 )
		
		
		sbSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer8.Add( sbSizer7, 1, wx.EXPAND, 5 )
		
		
		self._panel_feedback.SetSizer( bSizer8 )
		self._panel_feedback.Layout()
		bSizer8.Fit( self._panel_feedback )
		self._notebook.AddPage( self._panel_feedback, _(u"Document Feedback"), False )
		self._panel_query_results = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_query_results.Hide()
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self._panel_query_results, wx.ID_ANY, _(u"Query Results") ), wx.VERTICAL )
		
		self.m_staticText40 = wx.StaticText( self._panel_query_results, wx.ID_ANY, _(u"Please reveiw as many documents as possible, click on continue to sample documents or click on update query to refine search terms."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		self.m_staticText40.SetFont( wx.Font( 8, 74, 93, 92, False, "Tahoma" ) )
		
		sbSizer11.Add( self.m_staticText40, 0, wx.ALL, 5 )
		
		gbSizer34 = wx.GridBagSizer( 0, 0 )
		gbSizer34.SetFlexibleDirection( wx.BOTH )
		gbSizer34.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gbSizer29 = wx.GridBagSizer( 0, 0 )
		gbSizer29.SetFlexibleDirection( wx.BOTH )
		gbSizer29.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._panel_res = wx.Panel( self._panel_query_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_res.SetMinSize( wx.Size( 350,200 ) )
		
		gbSizer29.Add( self._panel_res, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self._panel_unres = wx.Panel( self._panel_query_results, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_unres.SetMinSize( wx.Size( 350,200 ) )
		
		gbSizer29.Add( self._panel_unres, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText55 = wx.StaticText( self._panel_query_results, wx.ID_ANY, _(u"Responsive Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		self.m_staticText55.SetFont( wx.Font( 8, 74, 90, 92, False, "Tahoma" ) )
		
		gbSizer29.Add( self.m_staticText55, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self._panel_query_results, wx.ID_ANY, _(u"Unresponsive Files"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		self.m_staticText56.SetFont( wx.Font( 8, 74, 90, 92, False, "Tahoma" ) )
		
		gbSizer29.Add( self.m_staticText56, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		bSizer811 = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_feedack_resChoices = [ _(u"Responsive"), _(u"Unresponsive"), _(u"Uncertain") ]
		self._rbx_feedack_res = wx.RadioBox( self._panel_query_results, wx.ID_ANY, _(u"Feedback"), wx.DefaultPosition, wx.DefaultSize, _rbx_feedack_resChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_feedack_res.SetSelection( 2 )
		bSizer811.Add( self._rbx_feedack_res, 0, wx.ALL, 5 )
		
		self._btn_next_res_res = wx.Button( self._panel_query_results, wx.ID_ANY, _(u">"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer811.Add( self._btn_next_res_res, 0, wx.ALL, 5 )
		
		self._btn_prev_res_res = wx.Button( self._panel_query_results, wx.ID_ANY, _(u"<"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer811.Add( self._btn_prev_res_res, 0, wx.ALL, 5 )
		
		
		gbSizer29.Add( bSizer811, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		bSizer812 = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_feedack_unresChoices = [ _(u"Responsive"), _(u"Unresponsive"), _(u"Uncertain") ]
		self._rbx_feedack_unres = wx.RadioBox( self._panel_query_results, wx.ID_ANY, _(u"Feedback"), wx.DefaultPosition, wx.DefaultSize, _rbx_feedack_unresChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_feedack_unres.SetSelection( 2 )
		bSizer812.Add( self._rbx_feedack_unres, 0, wx.ALL, 5 )
		
		self._btn_net_res_unres = wx.Button( self._panel_query_results, wx.ID_ANY, _(u">"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer812.Add( self._btn_net_res_unres, 0, wx.ALL, 5 )
		
		self._btn_prev_res_unres = wx.Button( self._panel_query_results, wx.ID_ANY, _(u"<"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer812.Add( self._btn_prev_res_unres, 0, wx.ALL, 5 )
		
		
		gbSizer29.Add( bSizer812, wx.GBPosition( 1, 5 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		
		gbSizer34.Add( gbSizer29, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		gbSizer30 = wx.GridBagSizer( 0, 0 )
		gbSizer30.SetFlexibleDirection( wx.BOTH )
		gbSizer30.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._tc_file_preview_pane = wx.TextCtrl( self._panel_query_results, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self._tc_file_preview_pane.SetMinSize( wx.Size( 1000,150 ) )
		
		gbSizer30.Add( self._tc_file_preview_pane, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText54 = wx.StaticText( self._panel_query_results, wx.ID_ANY, _(u"File Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )
		self.m_staticText54.SetFont( wx.Font( 8, 74, 93, 92, False, "Tahoma" ) )
		
		gbSizer30.Add( self.m_staticText54, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		gbSizer34.Add( gbSizer30, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		gbSizer31 = wx.GridBagSizer( 0, 0 )
		gbSizer31.SetFlexibleDirection( wx.BOTH )
		gbSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._btn_update_results = wx.Button( self._panel_query_results, wx.ID_ANY, _(u"Update Query"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer31.Add( self._btn_update_results, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_continue  = wx.Button( self._panel_query_results, wx.ID_ANY, _(u"Continue"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer31.Add( self._btn_continue , wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		gbSizer34.Add( gbSizer31, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		
		sbSizer11.Add( gbSizer34, 1, wx.EXPAND, 5 )
		
		
		self._panel_query_results.SetSizer( sbSizer11 )
		self._panel_query_results.Layout()
		sbSizer11.Fit( self._panel_query_results )
		self._notebook.AddPage( self._panel_query_results, _(u"Query Results"), False )
		self._panel_sample_conf = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self._panel_sample_conf.Hide()
		
		bSizer101 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self._panel_sample_conf, wx.ID_ANY, _(u"Sample Confidence") ), wx.VERTICAL )
		
		gbSizer13 = wx.GridBagSizer( 0, 0 )
		gbSizer13.SetFlexibleDirection( wx.BOTH )
		gbSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText19 = wx.StaticText( self._panel_sample_conf, wx.ID_ANY, _(u"Select Confidence Interval and Confidence Level to compute sample size. "), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		self.m_staticText19.SetFont( wx.Font( 8, 74, 93, 92, False, "Tahoma" ) )
		
		gbSizer13.Add( self.m_staticText19, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticline8 = wx.StaticLine( self._panel_sample_conf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer13.Add( self.m_staticline8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 7 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self._panel_sample_conf, wx.ID_ANY, _(u"Confidence Level(%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gbSizer13.Add( self.m_staticText20, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_confidence_levelsChoices = []
		self._cbx_confidence_levels = wx.ComboBox( self._panel_sample_conf, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_confidence_levelsChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self._cbx_confidence_levels.SetSelection( 0 )
		gbSizer13.Add( self._cbx_confidence_levels, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( self._panel_sample_conf, wx.ID_ANY, _(u"Confidence Interval(%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		gbSizer13.Add( self.m_staticText23, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_confidence_interval = wx.TextCtrl( self._panel_sample_conf, wx.ID_ANY, _(u"5"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer13.Add( self._tc_confidence_interval, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline10 = wx.StaticLine( self._panel_sample_conf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer13.Add( self.m_staticline10, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 4 ), wx.EXPAND |wx.ALL, 5 )
		
		self._st_num_samples_res = wx.StaticText( self._panel_sample_conf, wx.ID_ANY, _(u"Responsive: 0 of 0 documents"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_num_samples_res.Wrap( -1 )
		self._st_num_samples_res.SetFont( wx.Font( 8, 74, 93, 90, False, "Tahoma" ) )
		self._st_num_samples_res.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbSizer13.Add( self._st_num_samples_res, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_samples_unres = wx.StaticText( self._panel_sample_conf, wx.ID_ANY, _(u"Unresponsive: 0 of 0 documents"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_num_samples_unres.Wrap( -1 )
		self._st_num_samples_unres.SetFont( wx.Font( 8, 74, 93, 90, False, "Tahoma" ) )
		self._st_num_samples_unres.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbSizer13.Add( self._st_num_samples_unres, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._chk_toggle_cl_level = wx.CheckBox( self._panel_sample_conf, wx.ID_ANY, _(u"In addtion, apply to unresponsive documents"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer13.Add( self._chk_toggle_cl_level, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._panel_unres_cl = wx.Panel( self._panel_sample_conf, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer131 = wx.GridBagSizer( 0, 0 )
		gbSizer131.SetFlexibleDirection( wx.BOTH )
		gbSizer131.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText201 = wx.StaticText( self._panel_unres_cl, wx.ID_ANY, _(u"Confidence Level(%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText201.Wrap( -1 )
		gbSizer131.Add( self.m_staticText201, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cbx_confidence_levels_unresChoices = []
		self._cbx_confidence_levels_unres = wx.ComboBox( self._panel_unres_cl, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cbx_confidence_levels_unresChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self._cbx_confidence_levels_unres.SetSelection( 0 )
		gbSizer131.Add( self._cbx_confidence_levels_unres, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText231 = wx.StaticText( self._panel_unres_cl, wx.ID_ANY, _(u"Confidence Interval(%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText231.Wrap( -1 )
		gbSizer131.Add( self.m_staticText231, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_confidence_interval_unres = wx.TextCtrl( self._panel_unres_cl, wx.ID_ANY, _(u"5"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		gbSizer131.Add( self._tc_confidence_interval_unres, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._st_num_samples_ind_unres = wx.StaticText( self._panel_unres_cl, wx.ID_ANY, _(u"Unresponsive: 0 of 0 documents"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._st_num_samples_ind_unres.Wrap( -1 )
		self._st_num_samples_ind_unres.SetFont( wx.Font( 8, 74, 93, 90, False, "Tahoma" ) )
		self._st_num_samples_ind_unres.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbSizer131.Add( self._st_num_samples_ind_unres, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText53 = wx.StaticText( self._panel_unres_cl, wx.ID_ANY, _(u"For Unresponsive documents"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )
		self.m_staticText53.SetFont( wx.Font( 8, 74, 93, 92, False, "Tahoma" ) )
		
		gbSizer131.Add( self.m_staticText53, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		
		self._panel_unres_cl.SetSizer( gbSizer131 )
		self._panel_unres_cl.Layout()
		gbSizer131.Fit( self._panel_unres_cl )
		gbSizer13.Add( self._panel_unres_cl, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 7 ), wx.EXPAND |wx.ALL, 5 )
		
		
		sbSizer6.Add( gbSizer13, 1, wx.EXPAND, 5 )
		
		gbSizer21 = wx.GridBagSizer( 0, 0 )
		gbSizer21.SetFlexibleDirection( wx.BOTH )
		gbSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		sbSizer6.Add( gbSizer21, 1, wx.EXPAND, 5 )
		
		gbSizer14 = wx.GridBagSizer( 0, 0 )
		gbSizer14.SetFlexibleDirection( wx.BOTH )
		gbSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._btn_conf_back = wx.Button( self._panel_sample_conf, wx.ID_ANY, _(u"Back"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer14.Add( self._btn_conf_back, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_conf_next = wx.Button( self._panel_sample_conf, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer14.Add( self._btn_conf_next, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbSizer6.Add( gbSizer14, 1, wx.EXPAND, 5 )
		
		
		bSizer101.Add( sbSizer6, 1, wx.EXPAND, 5 )
		
		
		self._panel_sample_conf.SetSizer( bSizer101 )
		self._panel_sample_conf.Layout()
		bSizer101.Fit( self._panel_sample_conf )
		self._notebook.AddPage( self._panel_sample_conf, _(u"Sample Confidence"), False )
		self._panel_random_unresponsive = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		_gbsizer_review_unres = wx.GridBagSizer( 0, 0 )
		_gbsizer_review_unres.SetFlexibleDirection( wx.BOTH )
		_gbsizer_review_unres.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText131 = wx.StaticText( self._panel_random_unresponsive, wx.ID_ANY, _(u"Documents to be Reviewed\nDouble click on a file to open it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )
		self.m_staticText131.SetFont( wx.Font( 8, 74, 90, 92, False, "Tahoma" ) )
		
		_gbsizer_review_unres.Add( self.m_staticText131, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_clear_unres = wx.Button( self._panel_random_unresponsive, wx.ID_ANY, _(u"Clear Tags"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_review_unres.Add( self._btn_clear_unres, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._panel_review_unres = wx.Panel( self._panel_random_unresponsive, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,250 ), wx.TAB_TRAVERSAL )
		_gbsizer_review_unres.Add( self._panel_review_unres, wx.GBPosition( 1, 0 ), wx.GBSpan( 2, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self._tc_preview_tags_unres = wx.TextCtrl( self._panel_random_unresponsive, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,250 ), wx.TE_MULTILINE|wx.TE_WORDWRAP )
		_gbsizer_review_unres.Add( self._tc_preview_tags_unres, wx.GBPosition( 1, 3 ), wx.GBSpan( 2, 3 ), wx.ALL, 5 )
		
		self.m_staticText141 = wx.StaticText( self._panel_random_unresponsive, wx.ID_ANY, _(u"File Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText141.Wrap( -1 )
		_gbsizer_review_unres.Add( self.m_staticText141, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline61 = wx.StaticLine( self._panel_random_unresponsive, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		_gbsizer_review_unres.Add( self.m_staticline61, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 7 ), wx.EXPAND |wx.ALL, 5 )
		
		gbSizer111 = wx.GridBagSizer( 0, 0 )
		gbSizer111.SetFlexibleDirection( wx.BOTH )
		gbSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._btn_back_unres = wx.Button( self._panel_random_unresponsive, wx.ID_ANY, _(u"Back"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer111.Add( self._btn_back_unres, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_next_unres = wx.Button( self._panel_random_unresponsive, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer111.Add( self._btn_next_unres, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_review_unres.Add( gbSizer111, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		gbSizer121 = wx.GridBagSizer( 0, 0 )
		gbSizer121.SetFlexibleDirection( wx.BOTH )
		gbSizer121.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText151 = wx.StaticText( self._panel_random_unresponsive, wx.ID_ANY, _(u"Select a tag"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151.Wrap( -1 )
		self.m_staticText151.Hide()
		
		gbSizer121.Add( self.m_staticText151, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cmb_tags_unresChoices = [ _(u"Responsive"), _(u"Privileged"), _(u"All") ]
		self._cmb_tags_unres = wx.ComboBox( self._panel_random_unresponsive, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cmb_tags_unresChoices, wx.CB_READONLY )
		self._cmb_tags_unres.SetSelection( 2 )
		self._cmb_tags_unres.Hide()
		
		gbSizer121.Add( self._cmb_tags_unres, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_gen_report_unres = wx.Button( self._panel_random_unresponsive, wx.ID_ANY, _(u"Generate Report"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._btn_gen_report_unres.Hide()
		
		gbSizer121.Add( self._btn_gen_report_unres, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_review_unres.Add( gbSizer121, wx.GBPosition( 5, 5 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )
		
		self._panel_doc_tag_unres = wx.Panel( self._panel_random_unresponsive, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_response_unresChoices = [ _(u"Yes"), _(u"No"), _(u"Unknown") ]
		self._rbx_response_unres = wx.RadioBox( self._panel_doc_tag_unres, wx.ID_ANY, _(u"Responsive"), wx.DefaultPosition, wx.DefaultSize, _rbx_response_unresChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_response_unres.SetSelection( 2 )
		bSizer12.Add( self._rbx_response_unres, 0, wx.ALL, 5 )
		
		_rbx_privilage_unresChoices = [ _(u"Yes"), _(u"No"), _(u"Unknown") ]
		self._rbx_privilage_unres = wx.RadioBox( self._panel_doc_tag_unres, wx.ID_ANY, _(u"Privilage"), wx.DefaultPosition, wx.DefaultSize, _rbx_privilage_unresChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_privilage_unres.SetSelection( 0 )
		bSizer12.Add( self._rbx_privilage_unres, 0, wx.ALL, 5 )
		
		
		self._panel_doc_tag_unres.SetSizer( bSizer12 )
		self._panel_doc_tag_unres.Layout()
		bSizer12.Fit( self._panel_doc_tag_unres )
		_gbsizer_review_unres.Add( self._panel_doc_tag_unres, wx.GBPosition( 1, 6 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		
		self._panel_random_unresponsive.SetSizer( _gbsizer_review_unres )
		self._panel_random_unresponsive.Layout()
		_gbsizer_review_unres.Fit( self._panel_random_unresponsive )
		self._notebook.AddPage( self._panel_random_unresponsive, _(u"Sample Unresponsive"), False )
		self._panel_random_responsive = wx.Panel( self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		_gbsizer_review_res = wx.GridBagSizer( 0, 0 )
		_gbsizer_review_res.SetFlexibleDirection( wx.BOTH )
		_gbsizer_review_res.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText13 = wx.StaticText( self._panel_random_responsive, wx.ID_ANY, _(u"Documents to be Reviewed\nDouble click on a file to open it"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		self.m_staticText13.SetFont( wx.Font( 8, 74, 90, 92, False, "Tahoma" ) )
		
		_gbsizer_review_res.Add( self.m_staticText13, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_clear_res = wx.Button( self._panel_random_responsive, wx.ID_ANY, _(u"Clear Tags"), wx.DefaultPosition, wx.DefaultSize, 0 )
		_gbsizer_review_res.Add( self._btn_clear_res, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._panel_review_res = wx.Panel( self._panel_random_responsive, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,250 ), wx.TAB_TRAVERSAL )
		_gbsizer_review_res.Add( self._panel_review_res, wx.GBPosition( 1, 0 ), wx.GBSpan( 2, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self._tc_preview_tags = wx.TextCtrl( self._panel_random_responsive, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,250 ), wx.TE_MULTILINE|wx.TE_WORDWRAP )
		_gbsizer_review_res.Add( self._tc_preview_tags, wx.GBPosition( 1, 3 ), wx.GBSpan( 2, 3 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self._panel_random_responsive, wx.ID_ANY, _(u"File Preview"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		_gbsizer_review_res.Add( self.m_staticText14, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._panel_doc_tag_res = wx.Panel( self._panel_random_responsive, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		_rbx_response_resChoices = [ _(u"Yes"), _(u"No"), _(u"Unknown") ]
		self._rbx_response_res = wx.RadioBox( self._panel_doc_tag_res, wx.ID_ANY, _(u"Responsive"), wx.DefaultPosition, wx.DefaultSize, _rbx_response_resChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_response_res.SetSelection( 2 )
		bSizer11.Add( self._rbx_response_res, 0, wx.ALL, 5 )
		
		_rbx_privilage_resChoices = [ _(u"Yes"), _(u"No"), _(u"Unknown") ]
		self._rbx_privilage_res = wx.RadioBox( self._panel_doc_tag_res, wx.ID_ANY, _(u"Privilage"), wx.DefaultPosition, wx.DefaultSize, _rbx_privilage_resChoices, 1, wx.RA_SPECIFY_COLS )
		self._rbx_privilage_res.SetSelection( 2 )
		bSizer11.Add( self._rbx_privilage_res, 0, wx.ALL, 5 )
		
		
		self._panel_doc_tag_res.SetSizer( bSizer11 )
		self._panel_doc_tag_res.Layout()
		bSizer11.Fit( self._panel_doc_tag_res )
		_gbsizer_review_res.Add( self._panel_doc_tag_res, wx.GBPosition( 1, 7 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline6 = wx.StaticLine( self._panel_random_responsive, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		_gbsizer_review_res.Add( self.m_staticline6, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 7 ), wx.EXPAND |wx.ALL, 5 )
		
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._btn_back_res = wx.Button( self._panel_random_responsive, wx.ID_ANY, _(u"Back"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self._btn_back_res, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_next_res = wx.Button( self._panel_random_responsive, wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self._btn_next_res, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_review_res.Add( gbSizer11, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )
		
		gbSizer12 = wx.GridBagSizer( 0, 0 )
		gbSizer12.SetFlexibleDirection( wx.BOTH )
		gbSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText15 = wx.StaticText( self._panel_random_responsive, wx.ID_ANY, _(u"Select a tag"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		self.m_staticText15.Hide()
		
		gbSizer12.Add( self.m_staticText15, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		_cmb_tags_resChoices = [ _(u"Responsive"), _(u"Privileged"), _(u"All") ]
		self._cmb_tags_res = wx.ComboBox( self._panel_random_responsive, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, _cmb_tags_resChoices, wx.CB_READONLY )
		self._cmb_tags_res.SetSelection( 2 )
		self._cmb_tags_res.Hide()
		
		gbSizer12.Add( self._cmb_tags_res, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_gen_report_res = wx.Button( self._panel_random_responsive, wx.ID_ANY, _(u"Generate Report"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self._btn_gen_report_res.Hide()
		
		gbSizer12.Add( self._btn_gen_report_res, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		_gbsizer_review_res.Add( gbSizer12, wx.GBPosition( 5, 5 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )
		
		
		self._panel_random_responsive.SetSizer( _gbsizer_review_res )
		self._panel_random_responsive.Layout()
		_gbsizer_review_res.Fit( self._panel_random_responsive )
		self._notebook.AddPage( self._panel_random_responsive, _(u"Sample Responsive"), False )
		
		_bsizer_main.Add( self._notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( _bsizer_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self._on_menu_sel_preferences, id = self._mitem_preferences.GetId() )
		self.Bind( wx.EVT_MENU, self._on_menu_sel_about, id = self._mitem_about.GetId() )
		self.Bind( wx.EVT_MENU, self._on_menu_sel_help, id = self._mitem_help.GetId() )
		self._notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_notebook_page_changed )
		self._btn_clear_project_details.Bind( wx.EVT_BUTTON, self._on_click_clear_project_details )
		self._btn_index_data.Bind( wx.EVT_BUTTON, self._on_click_index_data )
		self._cbx_project_title.Bind( wx.EVT_COMBOBOX, self._on_set_existing_project )
		self._btn_new_project.Bind( wx.EVT_BUTTON, self._on_click_new_project )
		self._btn_add_to_query1.Bind( wx.EVT_BUTTON, self._on_click_add_to_query1 )
		self._btn_run_query1.Bind( wx.EVT_BUTTON, self._on_click_run_query )
		self._rbx_responsive.Bind( wx.EVT_RADIOBOX, self._on_rbx_responsive_updated )
		self._btn_recalculate_results.Bind( wx.EVT_BUTTON, self._on_click_recalculate )
		self._rbx_feedack_res.Bind( wx.EVT_RADIOBOX, self._on_rbx_result_responsive_update )
		self._btn_next_res_res.Bind( wx.EVT_BUTTON, self._on_click_next_res )
		self._btn_prev_res_res.Bind( wx.EVT_BUTTON, self._on_click_previous_res )
		self._rbx_feedack_unres.Bind( wx.EVT_RADIOBOX, self._on_rbx_result_unresponsive_update )
		self._btn_net_res_unres.Bind( wx.EVT_BUTTON, self._on_click_next_unres )
		self._btn_prev_res_unres.Bind( wx.EVT_BUTTON, self._on_click_previous_unres )
		self._btn_update_results.Bind( wx.EVT_BUTTON, self._on_click_update_results )
		self._btn_continue .Bind( wx.EVT_BUTTON, self._on_click_continue )
		self._cbx_confidence_levels.Bind( wx.EVT_COMBOBOX, self._on_confidence_changed )
		self._tc_confidence_interval.Bind( wx.EVT_KILL_FOCUS, self._on_precision_changed )
		self._chk_toggle_cl_level.Bind( wx.EVT_CHECKBOX, self._on_click_change_unres_focus )
		self._cbx_confidence_levels_unres.Bind( wx.EVT_COMBOBOX, self._on_confidence_changed_unres )
		self._tc_confidence_interval_unres.Bind( wx.EVT_KILL_FOCUS, self._on_precision_changed_unres )
		self._btn_conf_back.Bind( wx.EVT_BUTTON, self._on_click_cl_goback )
		self._btn_conf_next.Bind( wx.EVT_BUTTON, self._on_click_cl_next )
		self._btn_clear_unres.Bind( wx.EVT_BUTTON, self._on_click_clear_all_doc_tags_unres )
		self._btn_back_unres.Bind( wx.EVT_BUTTON, self._btn_sample_back_unres )
		self._btn_next_unres.Bind( wx.EVT_BUTTON, self._on_click_sample_next )
		self._rbx_response_unres.Bind( wx.EVT_RADIOBOX, self._on_rbx_responsive_updated_unres )
		self._rbx_privilage_unres.Bind( wx.EVT_RADIOBOX, self._on_rbx_privileged_updated_unres )
		self._btn_clear_res.Bind( wx.EVT_BUTTON, self._on_click_clear_all_doc_tags_res )
		self._rbx_response_res.Bind( wx.EVT_RADIOBOX, self._on_rbx_responsive_updated_res )
		self._rbx_privilage_res.Bind( wx.EVT_RADIOBOX, self._on_rbx_privileged_updated_res )
		self._btn_back_res.Bind( wx.EVT_BUTTON, self._btn_sample_back_unres )
		self._btn_gen_report_res.Bind( wx.EVT_BUTTON, self._on_click_review_gen_report )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_menu_sel_preferences( self, event ):
		event.Skip()
	
	def _on_menu_sel_about( self, event ):
		event.Skip()
	
	def _on_menu_sel_help( self, event ):
		event.Skip()
	
	def _on_notebook_page_changed( self, event ):
		event.Skip()
	
	def _on_click_clear_project_details( self, event ):
		event.Skip()
	
	def _on_click_index_data( self, event ):
		event.Skip()
	
	def _on_set_existing_project( self, event ):
		event.Skip()
	
	def _on_click_new_project( self, event ):
		event.Skip()
	
	def _on_click_add_to_query1( self, event ):
		event.Skip()
	
	def _on_click_run_query( self, event ):
		event.Skip()
	
	def _on_rbx_responsive_updated( self, event ):
		event.Skip()
	
	def _on_click_recalculate( self, event ):
		event.Skip()
	
	def _on_rbx_result_responsive_update( self, event ):
		event.Skip()
	
	def _on_click_next_res( self, event ):
		event.Skip()
	
	def _on_click_previous_res( self, event ):
		event.Skip()
	
	def _on_rbx_result_unresponsive_update( self, event ):
		event.Skip()
	
	def _on_click_next_unres( self, event ):
		event.Skip()
	
	def _on_click_previous_unres( self, event ):
		event.Skip()
	
	def _on_click_update_results( self, event ):
		event.Skip()
	
	def _on_click_continue( self, event ):
		event.Skip()
	
	def _on_confidence_changed( self, event ):
		event.Skip()
	
	def _on_precision_changed( self, event ):
		event.Skip()
	
	def _on_click_change_unres_focus( self, event ):
		event.Skip()
	
	def _on_confidence_changed_unres( self, event ):
		event.Skip()
	
	def _on_precision_changed_unres( self, event ):
		event.Skip()
	
	def _on_click_cl_goback( self, event ):
		event.Skip()
	
	def _on_click_cl_next( self, event ):
		event.Skip()
	
	def _on_click_clear_all_doc_tags_unres( self, event ):
		event.Skip()
	
	def _btn_sample_back_unres( self, event ):
		event.Skip()
	
	def _on_click_sample_next( self, event ):
		event.Skip()
	
	def _on_rbx_responsive_updated_unres( self, event ):
		event.Skip()
	
	def _on_rbx_privileged_updated_unres( self, event ):
		event.Skip()
	
	def _on_click_clear_all_doc_tags_res( self, event ):
		event.Skip()
	
	def _on_rbx_responsive_updated_res( self, event ):
		event.Skip()
	
	def _on_rbx_privileged_updated_res( self, event ):
		event.Skip()
	
	
	def _on_click_review_gen_report( self, event ):
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
	

###########################################################################
## Class PreferencesDialog
###########################################################################

class PreferencesDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Application Preferences"), pos = wx.DefaultPosition, size = wx.Size( 930,480 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_indexing = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Indexing Preferences") ), wx.VERTICAL )
		
		gbsizer_indexing = wx.GridBagSizer( 0, 0 )
		gbsizer_indexing.SetFlexibleDirection( wx.BOTH )
		gbsizer_indexing.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, _(u"Number of Topics"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_num_topics = wx.TextCtrl( self, wx.ID_ANY, _(u"50"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_num_topics.SetMaxLength( 3 ) 
		gbsizer_indexing.Add( self._tc_num_topics, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, _(u"Number of Passes"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText9, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_num_passes = wx.TextCtrl( self, wx.ID_ANY, _(u"1"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_num_passes.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_num_passes, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, _(u"Minimum Token Frequency"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_min_token_freq = wx.TextCtrl( self, wx.ID_ANY, _(u"1"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_min_token_freq.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_min_token_freq, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, _(u"Minimum Token Length"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gbsizer_indexing.Add( self.m_staticText11, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._tc_min_token_len = wx.TextCtrl( self, wx.ID_ANY, _(u"2"), wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
		self._tc_min_token_len.SetMaxLength( 2 ) 
		gbsizer_indexing.Add( self._tc_min_token_len, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, _(u"The below configurations are used for indexing and analysis of the documents given in the Data Folder (Index Data section). For indexing and analysis, we use Apache Lucene and the topic modeling methods such as TF-IDF, Latent Semantic Indexing, and Latent Dirichlet Allocation. Warning! Both of these methods are highly time consuming."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( 450 )
		self.m_staticText12.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		gbsizer_indexing.Add( self.m_staticText12, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, _(u"Tips"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		gbsizer_indexing.Add( self.m_staticText14, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _(u"Number of Topics: This is a predefined value used for the topic modeling based analysis. If the given documents are from very diverse backgrounds, use a higher value (> 50).\n\nNumber of Passes: It's a parameter used for the topic modeling algorithm. A higher value can increase the quality of the determined topics, but it can increase the execution time. \n\nMinimum Token Frequency: The topic modeling algorithm ignores the tokens (unique words in the corpus) with a token count (in the whole document collection) less than this value. \n\nMinimum Token Length: The topic modeling algorithm ignores the tokens with a token length less than this value.   \n\n"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.m_staticText13.Wrap( 400 )
		self.m_staticText13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.m_staticText13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_indexing.Add( self.m_staticText13, wx.GBPosition( 1, 3 ), wx.GBSpan( 6, 1 ), wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		self.m_staticline2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		gbsizer_indexing.Add( self.m_staticline2, wx.GBPosition( 0, 2 ), wx.GBSpan( 10, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.m_staticline1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.m_staticline1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		gbsizer_indexing.Add( self.m_staticline1, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )
		
		self._btn_reset_defaults = wx.Button( self, wx.ID_ANY, _(u"Reset Defaults"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_indexing.Add( self._btn_reset_defaults, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_save_indexing_preferences = wx.Button( self, wx.ID_ANY, _(u"Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_indexing.Add( self._btn_save_indexing_preferences, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_indexing.Add( gbsizer_indexing, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( sbsizer_indexing, 0, wx.ALL, 10 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self._btn_reset_defaults.Bind( wx.EVT_BUTTON, self._on_click_reset_defaults_indexing_preferences )
		self._btn_save_indexing_preferences.Bind( wx.EVT_BUTTON, self._on_click_save_indexing_preferences )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_click_reset_defaults_indexing_preferences( self, event ):
		event.Skip()
	
	def _on_click_save_indexing_preferences( self, event ):
		event.Skip()
	

###########################################################################
## Class NewProject
###########################################################################

class NewProject ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Create New Project"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		sbsizer_project = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Project Details") ), wx.VERTICAL )
		
		gbsizer_project = wx.GridBagSizer( 0, 0 )
		gbsizer_project.SetFlexibleDirection( wx.BOTH )
		gbsizer_project.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self._tc_project_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		self._tc_project_name.Enable( False )
		
		gbsizer_project.Add( self._tc_project_name, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Input Data Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText6, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._data_dir_picker = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE )
		gbsizer_project.Add( self._data_dir_picker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbsizer_project.Add( self.m_staticline3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )
		
		self._btn_clear_project_details = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_clear_project_details, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self._btn_index_data = wx.Button( self, wx.ID_ANY, _(u"Create Project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbsizer_project.Add( self._btn_index_data, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, _(u"Enter New Project Title"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		gbsizer_project.Add( self.m_staticText14, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		sbsizer_project.Add( gbsizer_project, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( sbsizer_project, 0, wx.ALL, 10 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		bSizer5.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self._tc_project_name.Bind( wx.EVT_KILL_FOCUS, self._on_focus_kill_chk_dup )
		self._btn_clear_project_details.Bind( wx.EVT_BUTTON, self._on_click_clear_project_details )
		self._btn_index_data.Bind( wx.EVT_BUTTON, self._on_click_index_data )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def _on_focus_kill_chk_dup( self, event ):
		event.Skip()
	
	def _on_click_clear_project_details( self, event ):
		event.Skip()
	
	def _on_click_index_data( self, event ):
		event.Skip()
	

