#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Thu Nov  8 18:29:42 2012

import wx
import os
from file import FileController
from file import merge3
from file import getLastCommit
import ConfigParser
from twisted.internet import reactor
# begin wxGlade: extracode
# end wxGlade


class DevilMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.directory = os.getcwd()
        fp = FileController(self.directory)
        try:
            y = open(fp.remotefile)
            remotecontent = y.read()
            y.close()
        except:
            remotecontent = ""
            print "No remote file"
        self.remote = {}
        # begin wxGlade: DevilMainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.text_ctrl_6 = wx.TextCtrl(self.notebook_1_pane_1, -1, "Username")
        self.text_ctrl_7 = wx.TextCtrl(self.notebook_1_pane_1, -1, "email")
        self.button_13 = wx.Button(self.notebook_1_pane_1, -1, "Initiate Repo")
        self.label_4 = wx.StaticText(self.notebook_1_pane_1, -1, "Add File or Directory")
        self.button_1 = wx.Button(self.notebook_1_pane_1, -1, "Add")
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_pane_1, -1, "Enter the commit to revert to. ", style=wx.TE_MULTILINE | wx.TE_LINEWRAP)
        self.button_6 = wx.Button(self.notebook_1_pane_1, -1, "Commit")
        self.combo_box_4 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_7 = wx.Button(self.notebook_1_pane_1, -1, "Revert")
        self.combo_box_5 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_8 = wx.Button(self.notebook_1_pane_1, -1, "Pull")
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_1_pane_1, -1, "localhost:7000")
        self.combo_box_6 = wx.ComboBox(self.notebook_1_pane_1, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.button_9 = wx.Button(self.notebook_1_pane_1, -1, "Push")
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.button_11 = wx.Button(self.notebook_1_pane_2, -1, "Status")
        self.button_12 = wx.Button(self.notebook_1_pane_2, -1, "Log")
        self.text_ctrl_5 = wx.TextCtrl(self.notebook_1_pane_2, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LINEWRAP)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.button_2 = wx.Button(self.notebook_1_pane_3, -1, "save")
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_pane_3, -1, remotecontent, style=wx.TE_MULTILINE | wx.TE_LINEWRAP)

        self.sb = self.CreateStatusBar()

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
        self.Bind(wx.EVT_BUTTON, self.OnSaveRemote, self.button_2)
        # end wxGlade
        self.UpdateRevertList()
        self.UpdateServerList()

    def __set_properties(self):
        # begin wxGlade: DevilMainFrame.__set_properties
        self.SetTitle("Devil")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("/home/satvik/acads/CS632/project/devil/devil.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((944, 783))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DevilMainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(1, 2, 1, 1)
        grid_sizer_1 = wx.FlexGridSizer(7, 2, 1, 1)
        grid_sizer_4 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_3 = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_3.Add(self.text_ctrl_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.text_ctrl_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_13, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.SHAPED, 0)
        grid_sizer_1.Add(self.button_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.combo_box_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.combo_box_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_4.Add(self.text_ctrl_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_4.Add(self.combo_box_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(grid_sizer_4, 1, wx.EXPAND, 0)
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
        sizer_2.Add(self.button_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(self.text_ctrl_1, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.notebook_1_pane_3.SetSizer(sizer_2)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Control")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Log")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Remotes")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnCommit(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        msg = self.text_ctrl_2.GetValue()
        """ Commit code here using commit message as msg"""
        obj=FileController(self.directory)
        obj.commit(msg)
        #print msg

        # Update commit list in dialog box 
        self.UpdateRevertList()
        self.sb.SetStatusText("Commited successfully ")
        

    def OnInit(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        """ Init the Repo on current directory """
        obj=FileController(self.directory)
        #print "Init called"
        username = self.text_ctrl_6.GetValue()
        email = self.text_ctrl_7.GetValue()
        obj.start2(username,email)
        self.sb.SetStatusText("Repo Initialized")


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
            obj=FileController(self.directory)
            obj.add(filename)
            #print filename
        dlg.Destroy()
        self.sb.SetStatusText("File added successfully")


    def OnRevert(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        commit = self.combo_box_4.GetValue()
        
        """ Revert to commit """
        obj=FileController(self.directory)
        obj.revert(commit)
        self.sb.SetStatusText("Reverted successfully")
        #print commit 

    def OnPull(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        server = self.combo_box_5.GetValue()
        loc=self.remote[server]
        """ Pull """
        obj=FileController(self.directory)
        obj.pull(loc)
        reactor.run()
        self.sb.SetStatusText("Pulled successfully")
        #print server 

    def OnPush(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        myloc = self.text_ctrl_3.GetValue()
        server = self.combo_box_6.GetValue()
        loc=self.remote[server]
        """ Push """
        print self.directory,"\n"
        obj=FileController(self.directory)
        print myloc+loc,"\n"
        obj.push(myloc+loc)
        reactor.run()
        self.sb.SetStatusText("Pushed successfully")
        #print server 

    def OnStatus(self, event):  # wxGlade: DevilMainFrame.<event_handler>

        """ Status code here """ 
        obj=FileController(self.directory)
        files=open(obj.trackingfile)
        lines=files.readlines();
        print lines
        #splitted = [(l[0],l[1],l[2]) for l in (y.split() for y in lines)]
        status=''
        for line in lines:
        #for (f,st,md) in splitted:
            sp = line.split()
            print sp
            f = sp[0]
            st = sp[1]
            md = sp[2]
            if st != 'commited':
                status=status+"added: " + f +"\n"
            elif not (md == str(os.path.getmtime(f))):
                status=status+"modified: " + f +"\n"
        #status = "get status from file"

        self.text_ctrl_5.SetValue(status)

    def OnLog(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        obj=FileController(self.directory)
        status = ''
        files=open(obj.statusfile)
        lines=files.readlines();
        for line in lines:
            line = line.split()
            status=status+"Commit: " + line[1] + "\n"  + "Author: " + line[2] + "\n" + "Email: " + line[3] + "\n" + "Date: " + line[4] + "\nMsg: "+ ' '.join(line[6:]) +"\n\n"

        self.text_ctrl_5.SetValue(status)

    def UpdateRevertList(self):
        """ Get all commits in the commit list """
        fp = FileController(self.directory)
        try:
            files=open(fp.statusfile)
            lines=files.readlines();
            commits = [l[1] for l in (m.split() for m in lines)]
            self.combo_box_4.Clear()
            self.combo_box_4.AppendItems(commits)
            wx.Yield()
        except:
            print "No status file"


    def UpdateServerList(self):  
        """ get list of servers """
        try:
            cp = ConfigParser.RawConfigParser()
            fp = FileController(self.directory)
            cp.read(fp.remotefile)
            nodes = cp.items("Remotes")
            servers = []
            for (n,l) in nodes:
                self.remote[n] = l 
                servers = servers + [n]
            self.combo_box_5.Clear()
            self.combo_box_5.AppendItems(servers)
            self.combo_box_6.Clear()
            self.combo_box_6.AppendItems(servers)
            wx.Yield()
        except:
            print "failed updating server list"



    def OnSaveRemote(self, event):  # wxGlade: DevilMainFrame.<event_handler>
        fp = FileController(self.directory)
        w = self.text_ctrl_1.GetValue()
        y = open(fp.remotefile,'w')
        y.write(w)
        y.close()
        self.UpdateServerList()
        self.sb.SetStatusText("Saved successfully")

# end of class DevilMainFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    Devil = DevilMainFrame(None, -1, "")
    app.SetTopWindow(Devil)
    Devil.Show()
    app.MainLoop()
