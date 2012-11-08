#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Thu Nov  8 18:29:42 2012

import wx
import os
import ConfigParser
from file import FileController

# begin wxGlade: extracode
# end wxGlade


class DevilMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.directory = os.getcwd()
        self.remote = {}
        # begin wxGlade: DevilMainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.label_1 = wx.StaticText(self.notebook_1_pane_1, -1, "Init the version control")
        self.button_13 = wx.Button(self.notebook_1_pane_1, -1, "Initiate Repo")
        self.label_4 = wx.StaticText(self.notebook_1_pane_1, -1, "Add File or Directory")
        self.button_1 = wx.Button(self.notebook_1_pane_1, -1, "Add")
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_pane_1, -1, "Enter the commit to revert to. ", style=wx.TE_MULTILINE | wx.TE_LINEWRAP)
        self.button_6 = wx.Button(self.notebook_1_pane_1, -1, "Commit")
        self.combo_box_4 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_7 = wx.Button(self.notebook_1_pane_1, -1, "Revert")
        self.combo_box_5 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_8 = wx.Button(self.notebook_1_pane_1, -1, "Pull")
        self.combo_box_6 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_9 = wx.Button(self.notebook_1_pane_1, -1, "Push")
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.button_11 = wx.Button(self.notebook_1_pane_2, -1, "Status")
        self.button_12 = wx.Button(self.notebook_1_pane_2, -1, "Log")
        self.text_ctrl_5 = wx.TextCtrl(self.notebook_1_pane_2, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LINEWRAP)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnInit, self.button_13)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnCommit, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.OnRevert, self.button_7)
        self.Bind(wx.EVT_BUTTON, self.OnPull, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.OnPush, self.button_9)
        self.Bind(wx.EVT_BUTTON, self.OnStatus, self.button_11)
        self.Bind(wx.EVT_BUTTON, self.OnLog, self.button_12)
        self.UpdateServerList()
        self.UpdateRevertList()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DevilMainFrame.__set_properties
        self.SetTitle("Devil")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("/home/satvik/acads/CS632/project/devil/devil.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((883, 983))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DevilMainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(1, 2, 1, 1)
        grid_sizer_1 = wx.FlexGridSizer(7, 2, 1, 1)
        grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_13, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        grid_sizer_1.Add(self.button_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.combo_box_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.combo_box_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.combo_box_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.notebook_1_pane_1.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableRow(2)
        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableRow(4)
        grid_sizer_1.AddGrowableRow(5)
        grid_sizer_1.AddGrowableRow(6)
        grid_sizer_1.AddGrowableRow(7)
        grid_sizer_1.AddGrowableRow(8)
        grid_sizer_1.AddGrowableRow(9)
        grid_sizer_1.AddGrowableCol(0)
        grid_sizer_1.AddGrowableCol(1)
        grid_sizer_2.Add(self.button_11, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.button_12, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.AddGrowableRow(0)
        grid_sizer_2.AddGrowableCol(0)
        grid_sizer_2.AddGrowableCol(1)
        sizer_3.Add(grid_sizer_2, 0, wx.EXPAND, 0)
        sizer_3.Add(self.text_ctrl_5, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.notebook_1_pane_2.SetSizer(sizer_3)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Control")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Log")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnCommit(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        msg = self.text_ctrl_2.GetValue()
        """ Commit code here using commit message as msg"""
        print msg

        # Update commit list in dialog box 
        self.UpdateRevertList()
        

    def OnInit(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        """ Init the Repo on current directory """
        print "Init called"
        pass 

    def OnAdd(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", '.', "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            fn = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            filename = os.path.join(dirname, fn)
            self.label_4.SetLabel(filename)
            wx.Yield()
            """ Add Code Here using """
            print filename
        dlg.Destroy()

    def OnRevert(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        commit = self.combo_box_4.GetValue()
        
        """ Revert to commit """
        print commit 

    def OnPull(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        server = self.combo_box_5.GetValue()
        
        """ Pull """

        print server 

    def OnPush(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        server = self.combo_box_6.GetValue()

        """ Push """
        print server 

    def OnStatus(self, event):  # wxGlade: DevilMainFrame.<event_handler>

        """ Status code here """ 
        status = "get status from file"

        self.text_ctrl_5.SetValue(status)

    def OnLog(self, event):  # wxGlade: DevilMainFrame.<event_handler>

        status = "get log  from file"

        self.text_ctrl_5.SetValue(status)

    def UpdateRevertList(self):
        """ Get all commits in the commit list """
        commits = ['1','2','3']
        self.combo_box_4.Clear()
        self.combo_box_4.AppendItems(commits)
        wx.Yield()

    def UpdateServerList(self):  
        """ get list of servers """
        cp = ConfigParser.RawConfigParser()
        fp = FileController(self.directory)
        cp.read(self.remotefile)
        #cp.read('remotes.txt')
        nodes = cp.items("Remotes")
        servers = []
        for (n,l) in nodes:
            self.remote[n] = l 
            servers = servers + [n]
        print nodes
        self.combo_box_5.Clear()
        self.combo_box_5.AppendItems(servers)
        self.combo_box_6.Clear()
        self.combo_box_6.AppendItems(servers)
        wx.Yield()


# end of class DevilMainFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    Devil = DevilMainFrame(None, -1, "")
    app.SetTopWindow(Devil)
    Devil.Show()
    app.MainLoop()