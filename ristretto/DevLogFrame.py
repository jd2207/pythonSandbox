#Boa:Frame:DevLogFrame

import wx
import IceraAdb, IceraToolbox
import time, re

def create(parent):
    return DevLogFrame(parent)

[wxID_DEVLOGFRAME, wxID_DEVLOGFRAMECLOSEBTN, wxID_DEVLOGFRAMEDEVLOGCONSOLE, 
 wxID_DEVLOGFRAMEFILTERLABEL, wxID_DEVLOGFRAMEFILTERTXT, 
 wxID_DEVLOGFRAMEMAINCB, wxID_DEVLOGFRAMERADIOCB, wxID_DEVLOGFRAMECLEANBTN, 
 wxID_DEVLOGFRAMESTATICLINE1, wxID_DEVLOGFRAMESTOPBTN, 
 wxID_DEVLOGFRAMESYSTEMCB, wxID_DEVLOGFRAMETIMECB, 
] = [wx.NewId() for _init_ctrls in range(12)]

CLOSE_EVT_ID_VALUE = wx.NewId()

################################
# Boa constructor generated frame for
#   logcat message viewing
################################

#class RedirectText(object):
#    '''
#    Class used to redirect messages to wx.TextCtrl text terminal
#    '''

#    def __init__(self,aWxTextCtrl):
#            self.out=aWxTextCtrl

#    def write(self,string):
#            self.out.WriteText(string)

class DevLogFrame(wx.Frame):

    def _init_coll_filteringUpperSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.timeCB, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.mainCB, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.radioCB, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.systemCB, 0, border=5, flag=wx.ALL)

    def _init_coll_filteringSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.filterLabel, 0, border=5,
              flag=wx.ALIGN_CENTER | wx.ALL)
        parent.AddWindow(self.filterTxt, 2, border=5, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.cleanBtn, 0, border=5, flag=wx.ALL)

    def _init_coll_btnSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.closeBtn, 0, border=5, flag=wx.ALL)
        parent.AddWindow(self.stopBtn, 0, border=5, flag=wx.ALL)

    def _init_coll_topSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.filteringUpperSizer, 0, border=0, flag=0)
        parent.AddSizer(self.filteringSizer, 0, border=0, flag=0)
        parent.AddWindow(self.devlogConsole, 1, border=0,
              flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.staticLine1, 0, border=5,
              flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
        parent.AddSizer(self.btnSizer, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.topSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.filteringSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.filteringUpperSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.btnSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_topSizer_Items(self.topSizer)
        self._init_coll_filteringSizer_Items(self.filteringSizer)
        self._init_coll_filteringUpperSizer_Items(self.filteringUpperSizer)
        self._init_coll_btnSizer_Items(self.btnSizer)

        self.SetSizer(self.topSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_DEVLOGFRAME, name=u'DevLogFrame',
              parent=prnt, pos=wx.Point(232, 232), size=wx.Size(630, 685),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Android Log Monitor')
        self.SetClientSize(wx.Size(612, 640))
        self.SetIcon(wx.Icon(u'icera.ico',wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))

        self.timeCB = wx.CheckBox(id=wxID_DEVLOGFRAMETIMECB, label=u'time',
              name=u'timeCB', parent=self, pos=wx.Point(5, 5), size=wx.Size(82,
              16), style=0)
        self.timeCB.SetValue(True)
        self.timeCB.SetToolTipString(u'-v time')
        self.timeCB.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        self.mainCB = wx.CheckBox(id=wxID_DEVLOGFRAMEMAINCB, label=u'main',
              name=u'mainCB', parent=self, pos=wx.Point(97, 5), size=wx.Size(82,
              16), style=0)
        self.mainCB.SetToolTipString(u'-b main')
        self.mainCB.SetValue(True)
        self.mainCB.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        self.radioCB = wx.CheckBox(id=wxID_DEVLOGFRAMERADIOCB, label=u'radio',
              name=u'radioCB', parent=self, pos=wx.Point(189, 5),
              size=wx.Size(82, 16), style=0)
        self.radioCB.SetToolTipString(u'-b radio')
        self.radioCB.SetValue(True)
        self.radioCB.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        self.systemCB = wx.CheckBox(id=wxID_DEVLOGFRAMESYSTEMCB,
              label=u'system', name=u'systemCB', parent=self, pos=wx.Point(281,
              5), size=wx.Size(82, 16), style=0)
        self.systemCB.SetToolTipString(u'-b system')
        self.systemCB.SetValue(True)
        self.systemCB.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)

        self.filterLabel = wx.StaticText(id=wxID_DEVLOGFRAMEFILTERLABEL,
              label=u'Additional Filter:', name=u'filterLabel', parent=self,
              pos=wx.Point(5, 37), size=wx.Size(94, 16), style=0)

        self.filterTxt = wx.TextCtrl(id=wxID_DEVLOGFRAMEFILTERTXT,
              name=u'filterTxt', parent=self, pos=wx.Point(109, 31),
              size=wx.Size(219, 28), style=0, value=u'')
        self.filterTxt.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.filterTxt.SetAutoLayout(False)
        self.filterTxt.SetToolTipString(u'Additional logcat filter')

        self.cleanBtn = wx.Button(id=wxID_DEVLOGFRAMECLEANBTN,
              label=u'Clean Logcat', name=u'cleanBtn', parent=self,
              pos=wx.Point(338, 31), size=wx.Size(87, 28), style=0)
        self.cleanBtn.SetToolTipString(u'Clean Logcat \n \'adb logcat -c ...\'')
        self.cleanBtn.Show(True)
        self.cleanBtn.Bind(wx.EVT_BUTTON, self.OnCleanBtnButton,
              id=wxID_DEVLOGFRAMECLEANBTN)

        self.devlogConsole = wx.TextCtrl(id=wxID_DEVLOGFRAMEDEVLOGCONSOLE,
              name=u'devlogConsole', parent=self,
              style=wx.TE_READONLY | wx.TE_MULTILINE, value='')
        self.devlogConsole.SetBackgroundColour(wx.Colour(64, 0, 64))
        self.devlogConsole.SetForegroundColour(wx.Colour(192, 192, 192))

        self.staticLine1 = wx.StaticLine(id=wxID_DEVLOGFRAMESTATICLINE1,
              name='staticLine1', parent=self, pos=wx.Point(5, 595),
              size=wx.Size(602, 2), style=0)

        self.closeBtn = wx.Button(id=wxID_DEVLOGFRAMECLOSEBTN, label=u'Close',
              name=u'closeBtn', parent=self, pos=wx.Point(5, 607),
              size=wx.Size(87, 28), style=0)
        self.closeBtn.Bind(wx.EVT_BUTTON, self.OnCloseBtnButton,
              id=wxID_DEVLOGFRAMECLOSEBTN)

        self.stopBtn = wx.Button(id=wxID_DEVLOGFRAMESTOPBTN, label=u'Stop',
              name=u'stopBtn', parent=self, pos=wx.Point(102, 607),
              size=wx.Size(87, 28), style=0)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopStartButton,
              id=wxID_DEVLOGFRAMESTOPBTN)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.device = ""
        self.adb = IceraAdb.AdbTool(None)
        self._SetupLogcatArgs()
        self.socket=None
        self.parent = parent
        self.monitoringFlashing = False
        self.Closed=False
        self.verbosity=IceraToolbox.VERB_NONE

        try:
            self.adb.Connect()
        except:
            pass
        
    def OnCheckBox(self, event):
        if not self.systemCB.GetValue() and not self.radioCB.GetValue():
            if not self.mainCB.GetValue():
                print "Default logcat is \'logcat -b main\'"
            self.mainCB.SetValue(True)
            self.mainCB.Disable()
        elif not self.mainCB.IsEnabled():
            self.mainCB.Enable()
            
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self._StopLogging()    
        self._SetupLogcatArgs()
        self._Refresh()

    def OnCleanBtnButton(self, event):
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self._StopLogging()
        self._SetupLogcatArgs()
        self.adb.Cmd("logcat", "{0} -c".format(self.logcatArgs), device=self.device)
        self._Refresh()
        

    def OnStopStartButton(self, event):
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self._StopLogging()            
        else:
            self._Refresh() 
    
    def OnCloseBtnButton(self, event):
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self._StopLogging()
        self.Close()

    def _SetupLogcatArgs(self):
        '''
        Build logcat args string from GUI elements
        '''

        self.logcatArgs = ""

        if self.timeCB.GetValue():
            self.logcatArgs = self.logcatArgs + "-v time"
        if self.mainCB.GetValue():
            self.logcatArgs = self.logcatArgs + " -b main"
        if self.radioCB.GetValue():
            self.logcatArgs = self.logcatArgs + " -b radio"
        if self.systemCB.GetValue():
            self.logcatArgs = self.logcatArgs + " -b system"

        self.logcatArgs = self.logcatArgs + " " + self.filterTxt.GetValue()

    def _StopLogging(self):
        '''
        Stop logcat message reading from device
        '''
        self.Closed=False
        if self.adb.State == IceraAdb.ConnectionState.IDLE:
            return

        self.adb.StopBlockingCmd(self.socket)
        self.stopBtn.SetLabel(u'Start')

    def _Refresh(self):
        '''
        Reload messages from devices using current logcat device and logcat args
        '''
        self.devlogConsole.Clear()

        if self.device == "":
            # if we haven't yet set the device - can't call for the transport
            self.devlogConsole.AppendText("Error: device serial number not set")
            return

        self.socket=self.adb.StartBlockingCmd(self, "logcat", self.logcatArgs, self.device)
        #self.adb.StartBlockingCmd(self.redOut, "logcat", self.logcatArgs, self.device)
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self.stopBtn.SetLabel(u'Stop')
            
    def disconnect(self,device):
        '''
        Stop logcat message reading from device
        '''
        self.Closed=False
        if self.adb.State == IceraAdb.ConnectionState.DISCONNECTED:
            return

        self.adb.StopBlockingCmd(self.socket)
        self.stopBtn.SetLabel(u'Start')

        self.adb.State = IceraAdb.ConnectionState.DISCONNECTED

    def ShowLog(self, device):
        '''
        Show logcat messages
        Will interrupt current reading process if one is running
        '''

        self.device = device
        self._Refresh()
        self.Show()

    def write(self,String):
        if self.adb.State == IceraAdb.ConnectionState.IDLE:
            self.Closed=True
        if IceraToolbox.IsWindows():
            String = String.decode('utf-8','ignore').encode('utf-8')
        self.devlogConsole.WriteText(String)
        
        if String == "\n\nConnection lost.\n\n":
            if self.adb.State == IceraAdb.ConnectionState.DISCONNECTED:
                return

            self.adb.StopBlockingCmd(self.socket)
            self.stopBtn.SetLabel(u'Start')
    
            self.adb.State = IceraAdb.ConnectionState.DISCONNECTED
            return

        if self.monitoringFlashing:
            # search for identifiers in the string
            search=re.search(r'use-Rlog/RLOG-RIL AT{.*}(.*): AT(.*)< Modem mode',String)
            if search:
                print "Flashing SUCCESS"
                self.monitoringFlashing = False
                self._StopLogging()
                return
            res = String.find("/vendor/bin/icera-loader: SUCCESS")
            if res != -1:
                print String
                # we finished - flashing successful
                self.monitoringFlashing = False
                # stop reading the logs
                self._StopLogging()
            else:
                # try to look for failure identifier
                res = String.find("/vendor/bin/icera-loader: downloader ERROR")
                if res != -1:
                    print String
                    # we finished - flashing failed
                    self.monitoringFlashing = False
                    # stop reading the logs
                    self._StopLogging()
                    self.Show()
                else:
                     # check time spent monitoring - time limit 10 seconds
                    if (time.time()-self.monitoringStartTime) > 30.0:
                        # show logcat if verbosity >= Debug
                        if self.adb.verbosity >= IceraToolbox.VERB_DEBUG:
                            self.Show()
                    if (time.time()-self.monitoringStartTime) > 60.0:
                        self.monitoringFlashing = False
                        if self.adb.verbosity >= IceraToolbox.VERB_ERROR:
                            self.Show()
                        print "ERROR: Fail to restart the modem, please try to reboot your device"

    def MonitorFlashing(self, device):
        # Restore args to have full logs
        self.timeCB.SetValue(True)
        self.mainCB.SetValue(True)
        self.systemCB.SetValue(True)
        self.radioCB.SetValue(True)

        # need to clean the ADB history
        if self.adb.State == IceraAdb.ConnectionState.Executing:
            self._StopLogging()
        self.adb.Cmd("logcat"," -b radio -b system -b main -c", device=device)
        self.device = device
        self.monitoringFlashing = True
        self.monitoringStartTime = time.time()
        self._SetupLogcatArgs()
        self._Refresh()

class DevLogWrapper(wx.Frame):
    '''
    Class used as an abstraction to keep track of the DevLogFrame window state,
    buffers generated log when closing window
    '''

    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        self.parent = parent
        self._devLog = None
        self.log = ""

    def ShowLog(self, device):
        if self._devLog == None:
            self._devLog = DevLogFrame(self)
            self._devLog.Bind(wx.EVT_CLOSE, self._onWinClose)

        self._devLog.ShowLog(device)

    def _onWinClose(self, event):
        '''
        Close window event handler
        When closing window, cache generated log and destroy the window
        '''
        if not self._devLog.monitoringFlashing:
            self._devLog._StopLogging()
            # cache log on window closing
            self.log = self._devLog.devlogConsole.GetValue()
            self._devLog.Destroy()        
            self._devLog = None
        else:
            self._devLog.Hide()
        
    def Close(self):
        if self._devLog != None:
            self._devLog._StopLogging()
            # cache log on window closing
            self.log = self._devLog.devlogConsole.GetValue()
            self._devLog.Destroy()        
            self._devLog = None
            super(DevLogWrapper,self).Close()
            
    def Hide(self):
        if self._devLog != None:
            self._onWinClose(wx.EVT_CLOSE)
            super(DevLogWrapper,self).Hide()

    def GetLog(self):
        if self._devLog == None:
            return self.log
        else:
            return self._devLog.devlogConsole.GetValue()

    def MonitorFlashing(self, device):
        if self._devLog == None:
            self._devLog = DevLogFrame(self)
            self._devLog.Bind(wx.EVT_CLOSE, self._onWinClose)

        self._devLog.MonitorFlashing(device)
