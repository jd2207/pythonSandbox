#Boa:Frame:UserGuide
import wx, os, sys, wx.html
import RistrettoCommon
import IceraToolbox

if IceraToolbox.IsWindows():
    import win32api

def create(parent):
    return UserGuide(parent)

[wxID_USERGUIDE, wxID_USERGUIDEHTMLWINDOW1, wxID_USERGUIDEHTMLWINDOW2,
 wxID_USERGUIDEHTMLWINDOW3, wxID_USERGUIDEHTMLWINDOW4,
 wxID_USERGUIDEHTMLWINDOW5, wxID_USERGUIDEHTMLWINDOW6,
 wxID_USERGUIDEHTMLWINDOW7, wxID_USERGUIDEHTMLWINDOW8, wxID_USERGUIDENOTEBOOKUSERGUIDE,
] = [wx.NewId() for _init_ctrls in range(10)]

GENERAL_PAGEID=0
FIRMWARE_PAGEID=1
CONFIGFILE_PAGEID=2
DEBUG_PAGEID=3
HIF_PAGEID=4
ADB_PAGEID=5
BOARDREPAIR_PAGEID=6
TOOLS_PAGEID=7

class UserGuide(wx.Frame):
    def _init_coll_boxSizerMain_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.notebookUserGuide, 1, border=0, flag=wx.EXPAND)

    def _init_coll_notebookUserGuide_Pages(self, parent):
        # generated method, don't edit

        # BOA method edited: removed imageId causing crash in Linux. Keep the pages ordered so
        # that the right page get hidden depending on options
        parent.AddPage(page=self.htmlWindow1, select=True,
              text='General')
        # imageId=FIRMWARE_PAGEID
        parent.AddPage(page=self.htmlWindow2, select=False, text='Firmware')
        # imageId=CONFIGFILE_PAGEID
        parent.AddPage(page=self.htmlWindow3, select=False, text='Configuration Files')
        # imageId=DEBUG_PAGEID
        parent.AddPage(page=self.htmlWindow4, select=False, text='Debug')
        # imageId=HIF_PAGEID
        parent.AddPage(page=self.htmlWindow5, select=False, text='Host Interface')
        # imageId=ADB_PAGEID
        parent.AddPage(page=self.htmlWindow8, select=False, text='ADB Interface')
        # imageId=BOARDREPAIR_PAGEID
        parent.AddPage(page=self.htmlWindow6, select=False, text='Board Repair')
        # imageId=TOOLS_PAGEID
        parent.AddPage(page=self.htmlWindow7, select=False, text='Tools')


    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizerMain = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizerMain_Items(self.boxSizerMain)

        self.SetSizer(self.boxSizerMain)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_USERGUIDE, name='UserGuide',
              parent=prnt, pos=wx.Point(509, 128), size=wx.Size(458, 587),
              style=wx.DEFAULT_FRAME_STYLE, title='User Guide')
        self.SetClientSize(wx.Size(450, 560))
        self.SetIcon(wx.Icon('icera.ico',wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.OnUserGuideClose)

        self.notebookUserGuide = wx.Notebook(id=wxID_USERGUIDENOTEBOOKUSERGUIDE,
              name='notebookUserGuide', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(450, 560), style=0)

        self.htmlWindow1 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW1,
              name='htmlWindow1', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow2 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW2,
              name='htmlWindow2', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow3 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW3,
              name='htmlWindow3', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow4 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW4,
              name='htmlWindow4', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow5 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW5,
              name='htmlWindow5', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow6 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW6,
              name='htmlWindow6', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow7 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW7,
              name='htmlWindow7', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self.htmlWindow8 = wx.html.HtmlWindow(id=wxID_USERGUIDEHTMLWINDOW8,
              name='htmlWindow8', parent=self.notebookUserGuide, pos=wx.Point(0,
              0), size=wx.Size(442, 534), style=wx.html.HW_SCROLLBAR_AUTO)

        self._init_coll_notebookUserGuide_Pages(self.notebookUserGuide)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(None)
        self.frame = parent

        general_guide = os.path.join(self.module_path(), 'user_guide', 'General.html')
        self.htmlWindow1.LoadFile(general_guide)

        firmware_guide = os.path.join(self.module_path(), 'user_guide', 'Firmware.html')
        self.htmlWindow2.LoadFile(firmware_guide)

        config_files_guide = os.path.join(self.module_path(), 'user_guide', 'ConfigFiles.html')
        self.htmlWindow3.LoadFile(config_files_guide)

        if parent.platform.conn.mode==RistrettoCommon.RISTRETTO_ADB:
            debug_guide = os.path.join(self.module_path(), 'user_guide', 'DebugAdb.html')
        else:
            debug_guide = os.path.join(self.module_path(), 'user_guide', 'Debug.html')
        self.htmlWindow4.LoadFile(debug_guide)

        hif_guide = os.path.join(self.module_path(), 'user_guide', 'HostInterface.html')
        self.htmlWindow5.LoadFile(hif_guide)

        board_repair_guide = os.path.join(self.module_path(), 'user_guide', 'BoardRepair.html')
        self.htmlWindow6.LoadFile(board_repair_guide)

        tools_guide = os.path.join(self.module_path(), 'user_guide', 'Tools.html')
        self.htmlWindow7.LoadFile(tools_guide)

        adb_guide = os.path.join(self.module_path(), 'user_guide', 'AdbInterface.html')
        self.htmlWindow8.LoadFile(adb_guide)

        # Update some pages: adapt regarding some settings get in MainFrame, mainly due to config.txt content
        self.updateGeneralPage()
        self.updateFirmwarePage(parent.platform.conn.mode)
        self.updateConfigFilesPage()
        self.updateBoardRepairPage()
        if IceraToolbox.IsWindows():
            if parent.platform.conn.mode!=RistrettoCommon.RISTRETTO_HIF:
                self.notebookUserGuide.RemovePage(HIF_PAGEID)
            if parent.platform.conn.mode!=RistrettoCommon.RISTRETTO_ADB:
                self.notebookUserGuide.RemovePage(ADB_PAGEID)

    def updateGeneralPage(self):
        try:
            self.extract_folder = os.environ['TEMP']
            if IceraToolbox.IsWindows():
                self.extract_folder = win32api.GetLongPathName(os.environ['TEMP'])
            self.htmlWindow1.AppendToPage('<br>')
            self.htmlWindow1.AppendToPage('When used with packaged version, tool must be extracted here <b>%s</b> in a RISTRETTO_GUI folder' % self.extract_folder)
        except:
            pass

    def updateFirmwarePage(self, mode):
        str=''
        if mode==RistrettoCommon.RISTRETTO_ADB:
            str+='<h2><b>Options:</b></h2>'
            str+='On a single flash platform, Cross Boot Check (CBC) is done by the tool and can be disabled through checkbox.<br>'
            str+='Key Revocation Mechanism (KRM) is also done by the tool and can be disabled through checkbox.<br>'
            str+='By default, FILD is re-started after any file update and this can be disabled through checkbox.<br>'
            self.htmlWindow2.AppendToPage(str)

    def updateConfigFilesPage(self):
        str = "<b><u>Configuration files settings:</u><b>"
        str += "<ul>"
        str += "<li> DEVICECFG: signed with OEM_FACT keys and embedding PCID.</li>"
        str += "<li> PRODUCTCFG: signed with OEM_FIELD keys.</li>"
        str += "<li> IMEI: signed with OEM_FACT and embedding PCID.</li>"
        str += " <li> CALIB: signed with OEM_FACT.</li>"
        str += "<li> AUDIOCFG: unsigned.</li>"
        str += "</ul>"
        str += "<br><br>"
        self.htmlWindow3.AppendToPage(str)

        str = "<b><u>NOTES:</u><b>"
        str += "<ul>"
        str += "<li>Update of all files can be performed even when multi platform detected except for:"
        str += "<ul>"
        str += "<li>IMEI</li>"
        str += "<li>Calibration</li>"
        str += "</ul></li>"
        str += "</ul>"
        str += "<br><br>"
        self.htmlWindow3.AppendToPage(str)


    def updateBoardRepairPage(self):
        str = "<h2> Boot Agent </h2>"
        str += "This utility to be used for a boot from UART sequence.<br>"
        str += "User to select:"
        str += "<ul>"
        str += "<li> Specific BT2 able to load any appli through UART.</li>"
        str += "<li> Application to be loaded by BT2 and started.</li>"
        str += "</ul>"
        str += "Additional settings:<br>"
        str+= "User can manually and separately select baudrate to use to communicate with BROM or BT2."
        str += "<br>"
        str += "<br><u>NOTES:</u><br>"
        str += "<ul>"
        str += "<li>\"Firmware\" & \"Configuration Files\" tabs can then be used in order to perform 1st platform programming.</li>"
        str += "</ul>"
        self.htmlWindow6.AppendToPage(str)

        str = " <h2> Repair Agent </h2>"
        str += "This utility to be used for automatic board repair:"
        str += "<ul>"
        str += "<li>Load and start specific BT2 and LDR responsibile for 1st platform boot and formatting.</li>"
        str += "<li>1st release programming via USB.</li>"
        str += "<li>Possibility of calibration programming.</li>"
        str += "</ul>"
        str += "<br>"
        str += "<br><u>NOTES:</u>"
        str += "<ul>"
        str += "<li>"
        str += "Repair package must contain all files selected thanks to check boxes."
        str += "All files checked and disabled by default are mandatory in order to successfully run repair agent."
        str += "</li>"
        str += "<li>Platform config and custom config must be .xml files.</li>"
        str += "</ul>"
        str += "<br>"
        self.htmlWindow6.AppendToPage(str)

    def module_path(self):
        if hasattr(sys,"frozen"):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(__file__)

    def OnUserGuideClose(self, event):
        self.frame.UserGuideDlg = None
        self.Destroy()
