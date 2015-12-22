#Boa:Frame:MainFrame
# -*- coding: utf-8 -*-

#########################################
# Ristretto ignores deprecating warnings
#########################################
import warnings
import time
import ctypes
warnings.filterwarnings('ignore', category=DeprecationWarning)

import wx
import wx.lib.delayedresult as delayedresult

########################
# Icera added: imports
########################
import UserGuideFrame, ArchInfoDialog, BuildDataFileFrame

import sys, os, re, shutil
import RistrettoCommon, RistrettoThreads, RistrettoFrameShare

from RistrettoCommon import PrintException, TMP_EXTRACT_FOLDER
from RistrettoFrameShare import FrameLog, FrameFileDragDrop, TextCtrlValidator, PopUpError, PopUpInfo, CloseConfirmation

sys.path.append(os.path.join(os.path.realpath(os.curdir),'..','modem-utils'))
import IceraToolbox
import icera_const as const

import DevLogFrame, IceraAdb

################################
# Icera added: global functions
################################
def create(parent):
    return MainFrame(parent)

[wxID_MAINFRAME, wxID_MAINFRAMEBUTTONADBAPIFACTIONSSTART, 
 wxID_MAINFRAMEBUTTONADBAPIFFORWARD, wxID_MAINFRAMEBUTTONADBAPIFSCAN, 
 wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESGET, 
 wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESSET, 
 wxID_MAINFRAMEBUTTONAPPLYHIFSWITCH, wxID_MAINFRAMEBUTTONBROWSEAPPLI, 
 wxID_MAINFRAMEBUTTONBROWSEBT2, wxID_MAINFRAMEBUTTONBROWSECALIBRATIONFILES, 
 wxID_MAINFRAMEBUTTONBROWSEDIRFIRMWAREINFO, 
 wxID_MAINFRAMEBUTTONBROWSEFIRMWAREINFO, wxID_MAINFRAMEBUTTONBROWSELOGFOLDER, 
 wxID_MAINFRAMEBUTTONBROWSERELEASEARCHIVE, 
 wxID_MAINFRAMEBUTTONBROWSEXMLSOURCE, wxID_MAINFRAMEBUTTONCRASHINFO, 
 wxID_MAINFRAMEBUTTONCRASHINFOBROWSE, wxID_MAINFRAMEBUTTONFACTBROWSEARCHIVE, 
 wxID_MAINFRAMEBUTTONFACTRELEASEUPDATE, 
 wxID_MAINFRAMEBUTTONFLASHCALIBRATIONFILES, wxID_MAINFRAMEBUTTONFLASHIMEI, 
 wxID_MAINFRAMEBUTTONFLASHRELEASE, wxID_MAINFRAMEBUTTONFLASHSINGLE, 
 wxID_MAINFRAMEBUTTONGETFIRMWAREINFO, wxID_MAINFRAMEBUTTONPATHBROWSE, 
 wxID_MAINFRAMEBUTTONPROGRAMXMLSOURCE, wxID_MAINFRAMEBUTTONSINGLE, 
 wxID_MAINFRAMEBUTTONSTARTBOARDREPAIR, wxID_MAINFRAMEBUTTONSTARTPLATINFO, 
 wxID_MAINFRAMEBUTTONSTOPBOARDREPAIR, 
 wxID_MAINFRAMEBUTTONUARTDISCOVERYSTARTSERVER, 
 wxID_MAINFRAMEBUTTONUARTDISCOVERYSTOPSERVER, wxID_MAINFRAMEBUTTONUNLOCK, 
 wxID_MAINFRAMECHECKBOXADBAPIFCONNECTION, wxID_MAINFRAMECHECKBOXALL, 
 wxID_MAINFRAMECHECKBOXAUDIOCFG, wxID_MAINFRAMECHECKBOXAUTODETECT, 
 wxID_MAINFRAMECHECKBOXBT2, wxID_MAINFRAMECHECKBOXBT3, 
 wxID_MAINFRAMECHECKBOXCRASHINFO, wxID_MAINFRAMECHECKBOXDEVICECFG, 
 wxID_MAINFRAMECHECKBOXFACTRELEASELISTALL, 
 wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTBT2, 
 wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTDEVICECFG, 
 wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTMDM, 
 wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTPRODUCTCFG, 
 wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTCALIB, 
 wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTLDR, 
 wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTPLATCG, 
 wxID_MAINFRAMECHECKBOXFLASHFORMAT, wxID_MAINFRAMECHECKBOXFLOWCONTROL, 
 wxID_MAINFRAMECHECKBOXLDR, wxID_MAINFRAMECHECKBOXMDM, 
 wxID_MAINFRAMECHECKBOXPRODUCTCFG, wxID_MAINFRAMECHECKBOXUPDATEENABLECBC, 
 wxID_MAINFRAMECHECKBOXUPDATEENABLEKRM, 
 wxID_MAINFRAMECHECKBOXUPDATEFILRESTART, wxID_MAINFRAMECHOICEADBAPIFACTIONS, 
 wxID_MAINFRAMECHOICEAPPCOMBAUDRATE, wxID_MAINFRAMECHOICEBROMCOMBAUDRATE, 
 wxID_MAINFRAMECHOICECRASHINFO, wxID_MAINFRAMECHOICEHIFBAUDRATE, 
 wxID_MAINFRAMECHOICEPLATINFO, wxID_MAINFRAMECHOICEXMLSOURCETYPE, 
 wxID_MAINFRAMECOMBOBOXADBAPIFDEVICES, wxID_MAINFRAMECOMBOBOXADBAPIFFORWARD, 
 wxID_MAINFRAMECOMBOBOXADBAPIFFORWARDSOCKET, 
 wxID_MAINFRAMECOMBOBOXADBAPIFSYSTEMPROPERTIES, 
 wxID_MAINFRAMECOMBOBOXADBAPIFSYSTEMPROPERTIESVALUE, 
 wxID_MAINFRAMECOMBOBOXATCOMMANDS, wxID_MAINFRAMECOMBOBOXCALIBRATIONFILES, 
 wxID_MAINFRAMECOMBOBOXCOMBLOCKSIZE, wxID_MAINFRAMECOMBOBOXCOMPORT, 
 wxID_MAINFRAMECOMBOBOXCRASHINFOLOGPATH, 
 wxID_MAINFRAMECOMBOBOXFACTRELEASEUPDATE, 
 wxID_MAINFRAMECOMBOBOXFACTUARTSERVER, wxID_MAINFRAMECOMBOBOXFIRMWAREINFO, 
 wxID_MAINFRAMECOMBOBOXLOGFOLDER, wxID_MAINFRAMECOMBOBOXPATH, 
 wxID_MAINFRAMECOMBOBOXSINGLE, wxID_MAINFRAMECOMBOBOXUARTAPPLI, 
 wxID_MAINFRAMECOMBOBOXUARTBT2, wxID_MAINFRAMECOMBOBOXUARTDISCOVERYSELECTPORT, 
 wxID_MAINFRAMECOMBOBOXXMLSOURCEPATH, wxID_MAINFRAMEGAUGEFACTSTATUS, 
 wxID_MAINFRAMENOTEBOOK, wxID_MAINFRAMENOTEBOOKBOARDREPAIR, 
 wxID_MAINFRAMENOTEBOOKUPDATE, wxID_MAINFRAMERADIOBUTTONUARTHIF, 
 wxID_MAINFRAMERADIOBUTTONUSBHIF, wxID_MAINFRAMESTATICBOXADBAPIFACTIONS, 
 wxID_MAINFRAMESTATICBOXADBAPIFCONNECTION, 
 wxID_MAINFRAMESTATICBOXADBAPIFFORWARD, 
 wxID_MAINFRAMESTATICBOXADBAPIFSYSTEMPROPERTIES, 
 wxID_MAINFRAMESTATICBOXATCOMMAND, wxID_MAINFRAMESTATICBOXCALIBRATIONFILES, 
 wxID_MAINFRAMESTATICBOXCONNECTION, wxID_MAINFRAMESTATICBOXCRASHINFO, 
 wxID_MAINFRAMESTATICBOXFACTBOARDREPAIRSETTINGS, 
 wxID_MAINFRAMESTATICBOXFACTRELEASEUPDATE, wxID_MAINFRAMESTATICBOXFACTSTATUS, 
 wxID_MAINFRAMESTATICBOXFACTUARTSERVER, wxID_MAINFRAMESTATICBOXFIRMWAREINFO, 
 wxID_MAINFRAMESTATICBOXHIFSETTINGS, wxID_MAINFRAMESTATICBOXHOSTINTERFACE, 
 wxID_MAINFRAMESTATICBOXIMEI, wxID_MAINFRAMESTATICBOXLIST, 
 wxID_MAINFRAMESTATICBOXPATH, wxID_MAINFRAMESTATICBOXPLATINFO, 
 wxID_MAINFRAMESTATICBOXUARTARCHIVESELECTION, 
 wxID_MAINFRAMESTATICBOXUARTBOOTAGENTSETTINGS, 
 wxID_MAINFRAMESTATICBOXUARTDISCOVERYSERVER, wxID_MAINFRAMESTATICBOXUNLOCK, 
 wxID_MAINFRAMESTATICBOXUPDATEOPTIONS, wxID_MAINFRAMESTATICBOXXMLSOURCES, 
 wxID_MAINFRAMESTATICTEXTADBAPIFACTIONSELECT, 
 wxID_MAINFRAMESTATICTEXTADBAPIFDEVICES, 
 wxID_MAINFRAMESTATICTEXTADBAPIFFORWARD, 
 wxID_MAINFRAMESTATICTEXTADBAPIFFORWARDSOCKET, 
 wxID_MAINFRAMESTATICTEXTADBAPIFSYSTEMPROPERTIES, 
 wxID_MAINFRAMESTATICTEXTADBAPIFSYSTEMPROPERTIESVALUE, 
 wxID_MAINFRAMESTATICTEXTAPPCOMBAUDRATE, 
 wxID_MAINFRAMESTATICTEXTBROMCOMBAUDRATE, 
 wxID_MAINFRAMESTATICTEXTCOMBLOCKSIZE, wxID_MAINFRAMESTATICTEXTCRASHINFO, 
 wxID_MAINFRAMESTATICTEXTFACTRELEASELIST, 
 wxID_MAINFRAMESTATICTEXTFACTUARTSERVER, wxID_MAINFRAMESTATICTEXTFLASHFORMAT, 
 wxID_MAINFRAMESTATICTEXTHIFBAUDRATE, wxID_MAINFRAMESTATICTEXTHOSTINTERFACE, 
 wxID_MAINFRAMESTATICTEXTIMEINOTE, wxID_MAINFRAMESTATICTEXTLIST, 
 wxID_MAINFRAMESTATICTEXTLOGFILE, wxID_MAINFRAMESTATICTEXTLOGFOLDER, 
 wxID_MAINFRAMESTATICTEXTPLATINFO, wxID_MAINFRAMESTATICTEXTSELECTAPPLI, 
 wxID_MAINFRAMESTATICTEXTSELECTBT2, wxID_MAINFRAMESTATICTEXTSELECTPORT, 
 wxID_MAINFRAMESTATICTEXTUARTDISCOVERYSELECTPORT, 
 wxID_MAINFRAMESTATICTEXTXMLSOURCESELESCT, wxID_MAINFRAMESTATUSBAR1, 
 wxID_MAINFRAMETEXTCTRLENTERIMEI, wxID_MAINFRAMETXTCTRLCONSOLE, 
 wxID_MAINFRAMEWINDOWADBAPINTERFACE, wxID_MAINFRAMEWINDOWBOARDREPAIR, 
 wxID_MAINFRAMEWINDOWCONFIGFILES, wxID_MAINFRAMEWINDOWDEBUG, 
 wxID_MAINFRAMEWINDOWDEBUGBOARDREPAIR, wxID_MAINFRAMEWINDOWFACTORYBOARDREPAIR, 
 wxID_MAINFRAMEWINDOWFIRMWARE, wxID_MAINFRAMEWINDOWHOSTINTERFACE, 
 wxID_MAINFRAMEWINDOWUPDATE, 
] = [wx.NewId() for _init_ctrls in range(152)]

[wxID_MAINFRAMEFILECHIPTYPE, wxID_MAINFRAMEFILEINTERFACESWITCH, 
 wxID_MAINFRAMEFILEITEMS2, wxID_MAINFRAMEFILEITEMS3, wxID_MAINFRAMEFILEITEMS8, 
 wxID_MAINFRAMEFILEITEMSCLEARCONSOLE, wxID_MAINFRAMEFILEITEMSSAVELOG, 
 wxID_MAINFRAMEFILEVERB, 
] = [wx.NewId() for _init_coll_File_Items in range(8)]

[wxID_MAINFRAMEVERBOSITYVERBDEBUG, wxID_MAINFRAMEVERBOSITYVERBDUMP, 
 wxID_MAINFRAMEVERBOSITYVERBERR, wxID_MAINFRAMEVERBOSITYVERBINFO, 
 wxID_MAINFRAMEVERBOSITYVERBSILENT, 
] = [wx.NewId() for _init_coll_verbosity_Items in range(5)]

[wxID_MAINFRAMEHELPITEMS0, wxID_MAINFRAMEHELPITEMS2, wxID_MAINFRAMEHELPITEMS3, 
] = [wx.NewId() for _init_coll_Help_Items in range(3)]

[wxID_MAINFRAMEKEYSITEMS0, wxID_MAINFRAMEKEYSITEMS1, wxID_MAINFRAMEKEYSITEMS2, 
 wxID_MAINFRAMEKEYSITEMS3, wxID_MAINFRAMEKEYSITEMS4, 
] = [wx.NewId() for _init_coll_keys_Items in range(5)]

[wxID_MAINFRAMEUPDATERLIBITEMS0] = [wx.NewId() for _init_coll_Updaterlib_Items in range(1)]

[wxID_MAINFRAMETOOLSADBTOOLPATHESELECT, wxID_MAINFRAMETOOLSITEMS0, 
 wxID_MAINFRAMETOOLSITEMS2, wxID_MAINFRAMETOOLSADBLOGCAT
] = [wx.NewId() for _init_coll_Tools_Items in range(4)]

[wxID_MAINFRAMEOEM_FACTOEM_FACT] = [wx.NewId() for _init_coll_OEM_FACT_Items in range(1)]

[wxID_MAINFRAMEICE_ICEICE_ICE] = [wx.NewId() for _init_coll_ICE_ICE_Items in range(1)]

[wxID_MAINFRAMEOEM_FIELDOEM_FIELD] = [wx.NewId() for _init_coll_OEM_FIELD_Items in range(1)]

[wxID_MAINFRAMEICE_OEMICE_OEM] = [wx.NewId() for _init_coll_ICE_OEM_Items in range(1)]

[wxID_MAINFRAMEUPDATERLIBMENUITEMS0] = [wx.NewId() for _init_coll_UpdaterLibMenu_Items in range(1)]

[wxID_MAINFRAMEICE_DBGICE_DBG] = [wx.NewId() for _init_coll_ICE_DBG_Items in range(1)]

class MainFrame(wx.Frame):
    def _init_coll_boxSizerFlashReleaseList3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxDEVICECFG, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxPRODUCTCFG, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxAUDIOCFG, 0, border=0, flag=0)

    def _init_coll_boxSizerConfiguration_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerConfigConnection, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerHifSettings, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.boxSizerConfigMisc, 0, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerUartDiscoveryServer, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerFactReleaseUpdate_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerFactBoardRepairRelease, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextFactReleaseList, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactReleaseList, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.staticBoxSizerFactBoardRepairSettings, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFactReleaseList_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerFactReleaseListAll, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactReleaseList1, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactReleaseList2, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactReleaseList3, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactReleaseList4, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerAdbApIfSystemProperties_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextAdbApIfSystemProperties, 0, border=0,
              flag=0)
        parent.AddWindow(self.comboBoxAdbApIfSystemProperties, 1, border=0,
              flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextAdbApIfSystemPropertiesValue, 0,
              border=0, flag=0)
        parent.AddWindow(self.comboBoxAdbApIfSystemPropertiesValue, 1, border=0,
              flag=0)
        parent.AddWindow(self.buttonAdbApIfSystemPropertiesSet, 0, border=0,
              flag=0)
        parent.AddWindow(self.buttonAdbApIfSystemPropertiesGet, 0, border=0,
              flag=0)

    def _init_coll_boxSizerConfigMisc_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerHostInterface, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerFirmwareInfo_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerBrowseFirmwareInfo, 0, border=0,
              flag=wx.EXPAND)
        parent.AddWindow(self.buttonGetFirmwareInfo, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFactBoardRepair_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerBoardRepairTabs, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerFactUartServer, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerFactStatus, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_MainTopSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.notebook, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerImeiUnlock_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerImei, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerUnlock, 1, border=10,
              flag=wx.LEFT | wx.EXPAND)

    def _init_coll_boxSizerFactStatusControl_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonStartBoardRepair, 1, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonStopBoardRepair, 1, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerRelease_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerFlashRelease1, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashRelease3, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashRelease2, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerUpdateWindow_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerUpdateTabs, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerSelectComPort_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(16, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextSelectPort, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxComPort, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerAdbApIfConnection_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxAdbApIfConnection, 0, border=0, flag=0)
        parent.AddSizer(self.boxSizerAdbApIfConnectionDevice, 0, border=0,
              flag=0)

    def _init_coll_staticBoxSizerDebugArchiveSelect_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextSelectBT2, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerDbgBoardRepairSelBT2, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextSelectAppli, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerDbgBoardRepairSelAPP, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFactStatusGauge_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.gaugeFactStatus, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerFlashing_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerRelease, 0, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerSingleFile, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerBoardRepairTabs_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.notebookBoardRepair, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerDebug_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerCrashInfo, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFirmwareInfos, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.staticBoxSizerATCommand, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerCrashInfo_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerCrashInfoAction, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerCrashInfoLogFolder, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerCrashInfoLogFile, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerSingle2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxSingle, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonSingle, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerDbgBoardRepairSelBT2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxUartBT2, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseBT2, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerFactBoardRepairRelease_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxFactReleaseUpdate, 1, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonFactReleaseUpdate, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonFactBrowseArchive, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFlashReleaseListAll_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxALL, 0, border=0, flag=0)

    def _init_coll_MainBottomSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.txtCtrlConsole, 1, border=0,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_staticBoxSizerUartBootAgentSettings_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextBromComBaudrate, 1, border=0,
              flag=wx.EXPAND)
        parent.AddWindow(self.choiceBromComBaudrate, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextAppComBaudrate, 1, border=0,
              flag=wx.EXPAND)
        parent.AddWindow(self.choiceAppComBaudrate, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerAdbApIfForwardPort_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextAdbApIfForward, 0, border=0, flag=0)
        parent.AddWindow(self.comboBoxAdbApIfForward, 0, border=0, flag=0)
        parent.AddWindow(self.buttonAdbApIfForward, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerHostInterface_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextHostInterface, 0, border=0, flag=0)
        parent.AddWindow(self.radioButtonUsbHif, 0, border=0, flag=0)
        parent.AddWindow(self.radioButtonUartHif, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonApplyHifSwitch, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerFlashReleaseList_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerFlashReleaseListAll, 0, border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashReleaseList1, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashReleaseList3, 0, border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashReleaseList4, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerSingleFile_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerSingle2, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerSingle1, 0, border=0, flag=wx.EXPAND)

    def _init_coll_MainSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.MainTopSizer, 0, border=0, flag=wx.ALL | wx.EXPAND)
        parent.AddSizer(self.MainBottomSizer, 1, border=0,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_staticBoxSizerImei_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerEnterImei, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerIMEINote, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerUnlock_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonUnlock, 1, border=20,
              flag=wx.BOTTOM | wx.TOP | wx.EXPAND)

    def _init_coll_boxSizerFlashReleaseList1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxBT2, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxLDR, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxMDM, 0, border=0, flag=0)

    def _init_coll_boxSizerIMEINote_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextIMEINote, 0, border=0, flag=0)

    def _init_coll_boxSizerFactReleaseList2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFactReleaseUpdateListMDM, 0, border=0,
              flag=0)

    def _init_coll_staticBoxSizerPlatInfo_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextPlatInfo, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.choicePlatInfo, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonStartPlatInfo, 0, border=0, flag=0)

    def _init_coll_boxSizerXmlSourceProgram_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxXmlSourcePath, 1, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseXmlSource, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonProgramXmlSource, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerSingle1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonFlashSingle, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerFactReleaseList1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFactReleaseUpdateListBT2, 0, border=0,
              flag=0)
        parent.AddWindow(self.checkBoxFactUpdateReleaseListLDR, 0, border=0,
              flag=0)

    def _init_coll_boxSizerFactReleaseList3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFactUpdateReleaseListPLATCG, 0, border=0,
              flag=0)
        parent.AddWindow(self.checkBoxFactUpdateReleaseListCALIB, 0, border=0,
              flag=0)

    def _init_coll_boxSizerFirmwareInfos_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerPlatInfo, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.staticBoxSizerFirmwareInfo, 1, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerMainDebugBoardRepair_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerDebugArchiveSelect, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerUartBootAgentSettings, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerCalibrationFiles_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxCalibrationFiles, 1, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseCalibrationFiles, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonFlashCalibrationFiles, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerATCommand_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxAtCommands, 0, border=0, flag=wx.EXPAND)

    def _init_coll_staticBoxSizerUartDiscoveryServer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextUartDiscoverySelectPort, 0, border=0,
              flag=0)
        parent.AddWindow(self.comboBoxUartDiscoverySelectPort, 0, border=0,
              flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonUartDiscoveryStartServer, 1, border=0,
              flag=wx.EXPAND)
        parent.AddWindow(self.buttonUartDiscoveryStopServer, 1, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerHifBaudrate_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextHifBaudrate, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.choiceHifBaudrate, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextCOMBlockSize, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxCOMBlockSize, 0, border=0, flag=0)

    def _init_coll_boxSizerAdbApIfForwardSocket_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextAdbApIfForwardSocket, 0, border=0,
              flag=0)
        parent.AddWindow(self.comboBoxAdbApIfForwardSocket, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerFactBoardRepairSettings_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextFlashFormat, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.checkBoxFlashFormat, 0, border=0, flag=0)

    def _init_coll_boxSizerFlashRelease2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.buttonFlashRelease, 1, border=0, flag=wx.EXPAND)

    def _init_coll_staticBoxSizerAdbApIfActions_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextAdbApIfActionSelect, 0, border=0,
              flag=0)
        parent.AddWindow(self.choiceAdbApIfActions, 0, border=0, flag=0)
        parent.AddWindow(self.buttonAdbApIfActionsStart, 0, border=0, flag=0)

    def _init_coll_boxSizerFlashRelease3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextList, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFlashReleaseList, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerConfigConnection_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxAutoDetect, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerSelectComPort, 0, border=0, flag=0)

    def _init_coll_boxSizerFlashRelease1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxPath, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseReleaseArchive, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonPathBrowse, 0, border=0, flag=wx.EXPAND)

    def _init_coll_staticBoxSizerAdbApIfForward_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerAdbApIfForwardPort, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.boxSizerAdbApIfForwardSocket, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerCrashInfoAction_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextCrashInfo, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.choiceCrashInfo, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonCrashInfo, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.checkBoxCrashInfo, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerBrowseFirmwareInfo_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxFirmwareInfo, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseFirmwareInfo, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseDirFirmwareInfo, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_staticBoxSizerUpdateOptions_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxUpdateEnableCbc, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxUpdateEnableKrm, 0, border=0, flag=0)
        parent.AddWindow(self.checkBoxUpdateFilRestart, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerFactUartServer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextFactUartServer, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxFactUartServer, 0, border=0, flag=0)

    def _init_coll_boxSizerAdbApIfConnectionDevice_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.staticTextAdbApIfDevices, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxAdbApIfDevices, 0, border=0, flag=0)
        parent.AddWindow(self.buttonAdbApIfScan, 0, border=0, flag=0)

    def _init_coll_BoxSizerAdbApInterface_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerAdbApIfConnection, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerAdbApIfForward, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerAdbApIfSystemProperties, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerAdbApIfActions, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFlashReleaseList4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxBT3, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerHifSettings_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFlowControl, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerHifBaudrate, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerXmlSources_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerXmlSourceSelect, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerXmlSourceProgram, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFactReleaseListAll_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFactReleaseListAll, 0, border=0, flag=0)

    def _init_coll_staticBoxSizerFactStatus_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizerFactStatusGauge, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerFactStatusControl, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerMainFactBoardRepair_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerFactReleaseUpdate, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerFactReleaseList4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.checkBoxFactReleaseUpdateListDEVICECFG, 0,
              border=0, flag=0)
        parent.AddWindow(self.checkBoxFactReleaseUpdateListPRODUCTCFG, 0,
              border=0, flag=0)

    def _init_coll_boxSizerDbgBoardRepairSelAPP_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.comboBoxUartAppli, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseAppli, 0, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizerXmlSourceSelect_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextXmlSourceSelesct, 0, border=0, flag=0)
        parent.AddWindow(self.choiceXmlSourceType, 0, border=0, flag=0)

    def _init_coll_boxSizerUpdateTabs_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.notebookUpdate, 1, border=0, flag=wx.EXPAND)
        parent.AddSizer(self.staticBoxSizerUpdateOptions, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerCrashInfoLogFile_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextLogFile, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxCrashInfoLogPath, 1, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonCrashInfoBrowse, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerCrashInfoLogFolder_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.staticTextLogFolder, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.comboBoxLogFolder, 1, border=0, flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonBrowseLogFolder, 0, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizerEnterImei_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.textCtrlEnterImei, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.buttonFlashImei, 0, border=0, flag=0)

    def _init_coll_boxSizerConfigFiles_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.staticBoxSizerXmlSources, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.staticBoxSizerCalibrationFiles, 0, border=0,
              flag=wx.EXPAND)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddSizer(self.boxSizerImeiUnlock, 0, border=0, flag=wx.EXPAND)

    def _init_coll_verbosity_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEVERBOSITYVERBINFO,
              kind=wx.ITEM_RADIO, text='VERB_INFO')
        parent.Append(help='', id=wxID_MAINFRAMEVERBOSITYVERBSILENT,
              kind=wx.ITEM_RADIO, text='VERB_SILENT')
        parent.Append(help='', id=wxID_MAINFRAMEVERBOSITYVERBERR,
              kind=wx.ITEM_RADIO, text='VERB_ERR')
        parent.Append(help='', id=wxID_MAINFRAMEVERBOSITYVERBDEBUG,
              kind=wx.ITEM_RADIO, text='VERB_DEBUG')
        parent.Append(help='', id=wxID_MAINFRAMEVERBOSITYVERBDUMP,
              kind=wx.ITEM_RADIO, text='VERB_DUMP')
        self.Bind(wx.EVT_MENU, self.OnVerbosityVerbinfoMenu,
              id=wxID_MAINFRAMEVERBOSITYVERBINFO)
        self.Bind(wx.EVT_MENU, self.OnVerbosityVerbsilentMenu,
              id=wxID_MAINFRAMEVERBOSITYVERBSILENT)
        self.Bind(wx.EVT_MENU, self.OnVerbosityVerberrMenu,
              id=wxID_MAINFRAMEVERBOSITYVERBERR)
        self.Bind(wx.EVT_MENU, self.OnVerbosityVerbdumpMenu,
              id=wxID_MAINFRAMEVERBOSITYVERBDUMP)
        self.Bind(wx.EVT_MENU, self.OnVerbosityVerbdebugMenu,
              id=wxID_MAINFRAMEVERBOSITYVERBDEBUG)

    def _init_coll_ICE_DBG_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEICE_DBGICE_DBG,
              kind=wx.ITEM_NORMAL, text='Change ICE_DBG...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnICE_DBGIce_dbgMenu,
              id=wxID_MAINFRAMEICE_DBGICE_DBG)

    def _init_coll_UpdaterLibMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEUPDATERLIBMENUITEMS0,
              kind=wx.ITEM_NORMAL, text='Switch UpdaterLib...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnUpdaterLibMenuItems0Menu,
              id=wxID_MAINFRAMEUPDATERLIBMENUITEMS0)

    def _init_coll_File_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEFILEINTERFACESWITCH,
              kind=wx.ITEM_NORMAL, text='Switch to Android Mode')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_MAINFRAMEFILEITEMSCLEARCONSOLE,
              kind=wx.ITEM_NORMAL, text='Clear console...')
        parent.AppendSeparator()
        parent.AppendMenu(help='', id=wxID_MAINFRAMEFILEITEMS8,
              submenu=self.keys, text='Change key path')
        parent.AppendSeparator()
        parent.AppendMenu(help='', id=wxID_MAINFRAMEFILEVERB,
              submenu=self.verbosity, text='Verbosity')
        parent.Append(help='', id=wxID_MAINFRAMEFILEITEMS3, kind=wx.ITEM_NORMAL,
              text='Scan connected target...')
        parent.Append(help='', id=wxID_MAINFRAMEFILEITEMSSAVELOG,
              kind=wx.ITEM_NORMAL, text='Save Log...')
        parent.AppendSeparator()
        parent.AppendMenu(help='', id=wxID_MAINFRAMEFILECHIPTYPE,
              submenu=self.chipType, text='Select Chip Type')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_MAINFRAMEFILEITEMS2, kind=wx.ITEM_NORMAL,
              text='Exit')
        self.Bind(wx.EVT_MENU, self.OnFileItems2Menu,
              id=wxID_MAINFRAMEFILEITEMS2)
        self.Bind(wx.EVT_MENU, self.OnFileItems3Menu,
              id=wxID_MAINFRAMEFILEITEMS3)
        self.Bind(wx.EVT_MENU, self.OnFileItemsclearconsoleMenu,
              id=wxID_MAINFRAMEFILEITEMSCLEARCONSOLE)
        self.Bind(wx.EVT_MENU, self.OnFileItemssavelogMenu,
              id=wxID_MAINFRAMEFILEITEMSSAVELOG)
        self.Bind(wx.EVT_MENU, self.OnFileInterfaceswitchMenu,
              id=wxID_MAINFRAMEFILEINTERFACESWITCH)

    def _init_coll_keys_Items(self, parent):
        # generated method, don't edit

        parent.AppendMenu(help='', id=wxID_MAINFRAMEKEYSITEMS0,
              submenu=self.ICE_ICE, text='ICE_ICE')
        parent.AppendMenu(help='', id=wxID_MAINFRAMEKEYSITEMS1,
              submenu=self.ICE_OEM, text='ICE_OEM')
        parent.AppendMenu(help='', id=wxID_MAINFRAMEKEYSITEMS2,
              submenu=self.OEM_FACT, text='OEM_FACT')
        parent.AppendMenu(help='', id=wxID_MAINFRAMEKEYSITEMS3,
              submenu=self.OEM_FIELD, text='OEM_FIELD')
        parent.AppendMenu(help='', id=wxID_MAINFRAMEKEYSITEMS4,
              submenu=self.ICE_DBG, text='ICE_DBG')

    def _init_coll_ICE_OEM_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEICE_OEMICE_OEM,
              kind=wx.ITEM_NORMAL, text='Change ICE_OEM...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnICE_OEMIce_oemMenu,
              id=wxID_MAINFRAMEICE_OEMICE_OEM)

    def _init_coll_Tools_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMETOOLSITEMS0,
              kind=wx.ITEM_NORMAL, text='Data File Tools...')
        parent.AppendSeparator()
        parent.AppendMenu(help='', id=wxID_MAINFRAMETOOLSITEMS2,
              submenu=self.UpdaterLibMenu, text='UpdaterLib')
        parent.Append(help='', id=wxID_MAINFRAMETOOLSADBTOOLPATHESELECT,
              kind=wx.ITEM_NORMAL, text='ADB tool path...')
        self.menuLogcat=parent.Append(help='', id=wxID_MAINFRAMETOOLSADBLOGCAT,
              kind=wx.ITEM_NORMAL, text='ADB logcat')
        self.Bind(wx.EVT_MENU, self.OnToolsItems0Menu,
              id=wxID_MAINFRAMETOOLSITEMS0)
        self.Bind(wx.EVT_MENU, self.OnToolsAdbtoolpatheselectMenu,
              id=wxID_MAINFRAMETOOLSADBTOOLPATHESELECT)
        self.Bind(wx.EVT_MENU, self.OnToolsAdbLogcat,
              id=wxID_MAINFRAMETOOLSADBLOGCAT)

    def _init_coll_Main_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.File, title='File')
        parent.Append(menu=self.Tools, title='Tools')
        parent.Append(menu=self.Help, title='Help')

    def _init_coll_OEM_FIELD_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEOEM_FIELDOEM_FIELD,
              kind=wx.ITEM_NORMAL, text='Change OEM_FIELD...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnOEM_FIELDOem_fieldMenu,
              id=wxID_MAINFRAMEOEM_FIELDOEM_FIELD)

    def _init_coll_ICE_ICE_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEICE_ICEICE_ICE,
              kind=wx.ITEM_NORMAL, text='Change ICE_ICE...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnICE_ICEIce_iceMenu,
              id=wxID_MAINFRAMEICE_ICEICE_ICE)

    def _init_coll_OEM_FACT_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEOEM_FACTOEM_FACT,
              kind=wx.ITEM_NORMAL, text='Change OEM_FACT...')
        parent.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnOEM_FACTOem_factMenu,
              id=wxID_MAINFRAMEOEM_FACTOEM_FACT)

    def _init_coll_Help_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_MAINFRAMEHELPITEMS2, kind=wx.ITEM_NORMAL,
              text='User Guide')
        parent.AppendSeparator()
        parent.Append(help='', id=wxID_MAINFRAMEHELPITEMS3, kind=wx.ITEM_NORMAL,
              text='Configuration')
        parent.Append(help='', id=wxID_MAINFRAMEHELPITEMS0, kind=wx.ITEM_NORMAL,
              text='About')
        self.Bind(wx.EVT_MENU, self.OnHelpItems0Menu,
              id=wxID_MAINFRAMEHELPITEMS0)
        self.Bind(wx.EVT_MENU, self.OnHelpItems2Menu,
              id=wxID_MAINFRAMEHELPITEMS2)
        self.Bind(wx.EVT_MENU, self.OnHelpItems3Menu,
              id=wxID_MAINFRAMEHELPITEMS3)

    def _init_coll_notebook_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(page=self.windowUpdate, select=True, text='Update')
        parent.AddPage(page=self.windowDebug, select=False, text='Debug')
        parent.AddPage(page=self.windowHostInterface, select=False,
              text='Host Interface')
        parent.AddPage(page=self.windowBoardrepair, select=False,
              text='Board Repair')
        parent.AddPage(page=self.windowAdbApInterface, select=False,
              text='ADB Interface')

    def _init_coll_notebookUpdate_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(page=self.windowFirmware, select=True, text='Firmware')
        parent.AddPage(page=self.windowConfigFiles, select=False,
              text='Config.Files')

    def _init_coll_notebookBoardRepair_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(page=self.windowDebugBoardRepair, select=True,
              text='Boot Agent')
        parent.AddPage(page=self.windowFactoryBoardRepair, select=False,
              text='Repair Agent')

    def _init_sizers(self):
        # generated method, don't edit
        self.MainTopSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.MainSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFlashing = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerRelease = wx.StaticBoxSizer(box=self.staticBoxPath,
              orient=wx.VERTICAL)

        self.staticBoxSizerSingleFile = wx.StaticBoxSizer(box=self.staticBoxList,
              orient=wx.VERTICAL)

        self.boxSizerFlashRelease1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFlashRelease2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.MainBottomSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerSingle1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerSingle2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFlashRelease3 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFlashReleaseList = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFlashReleaseListAll = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFlashReleaseList1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFlashReleaseList2 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFlashReleaseList3 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerDebug = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerCrashInfo = wx.StaticBoxSizer(box=self.staticBoxCrashInfo,
              orient=wx.VERTICAL)

        self.staticBoxSizerPlatInfo = wx.StaticBoxSizer(box=self.staticBoxPlatInfo,
              orient=wx.HORIZONTAL)

        self.boxSizerConfiguration = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerConfigConnection = wx.StaticBoxSizer(box=self.staticBoxConnection,
              orient=wx.VERTICAL)

        self.boxSizerSelectComPort = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerATCommand = wx.StaticBoxSizer(box=self.staticBoxATCommand,
              orient=wx.VERTICAL)

        self.boxSizerConfigMisc = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerHostInterface = wx.StaticBoxSizer(box=self.staticBoxHostInterface,
              orient=wx.HORIZONTAL)

        self.boxSizerConfigFiles = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerImei = wx.StaticBoxSizer(box=self.staticBoxImei,
              orient=wx.VERTICAL)

        self.boxSizerEnterImei = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerIMEINote = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFactBoardRepair = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerFactUartServer = wx.StaticBoxSizer(box=self.staticBoxFactUartServer,
              orient=wx.HORIZONTAL)

        self.staticBoxSizerFactStatus = wx.StaticBoxSizer(box=self.staticBoxFactStatus,
              orient=wx.VERTICAL)

        self.boxSizerFactStatusGauge = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFactStatusControl = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerCalibrationFiles = wx.StaticBoxSizer(box=self.staticBoxCalibrationFiles,
              orient=wx.HORIZONTAL)

        self.boxSizerFirmwareInfos = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerFirmwareInfo = wx.StaticBoxSizer(box=self.staticBoxFirmwareInfo,
              orient=wx.VERTICAL)

        self.boxSizerBrowseFirmwareInfo = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerUartDiscoveryServer = wx.StaticBoxSizer(box=self.staticBoxUartDiscoveryServer,
              orient=wx.HORIZONTAL)

        self.boxSizerFactReleaseList = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFactReleaseListAll = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFactReleaseList1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFactReleaseList2 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerFactReleaseList3 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerBoardRepairTabs = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerMainFactBoardRepair = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerMainDebugBoardRepair = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerFactReleaseUpdate = wx.StaticBoxSizer(box=self.staticBoxFactReleaseUpdate,
              orient=wx.VERTICAL)

        self.boxSizerFactBoardRepairRelease = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerDebugArchiveSelect = wx.StaticBoxSizer(box=self.staticBoxUartArchiveSelection,
              orient=wx.VERTICAL)

        self.boxSizerDbgBoardRepairSelBT2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerDbgBoardRepairSelAPP = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerXmlSources = wx.StaticBoxSizer(box=self.staticBoxXmlSources,
              orient=wx.VERTICAL)

        self.boxSizerXmlSourceSelect = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerXmlSourceProgram = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerCrashInfoAction = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerCrashInfoLogFile = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerFactBoardRepairSettings = wx.StaticBoxSizer(box=self.staticBoxFactBoardRepairSettings,
              orient=wx.HORIZONTAL)

        self.boxSizerCrashInfoLogFolder = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerFactReleaseList4 = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerHifSettings = wx.StaticBoxSizer(box=self.staticBoxHifSettings,
              orient=wx.VERTICAL)

        self.boxSizerHifBaudrate = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerUartBootAgentSettings = wx.StaticBoxSizer(box=self.staticBoxUartBootAgentSettings,
              orient=wx.HORIZONTAL)

        self.boxSizerFlashReleaseList4 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerUpdateWindow = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizerUpdateTabs = wx.BoxSizer(orient=wx.VERTICAL)

        self.BoxSizerAdbApInterface = wx.BoxSizer(orient=wx.VERTICAL)

        self.staticBoxSizerAdbApIfConnection = wx.StaticBoxSizer(box=self.staticBoxAdbApIfConnection,
              orient=wx.VERTICAL)

        self.staticBoxSizerAdbApIfForward = wx.StaticBoxSizer(box=self.staticBoxAdbApIfForward,
              orient=wx.VERTICAL)

        self.staticBoxSizerAdbApIfSystemProperties = wx.StaticBoxSizer(box=self.staticBoxAdbApIfSystemProperties,
              orient=wx.HORIZONTAL)

        self.boxSizerAdbApIfForwardPort = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerAdbApIfForwardSocket = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerAdbApIfConnectionDevice = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerAdbApIfActions = wx.StaticBoxSizer(box=self.staticBoxAdbApIfActions,
              orient=wx.HORIZONTAL)

        self.staticBoxSizerUpdateOptions = wx.StaticBoxSizer(box=self.staticBoxUpdateOptions,
              orient=wx.HORIZONTAL)

        self.boxSizerImeiUnlock = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.staticBoxSizerUnlock = wx.StaticBoxSizer(box=self.staticBoxUnlock,
              orient=wx.VERTICAL)

        self._init_coll_MainTopSizer_Items(self.MainTopSizer)
        self._init_coll_MainSizer_Items(self.MainSizer)
        self._init_coll_boxSizerFlashing_Items(self.boxSizerFlashing)
        self._init_coll_staticBoxSizerRelease_Items(self.staticBoxSizerRelease)
        self._init_coll_staticBoxSizerSingleFile_Items(self.staticBoxSizerSingleFile)
        self._init_coll_boxSizerFlashRelease1_Items(self.boxSizerFlashRelease1)
        self._init_coll_boxSizerFlashRelease2_Items(self.boxSizerFlashRelease2)
        self._init_coll_MainBottomSizer_Items(self.MainBottomSizer)
        self._init_coll_boxSizerSingle1_Items(self.boxSizerSingle1)
        self._init_coll_boxSizerSingle2_Items(self.boxSizerSingle2)
        self._init_coll_boxSizerFlashRelease3_Items(self.boxSizerFlashRelease3)
        self._init_coll_boxSizerFlashReleaseList_Items(self.boxSizerFlashReleaseList)
        self._init_coll_boxSizerFlashReleaseListAll_Items(self.boxSizerFlashReleaseListAll)
        self._init_coll_boxSizerFlashReleaseList1_Items(self.boxSizerFlashReleaseList1)
        self._init_coll_boxSizerFlashReleaseList3_Items(self.boxSizerFlashReleaseList3)
        self._init_coll_boxSizerDebug_Items(self.boxSizerDebug)
        self._init_coll_staticBoxSizerCrashInfo_Items(self.staticBoxSizerCrashInfo)
        self._init_coll_staticBoxSizerPlatInfo_Items(self.staticBoxSizerPlatInfo)
        self._init_coll_boxSizerConfiguration_Items(self.boxSizerConfiguration)
        self._init_coll_staticBoxSizerConfigConnection_Items(self.staticBoxSizerConfigConnection)
        self._init_coll_boxSizerSelectComPort_Items(self.boxSizerSelectComPort)
        self._init_coll_staticBoxSizerATCommand_Items(self.staticBoxSizerATCommand)
        self._init_coll_boxSizerConfigMisc_Items(self.boxSizerConfigMisc)
        self._init_coll_staticBoxSizerHostInterface_Items(self.staticBoxSizerHostInterface)
        self._init_coll_boxSizerConfigFiles_Items(self.boxSizerConfigFiles)
        self._init_coll_staticBoxSizerImei_Items(self.staticBoxSizerImei)
        self._init_coll_boxSizerEnterImei_Items(self.boxSizerEnterImei)
        self._init_coll_boxSizerIMEINote_Items(self.boxSizerIMEINote)
        self._init_coll_boxSizerFactBoardRepair_Items(self.boxSizerFactBoardRepair)
        self._init_coll_staticBoxSizerFactUartServer_Items(self.staticBoxSizerFactUartServer)
        self._init_coll_staticBoxSizerFactStatus_Items(self.staticBoxSizerFactStatus)
        self._init_coll_boxSizerFactStatusGauge_Items(self.boxSizerFactStatusGauge)
        self._init_coll_boxSizerFactStatusControl_Items(self.boxSizerFactStatusControl)
        self._init_coll_staticBoxSizerCalibrationFiles_Items(self.staticBoxSizerCalibrationFiles)
        self._init_coll_boxSizerFirmwareInfos_Items(self.boxSizerFirmwareInfos)
        self._init_coll_staticBoxSizerFirmwareInfo_Items(self.staticBoxSizerFirmwareInfo)
        self._init_coll_boxSizerBrowseFirmwareInfo_Items(self.boxSizerBrowseFirmwareInfo)
        self._init_coll_staticBoxSizerUartDiscoveryServer_Items(self.staticBoxSizerUartDiscoveryServer)
        self._init_coll_boxSizerFactReleaseList_Items(self.boxSizerFactReleaseList)
        self._init_coll_boxSizerFactReleaseListAll_Items(self.boxSizerFactReleaseListAll)
        self._init_coll_boxSizerFactReleaseList1_Items(self.boxSizerFactReleaseList1)
        self._init_coll_boxSizerFactReleaseList2_Items(self.boxSizerFactReleaseList2)
        self._init_coll_boxSizerFactReleaseList3_Items(self.boxSizerFactReleaseList3)
        self._init_coll_boxSizerBoardRepairTabs_Items(self.boxSizerBoardRepairTabs)
        self._init_coll_boxSizerMainFactBoardRepair_Items(self.boxSizerMainFactBoardRepair)
        self._init_coll_boxSizerMainDebugBoardRepair_Items(self.boxSizerMainDebugBoardRepair)
        self._init_coll_staticBoxSizerFactReleaseUpdate_Items(self.staticBoxSizerFactReleaseUpdate)
        self._init_coll_boxSizerFactBoardRepairRelease_Items(self.boxSizerFactBoardRepairRelease)
        self._init_coll_staticBoxSizerDebugArchiveSelect_Items(self.staticBoxSizerDebugArchiveSelect)
        self._init_coll_boxSizerDbgBoardRepairSelBT2_Items(self.boxSizerDbgBoardRepairSelBT2)
        self._init_coll_boxSizerDbgBoardRepairSelAPP_Items(self.boxSizerDbgBoardRepairSelAPP)
        self._init_coll_staticBoxSizerXmlSources_Items(self.staticBoxSizerXmlSources)
        self._init_coll_boxSizerXmlSourceSelect_Items(self.boxSizerXmlSourceSelect)
        self._init_coll_boxSizerXmlSourceProgram_Items(self.boxSizerXmlSourceProgram)
        self._init_coll_boxSizerCrashInfoAction_Items(self.boxSizerCrashInfoAction)
        self._init_coll_boxSizerCrashInfoLogFile_Items(self.boxSizerCrashInfoLogFile)
        self._init_coll_staticBoxSizerFactBoardRepairSettings_Items(self.staticBoxSizerFactBoardRepairSettings)
        self._init_coll_boxSizerCrashInfoLogFolder_Items(self.boxSizerCrashInfoLogFolder)
        self._init_coll_boxSizerFactReleaseList4_Items(self.boxSizerFactReleaseList4)
        self._init_coll_staticBoxSizerHifSettings_Items(self.staticBoxSizerHifSettings)
        self._init_coll_boxSizerHifBaudrate_Items(self.boxSizerHifBaudrate)
        self._init_coll_staticBoxSizerUartBootAgentSettings_Items(self.staticBoxSizerUartBootAgentSettings)
        self._init_coll_boxSizerFlashReleaseList4_Items(self.boxSizerFlashReleaseList4)
        self._init_coll_boxSizerUpdateWindow_Items(self.boxSizerUpdateWindow)
        self._init_coll_boxSizerUpdateTabs_Items(self.boxSizerUpdateTabs)
        self._init_coll_BoxSizerAdbApInterface_Items(self.BoxSizerAdbApInterface)
        self._init_coll_staticBoxSizerAdbApIfConnection_Items(self.staticBoxSizerAdbApIfConnection)
        self._init_coll_staticBoxSizerAdbApIfForward_Items(self.staticBoxSizerAdbApIfForward)
        self._init_coll_staticBoxSizerAdbApIfSystemProperties_Items(self.staticBoxSizerAdbApIfSystemProperties)
        self._init_coll_boxSizerAdbApIfForwardPort_Items(self.boxSizerAdbApIfForwardPort)
        self._init_coll_boxSizerAdbApIfForwardSocket_Items(self.boxSizerAdbApIfForwardSocket)
        self._init_coll_boxSizerAdbApIfConnectionDevice_Items(self.boxSizerAdbApIfConnectionDevice)
        self._init_coll_staticBoxSizerAdbApIfActions_Items(self.staticBoxSizerAdbApIfActions)
        self._init_coll_staticBoxSizerUpdateOptions_Items(self.staticBoxSizerUpdateOptions)
        self._init_coll_boxSizerImeiUnlock_Items(self.boxSizerImeiUnlock)
        self._init_coll_staticBoxSizerUnlock_Items(self.staticBoxSizerUnlock)

        self.SetSizer(self.MainSizer)
        self.windowDebug.SetSizer(self.boxSizerDebug)
        self.windowHostInterface.SetSizer(self.boxSizerConfiguration)
        self.windowFactoryBoardRepair.SetSizer(self.boxSizerMainFactBoardRepair)
        self.windowConfigFiles.SetSizer(self.boxSizerConfigFiles)
        self.windowUpdate.SetSizer(self.boxSizerUpdateWindow)
        self.windowFirmware.SetSizer(self.boxSizerFlashing)
        self.windowBoardrepair.SetSizer(self.boxSizerFactBoardRepair)
        self.windowDebugBoardRepair.SetSizer(self.boxSizerMainDebugBoardRepair)
        self.windowAdbApInterface.SetSizer(self.BoxSizerAdbApInterface)

    def _init_utils(self):
        # generated method, don't edit
        self.Main = wx.MenuBar()
        self.Main.SetEvtHandlerEnabled(False)

        self.File = wx.Menu(title='')
        self.File.SetEvtHandlerEnabled(False)

        self.Help = wx.Menu(title='')
        self.Help.SetEvtHandlerEnabled(False)

        self.verbosity = wx.Menu(title='')
        self.verbosity.SetEvtHandlerEnabled(False)

        self.keys = wx.Menu(title='')
        self.keys.SetEvtHandlerEnabled(False)

        self.Tools = wx.Menu(title='')

        self.ICE_OEM = wx.Menu(title='ICE_OEM')

        self.OEM_FACT = wx.Menu(title='OEM_FACT')

        self.ICE_ICE = wx.Menu(title='ICE_ICE')

        self.OEM_FIELD = wx.Menu(title='OEM_FIELD')

        self.UpdaterLibMenu = wx.Menu(title='')

        self.chipType = wx.Menu(title='')
        self.chipType.SetEvtHandlerEnabled(False)

        self.ICE_DBG = wx.Menu(title='ICE_DBG')

        self._init_coll_Main_Menus(self.Main)
        self._init_coll_File_Items(self.File)
        self._init_coll_Help_Items(self.Help)
        self._init_coll_verbosity_Items(self.verbosity)
        self._init_coll_keys_Items(self.keys)
        self._init_coll_Tools_Items(self.Tools)
        self._init_coll_ICE_OEM_Items(self.ICE_OEM)
        self._init_coll_OEM_FACT_Items(self.OEM_FACT)
        self._init_coll_ICE_ICE_Items(self.ICE_ICE)
        self._init_coll_OEM_FIELD_Items(self.OEM_FIELD)
        self._init_coll_UpdaterLibMenu_Items(self.UpdaterLibMenu)
        self._init_coll_ICE_DBG_Items(self.ICE_DBG)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='MainFrame',
              parent=prnt, pos=wx.Point(617, 181), size=wx.Size(636, 677),
              style=wx.DEFAULT_FRAME_STYLE, title='Ristretto')
        self._init_utils()
        self.SetClientSize(wx.Size(628, 645))
        self.SetBackgroundColour(wx.Colour(212, 208, 200))
        self.SetToolTipString('')
        self.SetIcon(wx.Icon('icera.ico',wx.BITMAP_TYPE_ICO))
        self.SetMinSize(wx.Size(572, -1))
        self.SetHelpText('')
        self.SetMenuBar(self.Main)
        self.Bind(wx.EVT_CLOSE, self.OnFrame1Close)

        self.statusBar1 = wx.StatusBar(id=wxID_MAINFRAMESTATUSBAR1,
              name='statusBar1', parent=self,
              style=wx.ALWAYS_SHOW_SB | wx.CLIP_CHILDREN | wx.STATIC_BORDER | wx.ST_SIZEGRIP | wx.MAXIMIZE_BOX)
        self.statusBar1.SetFieldsCount(3)
        self.statusBar1.Center(wx.HORIZONTAL)
        self.statusBar1.Enable(True)
        self.statusBar1.SetHelpText('')
        self.statusBar1.SetLabel('')
        self.statusBar1.SetToolTipString('')
        self.statusBar1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.SetStatusBar(self.statusBar1)

        self.txtCtrlConsole = wx.TextCtrl(id=wxID_MAINFRAMETXTCTRLCONSOLE,
              name='txtCtrlConsole', parent=self,
              style=wx.TE_READONLY | wx.TE_MULTILINE, value='')
        self.txtCtrlConsole.SetBackgroundColour(wx.Colour(64, 0, 64))
        self.txtCtrlConsole.SetForegroundColour(wx.Colour(192, 192, 192))
        self.txtCtrlConsole.Bind(wx.EVT_TEXT_ENTER,
              self.OnTxtCtrlConsoleTextEnter, id=wxID_MAINFRAMETXTCTRLCONSOLE)
        self.txtCtrlConsole.Bind(wx.EVT_CHAR, self.OnTxtCtrlConsoleChar,
              id=wxID_MAINFRAMETXTCTRLCONSOLE)

        self.notebook = wx.Notebook(id=wxID_MAINFRAMENOTEBOOK, name='notebook',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(628, 370), style=0)
        self.notebook.SetFitToCurrentPage(True)
        self.notebook.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
        self.notebook.SetMinSize(wx.Size(564, 370))
        self.notebook.SetLabel('')
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
              self.OnNotebookNotebookPageChanged, id=wxID_MAINFRAMENOTEBOOK)

        self.windowUpdate = wx.Panel(id=wxID_MAINFRAMEWINDOWUPDATE,
              name='windowUpdate', parent=self.notebook, pos=wx.Point(0, 0),
              size=wx.Size(620, 341), style=wx.TAB_TRAVERSAL)

        self.notebookUpdate = wx.Notebook(id=wxID_MAINFRAMENOTEBOOKUPDATE,
              name='notebookUpdate', parent=self.windowUpdate, pos=wx.Point(0,
              0), size=wx.Size(620, 299), style=wx.STATIC_BORDER | wx.NB_LEFT)

        self.windowConfigFiles = wx.Panel(id=wxID_MAINFRAMEWINDOWCONFIGFILES,
              name='windowConfigFilesUpdate', parent=self.notebookUpdate,
              pos=wx.Point(0, 0), size=wx.Size(590, 291),
              style=wx.TAB_TRAVERSAL)

        self.windowFirmware = wx.Panel(id=wxID_MAINFRAMEWINDOWFIRMWARE,
              name='windowFirmwareUpdate', parent=self.notebookUpdate,
              pos=wx.Point(0, 0), size=wx.Size(590, 291),
              style=wx.TAB_TRAVERSAL)

        self.windowDebug = wx.Panel(id=wxID_MAINFRAMEWINDOWDEBUG,
              name='windowDebug', parent=self.notebook, pos=wx.Point(0, 0),
              size=wx.Size(620, 341), style=0)

        self.staticBoxPath = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXPATH,
              label='Release Update', name='staticBoxPath',
              parent=self.windowFirmware, pos=wx.Point(0, 0), size=wx.Size(590,
              167), style=0)

        self.staticBoxList = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXLIST,
              label='Single File Update', name='staticBoxList',
              parent=self.windowFirmware, style=0)

        self.comboBoxPath = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXPATH, name='comboBoxPath',
              parent=self.windowFirmware, style=0, value='')
        self.comboBoxPath.SetLabel('')
        self.comboBoxPath.SetInsertionPoint(4)

        self.buttonPathBrowse = wx.Button(id=wxID_MAINFRAMEBUTTONPATHBROWSE,
              label='Browse...', name='buttonPathBrowse',
              parent=self.windowFirmware, style=0)
        self.buttonPathBrowse.Bind(wx.EVT_BUTTON, self.OnButtonPathBrowseButton,
              id=wxID_MAINFRAMEBUTTONPATHBROWSE)

        self.comboBoxSingle = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXSINGLE, name='comboBoxSingle',
              parent=self.windowFirmware, style=0, value='')
        self.comboBoxSingle.SetLabel('')

        self.buttonSingle = wx.Button(id=wxID_MAINFRAMEBUTTONSINGLE,
              label='Browse...', name='buttonSingle',
              parent=self.windowFirmware, style=0)
        self.buttonSingle.Bind(wx.EVT_BUTTON, self.OnButtonBrowseSingleButton,
              id=wxID_MAINFRAMEBUTTONSINGLE)

        self.buttonFlashSingle = wx.Button(id=wxID_MAINFRAMEBUTTONFLASHSINGLE,
              label='Flash', name='buttonFlashSingle',
              parent=self.windowFirmware, pos=wx.Point(5, 224),
              size=wx.Size(580, 23), style=0)
        self.buttonFlashSingle.Bind(wx.EVT_BUTTON,
              self.OnButtonFlashSingleButton,
              id=wxID_MAINFRAMEBUTTONFLASHSINGLE)

        self.windowHostInterface = wx.Panel(id=wxID_MAINFRAMEWINDOWHOSTINTERFACE,
              name='windowHostInterface', parent=self.notebook, pos=wx.Point(0,
              0), size=wx.Size(620, 341), style=0)

        self.checkBoxAutoDetect = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXAUTODETECT,
              label='Use COM port automatic selection.',
              name='checkBoxAutoDetect', parent=self.windowHostInterface,
              style=0)
        self.checkBoxAutoDetect.SetValue(True)
        self.checkBoxAutoDetect.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxAutoDetectCheckbox,
              id=wxID_MAINFRAMECHECKBOXAUTODETECT)

        self.staticBoxConnection = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXCONNECTION,
              label='Connection', name='staticBoxConnection',
              parent=self.windowHostInterface, style=0)
        self.staticBoxConnection.SetHelpText('')

        self.staticTextSelectPort = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTSELECTPORT,
              label='Select COM port to use:', name='staticTextSelectPort',
              parent=self.windowHostInterface, style=0)

        self.buttonFlashRelease = wx.Button(id=wxID_MAINFRAMEBUTTONFLASHRELEASE,
              label='Flash', name='buttonFlashRelease',
              parent=self.windowFirmware, style=0)
        self.buttonFlashRelease.Bind(wx.EVT_BUTTON,
              self.OnButtonFlashReleaseButton,
              id=wxID_MAINFRAMEBUTTONFLASHRELEASE)

        self.checkBoxALL = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXALL,
              label='All Files', name='checkBoxALL', parent=self.windowFirmware,
              pos=wx.Point(5, 78), size=wx.Size(70, 13), style=0)
        self.checkBoxALL.SetValue(True)
        self.checkBoxALL.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxALLCheckbox,
              id=wxID_MAINFRAMECHECKBOXALL)

        self.staticTextList = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTLIST,
              label='Files to download: ', name='staticTextList',
              parent=self.windowFirmware, pos=wx.Point(5, 57), size=wx.Size(131,
              13), style=0)

        self.staticBoxCrashInfo = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXCRASHINFO,
              label='Crash Information', name='staticBoxCrashInfo',
              parent=self.windowDebug, style=0)

        self.staticBoxPlatInfo = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXPLATINFO,
              label='Platform Information', name='staticBoxPlatInfo',
              parent=self.windowDebug, style=0)

        self.checkBoxBT2 = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXBT2,
              label='Secondary Boot', name='checkBoxBT2',
              parent=self.windowFirmware, style=0)
        self.checkBoxBT2.SetValue(True)

        self.checkBoxLDR = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXLDR,
              label='Loader', name='checkBoxLDR', parent=self.windowFirmware,
              style=0)
        self.checkBoxLDR.SetValue(True)

        self.checkBoxMDM = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXMDM,
              label='Modem', name='checkBoxMDM', parent=self.windowFirmware,
              style=0)
        self.checkBoxMDM.SetValue(True)

        self.checkBoxDEVICECFG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXDEVICECFG,
              label='Device Config', name='checkBoxDEVICECFG',
              parent=self.windowFirmware, style=0)
        self.checkBoxDEVICECFG.SetValue(True)

        self.checkBoxPRODUCTCFG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXPRODUCTCFG,
              label='Product Config', name='checkBoxPRODUCTCFG',
              parent=self.windowFirmware, style=0)
        self.checkBoxPRODUCTCFG.SetValue(True)

        self.staticBoxATCommand = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXATCOMMAND,
              label='Enter AT command: ', name='staticBoxATCommand',
              parent=self.windowDebug, style=0)

        self.comboBoxAtCommands = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXATCOMMANDS, name='comboBoxAtCommands',
              parent=self.windowDebug, pos=wx.Point(5, 298), size=wx.Size(610,
              24), style=wx.TE_PROCESS_ENTER, value='')
        self.comboBoxAtCommands.SetLabel('')
        self.comboBoxAtCommands.SetToolTipString('')
        self.comboBoxAtCommands.Bind(wx.EVT_TEXT_ENTER,
              self.OnComboBoxAtCommandsTextEnter,
              id=wxID_MAINFRAMECOMBOBOXATCOMMANDS)

        self.checkBoxFlowControl = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFLOWCONTROL,
              label='Disable Flow Control.', name='checkBoxFlowControl',
              parent=self.windowHostInterface, style=0)
        self.checkBoxFlowControl.SetValue(False)
        self.checkBoxFlowControl.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxFlowControlCheckbox,
              id=wxID_MAINFRAMECHECKBOXFLOWCONTROL)

        self.staticBoxHostInterface = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXHOSTINTERFACE,
              label='Host Interface Switching', name='staticBoxHostInterface',
              parent=self.windowHostInterface, pos=wx.Point(0, 149),
              size=wx.Size(620, 54), style=0)

        self.staticTextHostInterface = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTHOSTINTERFACE,
              label='Switch Hardware Host Interface: ',
              name='staticTextHostInterface', parent=self.windowHostInterface,
              pos=wx.Point(5, 170), size=wx.Size(161, 13), style=0)

        self.radioButtonUsbHif = wx.RadioButton(id=wxID_MAINFRAMERADIOBUTTONUSBHIF,
              label='USB', name='radioButtonUsbHif',
              parent=self.windowHostInterface, style=0)
        self.radioButtonUsbHif.SetValue(False)
        self.radioButtonUsbHif.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButtonUsbHifRadiobutton,
              id=wxID_MAINFRAMERADIOBUTTONUSBHIF)

        self.radioButtonUartHif = wx.RadioButton(id=wxID_MAINFRAMERADIOBUTTONUARTHIF,
              label='UART', name='radioButtonUartHif',
              parent=self.windowHostInterface, style=0)
        self.radioButtonUartHif.SetValue(False)
        self.radioButtonUartHif.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButtonUartHifRadiobutton,
              id=wxID_MAINFRAMERADIOBUTTONUARTHIF)

        self.buttonApplyHifSwitch = wx.Button(id=wxID_MAINFRAMEBUTTONAPPLYHIFSWITCH,
              label='Apply', name='buttonApplyHifSwitch',
              parent=self.windowHostInterface, style=0)
        self.buttonApplyHifSwitch.Bind(wx.EVT_BUTTON,
              self.OnButtonApplyHifSwitchButton,
              id=wxID_MAINFRAMEBUTTONAPPLYHIFSWITCH)

        self.staticBoxImei = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXIMEI,
              label=u'IMEI Value', name='staticBoxImei',
              parent=self.windowConfigFiles, pos=wx.Point(0, 152),
              size=wx.Size(295, 121), style=0)

        self.textCtrlEnterImei = wx.TextCtrl(id=wxID_MAINFRAMETEXTCTRLENTERIMEI,
              name='textCtrlEnterImei', parent=self.windowConfigFiles,
              pos=wx.Point(5, 173), size=wx.Size(150, 21),
              style=wx.TE_PROCESS_ENTER, value='')
        self.textCtrlEnterImei.SetMaxLength(14)
        self.textCtrlEnterImei.Bind(wx.EVT_TEXT_ENTER,
              self.OnTextCtrlEnterImeiTextEnter,
              id=wxID_MAINFRAMETEXTCTRLENTERIMEI)

        self.buttonFlashImei = wx.Button(id=wxID_MAINFRAMEBUTTONFLASHIMEI,
              label='Flash', name='buttonFlashImei',
              parent=self.windowConfigFiles, pos=wx.Point(163, 173),
              size=wx.Size(75, 23), style=0)
        self.buttonFlashImei.Bind(wx.EVT_BUTTON, self.OnButtonFlashImeiButton,
              id=wxID_MAINFRAMEBUTTONFLASHIMEI)

        self.staticTextIMEINote = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTIMEINOTE,
              label='NOTE:\nThe IMEI value must be a 14 digits value.\nThe 15th digit is computed automatically as a\nstandard Luhn checksum of the 1st 14digits.',
              name='staticTextIMEINote', parent=self.windowConfigFiles,
              style=0)

        self.buttonBrowseReleaseArchive = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSERELEASEARCHIVE,
              label='Browse Archive', name='buttonBrowseReleaseArchive',
              parent=self.windowFirmware, style=0)
        self.buttonBrowseReleaseArchive.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseReleaseArchiveButton,
              id=wxID_MAINFRAMEBUTTONBROWSERELEASEARCHIVE)

        self.comboBoxComPort = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXCOMPORT, name='comboBoxComPort',
              parent=self.windowHostInterface, style=0, value='')
        self.comboBoxComPort.SetMinSize(wx.Size(200, 25))
        self.comboBoxComPort.SetLabel('')
        self.comboBoxComPort.Bind(wx.EVT_COMBOBOX,
              self.OnComboBoxComPortCombobox, id=wxID_MAINFRAMECOMBOBOXCOMPORT)
        self.comboBoxComPort.Bind(wx.EVT_TEXT, self.OnComboBoxComPortText,
              id=wxID_MAINFRAMECOMBOBOXCOMPORT)

        self.windowBoardrepair = wx.Panel(id=wxID_MAINFRAMEWINDOWBOARDREPAIR,
              name='windowBoardrepair', parent=self.notebook, pos=wx.Point(0,
              0), size=wx.Size(620, 341), style=wx.TAB_TRAVERSAL)

        self.staticBoxFactUartServer = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXFACTUARTSERVER,
              label='UART Server', name='staticBoxFactUartServer',
              parent=self.windowBoardrepair, pos=wx.Point(0, 208),
              size=wx.Size(620, 50), style=0)

        self.staticBoxFactStatus = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXFACTSTATUS,
              label='Status', name='staticBoxFactStatus',
              parent=self.windowBoardrepair, pos=wx.Point(0, 258),
              size=wx.Size(620, 90), style=0)

        self.staticTextFactUartServer = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTFACTUARTSERVER,
              label='Select UART COM port to use:',
              name='staticTextFactUartServer', parent=self.windowBoardrepair,
              pos=wx.Point(5, 229), size=wx.Size(408, 21), style=0)

        self.comboBoxFactUartServer = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXFACTUARTSERVER,
              name='comboBoxFactUartServer', parent=self.windowBoardrepair,
              pos=wx.Point(421, 229), size=wx.Size(130, 24), style=0, value='')
        self.comboBoxFactUartServer.SetLabel('')
        self.comboBoxFactUartServer.Bind(wx.EVT_TEXT,
              self.OnComboBoxFactUartServerText,
              id=wxID_MAINFRAMECOMBOBOXFACTUARTSERVER)
        self.comboBoxFactUartServer.Bind(wx.EVT_COMBOBOX,
              self.OnComboBoxFactUartServerCombobox,
              id=wxID_MAINFRAMECOMBOBOXFACTUARTSERVER)

        self.gaugeFactStatus = wx.Gauge(id=wxID_MAINFRAMEGAUGEFACTSTATUS,
              name='gaugeFactStatus', parent=self.windowBoardrepair,
              pos=wx.Point(5, 279), range=100, size=wx.Size(610, 28),
              style=wx.GA_HORIZONTAL)

        self.buttonStartBoardRepair = wx.Button(id=wxID_MAINFRAMEBUTTONSTARTBOARDREPAIR,
              label='Start', name='buttonStartBoardRepair',
              parent=self.windowBoardrepair, pos=wx.Point(5, 315),
              size=wx.Size(301, 28), style=0)
        self.buttonStartBoardRepair.Bind(wx.EVT_BUTTON,
              self.OnButtonBoardRepairStartButton,
              id=wxID_MAINFRAMEBUTTONSTARTBOARDREPAIR)

        self.buttonStopBoardRepair = wx.Button(id=wxID_MAINFRAMEBUTTONSTOPBOARDREPAIR,
              label='Stop', name='buttonStopBoardRepair',
              parent=self.windowBoardrepair, style=0)
        self.buttonStopBoardRepair.Bind(wx.EVT_BUTTON,
              self.OnButtonBoardRepairStopButton,
              id=wxID_MAINFRAMEBUTTONSTOPBOARDREPAIR)

        self.staticBoxCalibrationFiles = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXCALIBRATIONFILES,
              label='Calibration files', name='staticBoxCalibrationFiles',
              parent=self.windowConfigFiles, pos=wx.Point(0, 94),
              size=wx.Size(590, 50), style=0)

        self.comboBoxCalibrationFiles = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXCALIBRATIONFILES,
              name='comboBoxCalibrationFiles', parent=self.windowConfigFiles,
              pos=wx.Point(5, 115), size=wx.Size(414, 24), style=0, value='')
        self.comboBoxCalibrationFiles.SetLabel('')

        self.buttonBrowseCalibrationFiles = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSECALIBRATIONFILES,
              label='Browse...', name='buttonBrowseCalibrationFiles',
              parent=self.windowConfigFiles, pos=wx.Point(427, 115),
              size=wx.Size(75, 23), style=0)
        self.buttonBrowseCalibrationFiles.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseCalibrationFilesButton,
              id=wxID_MAINFRAMEBUTTONBROWSECALIBRATIONFILES)

        self.buttonFlashCalibrationFiles = wx.Button(id=wxID_MAINFRAMEBUTTONFLASHCALIBRATIONFILES,
              label='Flash', name='buttonFlashCalibrationFiles',
              parent=self.windowConfigFiles, pos=wx.Point(510, 115),
              size=wx.Size(75, 23), style=0)
        self.buttonFlashCalibrationFiles.Bind(wx.EVT_BUTTON,
              self.OnButtonFlashCalibrationFilesButton,
              id=wxID_MAINFRAMEBUTTONFLASHCALIBRATIONFILES)

        self.comboBoxFirmwareInfo = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXFIRMWAREINFO,
              name='comboBoxFirmwareInfo', parent=self.windowDebug,
              pos=wx.Point(5, 213), size=wx.Size(424, 24), style=0, value='')
        self.comboBoxFirmwareInfo.SetLabel('')

        self.buttonBrowseFirmwareInfo = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSEFIRMWAREINFO,
              label='Browse...', name='buttonBrowseFirmwareInfo',
              parent=self.windowDebug, pos=wx.Point(437, 213), size=wx.Size(75,
              28), style=0)
        self.buttonBrowseFirmwareInfo.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseFirmwareInfoButton,
              id=wxID_MAINFRAMEBUTTONBROWSEFIRMWAREINFO)

        self.staticBoxFirmwareInfo = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXFIRMWAREINFO,
              label='File(s) Information', name='staticBoxFirmwareInfo',
              parent=self.windowDebug, pos=wx.Point(0, 192), size=wx.Size(620,
              77), style=0)

        self.buttonGetFirmwareInfo = wx.Button(id=wxID_MAINFRAMEBUTTONGETFIRMWAREINFO,
              label='Get Information', name='buttonGetFirmwareInfo',
              parent=self.windowDebug, pos=wx.Point(5, 241), size=wx.Size(610,
              23), style=0)
        self.buttonGetFirmwareInfo.Bind(wx.EVT_BUTTON,
              self.OnButtonGetFirmwareInfoButton,
              id=wxID_MAINFRAMEBUTTONGETFIRMWAREINFO)

        self.buttonBrowseDirFirmwareInfo = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSEDIRFIRMWAREINFO,
              label='Browse Dir...', name='buttonBrowseDirFirmwareInfo',
              parent=self.windowDebug, style=0)
        self.buttonBrowseDirFirmwareInfo.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseDirFirmwareInfoButton,
              id=wxID_MAINFRAMEBUTTONBROWSEDIRFIRMWAREINFO)

        self.staticBoxUartDiscoveryServer = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXUARTDISCOVERYSERVER,
              label='UART discovery server',
              name='staticBoxUartDiscoveryServer',
              parent=self.windowHostInterface, style=0)

        self.staticTextUartDiscoverySelectPort = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTUARTDISCOVERYSELECTPORT,
              label='Select COM port to use: ',
              name='staticTextUartDiscoverySelectPort',
              parent=self.windowHostInterface, style=0)

        self.comboBoxUartDiscoverySelectPort = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXUARTDISCOVERYSELECTPORT,
              name='comboBoxUartDiscoverySelectPort',
              parent=self.windowHostInterface, style=0, value='')
        self.comboBoxUartDiscoverySelectPort.SetLabel('')
        self.comboBoxUartDiscoverySelectPort.Bind(wx.EVT_COMBOBOX,
              self.OnComboBoxUartDiscoverySelectPortCombobox,
              id=wxID_MAINFRAMECOMBOBOXUARTDISCOVERYSELECTPORT)
        self.comboBoxUartDiscoverySelectPort.Bind(wx.EVT_TEXT,
              self.OnComboBoxUartDiscoverySelectPortText,
              id=wxID_MAINFRAMECOMBOBOXUARTDISCOVERYSELECTPORT)

        self.buttonUartDiscoveryStartServer = wx.Button(id=wxID_MAINFRAMEBUTTONUARTDISCOVERYSTARTSERVER,
              label='Start Server...', name='buttonUartDiscoveryStartServer',
              parent=self.windowHostInterface, style=0)
        self.buttonUartDiscoveryStartServer.Bind(wx.EVT_BUTTON,
              self.OnButtonUartDiscoveryStartServerButton,
              id=wxID_MAINFRAMEBUTTONUARTDISCOVERYSTARTSERVER)

        self.buttonUartDiscoveryStopServer = wx.Button(id=wxID_MAINFRAMEBUTTONUARTDISCOVERYSTOPSERVER,
              label='Stop', name='buttonUartDiscoveryStopServer',
              parent=self.windowHostInterface, style=0)
        self.buttonUartDiscoveryStopServer.Bind(wx.EVT_BUTTON,
              self.OnButtonUartDiscoveryStopServerButton,
              id=wxID_MAINFRAMEBUTTONUARTDISCOVERYSTOPSERVER)

        self.notebookBoardRepair = wx.Notebook(id=wxID_MAINFRAMENOTEBOOKBOARDREPAIR,
              name='notebookBoardRepair', parent=self.windowBoardrepair,
              pos=wx.Point(0, 0), size=wx.Size(620, 208), style=wx.NB_LEFT)
        self.notebookBoardRepair.SetToolTipString('')

        self.windowFactoryBoardRepair = wx.Panel(id=wxID_MAINFRAMEWINDOWFACTORYBOARDREPAIR,
              name='windowFactoryBoardRepair', parent=self.notebookBoardRepair,
              pos=wx.Point(0, 0), size=wx.Size(590, 200), style=0)

        self.windowDebugBoardRepair = wx.Panel(id=wxID_MAINFRAMEWINDOWDEBUGBOARDREPAIR,
              name='windowDebugBoardRepair', parent=self.notebookBoardRepair,
              pos=wx.Point(0, 0), size=wx.Size(590, 200), style=0)

        self.staticBoxFactReleaseUpdate = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXFACTRELEASEUPDATE,
              label='Repair Package', name='staticBoxFactReleaseUpdate',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(0, 0),
              size=wx.Size(590, 159), style=0)

        self.checkBoxFactReleaseListAll = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTRELEASELISTALL,
              label='All Files', name='checkBoxFactReleaseListAll',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(5, 78),
              size=wx.Size(54, 13), style=0)
        self.checkBoxFactReleaseListAll.SetValue(True)
        self.checkBoxFactReleaseListAll.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxFactReleaseListAllCheckbox,
              id=wxID_MAINFRAMECHECKBOXFACTRELEASELISTALL)

        self.checkBoxFactReleaseUpdateListBT2 = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTBT2,
              label='Secondary Boot', name='checkBoxFactReleaseUpdateListBT2',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(67, 78),
              size=wx.Size(95, 13), style=0)
        self.checkBoxFactReleaseUpdateListBT2.SetValue(True)
        self.checkBoxFactReleaseUpdateListBT2.Enable(False)

        self.checkBoxFactUpdateReleaseListLDR = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTLDR,
              label='Loader', name='checkBoxFactUpdateReleaseListLDR',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(67, 91),
              size=wx.Size(52, 13), style=0)
        self.checkBoxFactUpdateReleaseListLDR.SetValue(True)
        self.checkBoxFactUpdateReleaseListLDR.Enable(False)

        self.checkBoxFactReleaseUpdateListMDM = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTMDM,
              label='Modem', name='checkBoxFactReleaseUpdateListMDM',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(170, 78),
              size=wx.Size(53, 13), style=0)
        self.checkBoxFactReleaseUpdateListMDM.SetValue(True)

        self.checkBoxFactUpdateReleaseListPLATCG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTPLATCG,
              label='Platform Config',
              name='checkBoxFactUpdateReleaseListPLATCG',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(231, 78),
              size=wx.Size(93, 13), style=0)
        self.checkBoxFactUpdateReleaseListPLATCG.SetValue(True)
        self.checkBoxFactUpdateReleaseListPLATCG.Enable(False)

        self.checkBoxFactUpdateReleaseListCALIB = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTUPDATERELEASELISTCALIB,
              label='Calibration', name='checkBoxFactUpdateReleaseListCALIB',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(231, 91),
              size=wx.Size(70, 13), style=0)
        self.checkBoxFactUpdateReleaseListCALIB.SetValue(True)

        self.staticTextFactReleaseList = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTFACTRELEASELIST,
              label='Select files to consider for release update:',
              name='staticTextFactReleaseList',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(5, 57),
              size=wx.Size(203, 13), style=0)

        self.buttonFactBrowseArchive = wx.Button(id=wxID_MAINFRAMEBUTTONFACTBROWSEARCHIVE,
              label='Browse Archive', name='buttonFactBrowseArchive',
              parent=self.windowFactoryBoardRepair, style=0)
        self.buttonFactBrowseArchive.Bind(wx.EVT_BUTTON,
              self.OnButtonFactBrowseArchiveButton,
              id=wxID_MAINFRAMEBUTTONFACTBROWSEARCHIVE)

        self.buttonFactReleaseUpdate = wx.Button(id=wxID_MAINFRAMEBUTTONFACTRELEASEUPDATE,
              label='Browse', name='buttonFactReleaseUpdate',
              parent=self.windowFactoryBoardRepair, style=0)
        self.buttonFactReleaseUpdate.Bind(wx.EVT_BUTTON,
              self.OnButtonFactReleaseUpdateButton,
              id=wxID_MAINFRAMEBUTTONFACTRELEASEUPDATE)

        self.comboBoxFactReleaseUpdate = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXFACTRELEASEUPDATE,
              name='comboBoxFactReleaseUpdate',
              parent=self.windowFactoryBoardRepair, style=0, value='')
        self.comboBoxFactReleaseUpdate.SetLabel('')

        self.staticTextSelectBT2 = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTSELECTBT2,
              label='Select BT2: ', name='staticTextSelectBT2',
              parent=self.windowDebugBoardRepair, style=0)

        self.staticTextSelectAppli = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTSELECTAPPLI,
              label='Select Application: ', name='staticTextSelectAppli',
              parent=self.windowDebugBoardRepair, style=0)

        self.buttonBrowseAppli = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSEAPPLI,
              label='Browse...', name='buttonBrowseAppli',
              parent=self.windowDebugBoardRepair, style=0)
        self.buttonBrowseAppli.Bind(wx.EVT_BUTTON,
              self.OnButtonDbgBrowseUartAppliButton,
              id=wxID_MAINFRAMEBUTTONBROWSEAPPLI)

        self.buttonBrowseBT2 = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSEBT2,
              label='Browse...', name='buttonBrowseBT2',
              parent=self.windowDebugBoardRepair, style=0)
        self.buttonBrowseBT2.Bind(wx.EVT_BUTTON,
              self.OnButtonDbgBrowseUartBT2Button,
              id=wxID_MAINFRAMEBUTTONBROWSEBT2)

        self.comboBoxUartBT2 = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXUARTBT2, name='comboBoxUartBT2',
              parent=self.windowDebugBoardRepair, style=0, value='')
        self.comboBoxUartBT2.SetLabel('')

        self.comboBoxUartAppli = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXUARTAPPLI, name='comboBoxUartAppli',
              parent=self.windowDebugBoardRepair, style=0, value='')
        self.comboBoxUartAppli.SetLabel('')

        self.staticBoxUartArchiveSelection = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXUARTARCHIVESELECTION,
              label='Archive Selection', name='staticBoxUartArchiveSelection',
              parent=self.windowDebugBoardRepair, style=0)

        self.staticBoxXmlSources = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXXMLSOURCES,
              label='XML sources', name='staticBoxXmlSources',
              parent=self.windowConfigFiles, style=0)

        self.staticTextXmlSourceSelesct = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTXMLSOURCESELESCT,
              label='Select file type: ', name='staticTextXmlSourceSelesct',
              parent=self.windowConfigFiles, style=0)

        self.choiceXmlSourceType = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEXMLSOURCETYPE, name='choiceXmlSourceType',
              parent=self.windowConfigFiles, style=0)
        self.choiceXmlSourceType.Bind(wx.EVT_CHOICE,
              self.OnChoiceXmlSourceTypeChoice,
              id=wxID_MAINFRAMECHOICEXMLSOURCETYPE)

        self.comboBoxXmlSourcePath = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXXMLSOURCEPATH,
              name='comboBoxXmlSourcePath', parent=self.windowConfigFiles,
              style=0, value='')
        self.comboBoxXmlSourcePath.SetLabel('')

        self.buttonBrowseXmlSource = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSEXMLSOURCE,
              label='Browse...', name='buttonBrowseXmlSource',
              parent=self.windowConfigFiles, style=0)
        self.buttonBrowseXmlSource.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseXmlSourceButton,
              id=wxID_MAINFRAMEBUTTONBROWSEXMLSOURCE)

        self.buttonProgramXmlSource = wx.Button(id=wxID_MAINFRAMEBUTTONPROGRAMXMLSOURCE,
              label='Flash', name='buttonProgramXmlSource',
              parent=self.windowConfigFiles, style=0)
        self.buttonProgramXmlSource.Bind(wx.EVT_BUTTON,
              self.OnButtonProgramXmlSourceButton,
              id=wxID_MAINFRAMEBUTTONPROGRAMXMLSOURCE)

        self.staticTextCrashInfo = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTCRASHINFO,
              label='Select action: ', name='staticTextCrashInfo',
              parent=self.windowDebug, style=0)

        self.choiceCrashInfo = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICECRASHINFO, name='choiceCrashInfo',
              parent=self.windowDebug, style=0)
        self.choiceCrashInfo.Bind(wx.EVT_CHOICE, self.OnChoiceCrashInfoChoice,
              id=wxID_MAINFRAMECHOICECRASHINFO)

        self.buttonCrashInfo = wx.Button(id=wxID_MAINFRAMEBUTTONCRASHINFO,
              label='Start', name='buttonCrashInfo', parent=self.windowDebug,
              pos=wx.Point(238, 21), size=wx.Size(75, 24), style=0)
        self.buttonCrashInfo.Bind(wx.EVT_BUTTON, self.OnButtonCrashInfoButton,
              id=wxID_MAINFRAMEBUTTONCRASHINFO)

        self.checkBoxCrashInfo = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXCRASHINFO,
              label='No decoding', name='checkBoxCrashInfo',
              parent=self.windowDebug, style=0)
        self.checkBoxCrashInfo.SetValue(False)
        self.checkBoxCrashInfo.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxCrashInfoCheckbox,
              id=wxID_MAINFRAMECHECKBOXCRASHINFO)

        self.comboBoxCrashInfoLogPath = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXCRASHINFOLOGPATH,
              name='comboBoxCrashInfoLogPath', parent=self.windowDebug, style=0,
              value='')
        self.comboBoxCrashInfoLogPath.SetLabel('')

        self.buttonCrashInfoBrowse = wx.Button(id=wxID_MAINFRAMEBUTTONCRASHINFOBROWSE,
              label='Browse...', name='buttonCrashInfoBrowse',
              parent=self.windowDebug, style=0)
        self.buttonCrashInfoBrowse.Bind(wx.EVT_BUTTON,
              self.OnButtonCrashInfoBrowseButton,
              id=wxID_MAINFRAMEBUTTONCRASHINFOBROWSE)

        self.staticTextFlashFormat = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTFLASHFORMAT,
              label='Full Flash Format: ', name='staticTextFlashFormat',
              parent=self.windowFactoryBoardRepair, style=0)

        self.checkBoxFlashFormat = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFLASHFORMAT,
              label='', name='checkBoxFlashFormat',
              parent=self.windowFactoryBoardRepair, style=0)
        self.checkBoxFlashFormat.SetValue(False)
        self.checkBoxFlashFormat.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxFlashFormatCheckbox,
              id=wxID_MAINFRAMECHECKBOXFLASHFORMAT)

        self.staticBoxFactBoardRepairSettings = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXFACTBOARDREPAIRSETTINGS,
              label='Settings', name='staticBoxFactBoardRepairSettings',
              parent=self.windowFactoryBoardRepair, style=0)

        self.staticTextPlatInfo = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTPLATINFO,
              label='Select action: ', name='staticTextPlatInfo',
              parent=self.windowDebug, style=0)

        self.choicePlatInfo = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEPLATINFO, name='choicePlatInfo',
              parent=self.windowDebug, style=0)
        self.choicePlatInfo.Bind(wx.EVT_CHOICE, self.OnChoicePlatInfoChoice,
              id=wxID_MAINFRAMECHOICEPLATINFO)

        self.buttonStartPlatInfo = wx.Button(id=wxID_MAINFRAMEBUTTONSTARTPLATINFO,
              label='Start', name='buttonStartPlatInfo',
              parent=self.windowDebug, style=0)
        self.buttonStartPlatInfo.Bind(wx.EVT_BUTTON,
              self.OnButtonStartPlatInfoButton,
              id=wxID_MAINFRAMEBUTTONSTARTPLATINFO)

        self.staticTextLogFile = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTLOGFILE,
              label='Select log file: ', name='staticTextLogFile',
              parent=self.windowDebug, style=0)

        self.staticTextLogFolder = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTLOGFOLDER,
              label='Select log folder: ', name='staticTextLogFolder',
              parent=self.windowDebug, style=0)

        self.comboBoxLogFolder = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXLOGFOLDER, name='comboBoxLogFolder',
              parent=self.windowDebug, style=0, value='')
        self.comboBoxLogFolder.SetLabel('')

        self.buttonBrowseLogFolder = wx.Button(id=wxID_MAINFRAMEBUTTONBROWSELOGFOLDER,
              label='Browse...', name='buttonBrowseLogFolder',
              parent=self.windowDebug, style=0)
        self.buttonBrowseLogFolder.Bind(wx.EVT_BUTTON,
              self.OnButtonBrowseLogFolderButton,
              id=wxID_MAINFRAMEBUTTONBROWSELOGFOLDER)

        self.checkBoxFactReleaseUpdateListDEVICECFG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTDEVICECFG,
              label='Device Config',
              name='checkBoxFactReleaseUpdateListDEVICECFG',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(332, 78),
              size=wx.Size(85, 13), style=0)
        self.checkBoxFactReleaseUpdateListDEVICECFG.SetValue(True)

        self.checkBoxFactReleaseUpdateListPRODUCTCFG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXFACTRELEASEUPDATELISTPRODUCTCFG,
              label='Product Config',
              name='checkBoxFactReleaseUpdateListPRODUCTCFG',
              parent=self.windowFactoryBoardRepair, pos=wx.Point(332, 91),
              size=wx.Size(90, 13), style=0)
        self.checkBoxFactReleaseUpdateListPRODUCTCFG.SetValue(True)

        self.staticBoxHifSettings = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXHIFSETTINGS,
              label='Settings', name='staticBoxHifSettings',
              parent=self.windowHostInterface, pos=wx.Point(0, 75),
              size=wx.Size(620, 74), style=0)

        self.staticTextHifBaudrate = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTHIFBAUDRATE,
              label='Select COM baudrate : ', name='staticTextHifBaudrate',
              parent=self.windowHostInterface, pos=wx.Point(5, 120),
              size=wx.Size(112, 13), style=0)

        self.choiceHifBaudrate = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEHIFBAUDRATE, name='choiceHifBaudrate',
              parent=self.windowHostInterface, pos=wx.Point(125, 120),
              size=wx.Size(130, 24), style=0)
        self.choiceHifBaudrate.SetSelection(-1)
        self.choiceHifBaudrate.Bind(wx.EVT_CHOICE,
              self.OnChoiceHifBaudrateChoice,
              id=wxID_MAINFRAMECHOICEHIFBAUDRATE)

        self.staticBoxUartBootAgentSettings = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXUARTBOOTAGENTSETTINGS,
              label='Settings', name='staticBoxUartBootAgentSettings',
              parent=self.windowDebugBoardRepair, pos=wx.Point(0, 138),
              size=wx.Size(590, 59), style=0)

        self.staticTextBromComBaudrate = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTBROMCOMBAUDRATE,
              label='BROM COM baudrate: ', name='staticTextBromComBaudrate',
              parent=self.windowDebugBoardRepair, pos=wx.Point(5, 159),
              size=wx.Size(153, 33), style=0)

        self.staticTextAppComBaudrate = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTAPPCOMBAUDRATE,
              label='Appli COM baudrate: ', name='staticTextAppComBaudrate',
              parent=self.windowDebugBoardRepair, pos=wx.Point(296, 159),
              size=wx.Size(154, 33), style=0)

        self.choiceBromComBaudrate = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEBROMCOMBAUDRATE,
              name='choiceBromComBaudrate', parent=self.windowDebugBoardRepair,
              pos=wx.Point(158, 159), size=wx.Size(130, 24), style=0)
        self.choiceBromComBaudrate.Bind(wx.EVT_CHOICE,
              self.OnChoiceBromComBaudrateChoice,
              id=wxID_MAINFRAMECHOICEBROMCOMBAUDRATE)

        self.choiceAppComBaudrate = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEAPPCOMBAUDRATE,
              name='choiceAppComBaudrate', parent=self.windowDebugBoardRepair,
              style=0)
        self.choiceAppComBaudrate.Bind(wx.EVT_CHOICE,
              self.OnChoiceAppComBaudrateChoice,
              id=wxID_MAINFRAMECHOICEAPPCOMBAUDRATE)

        self.staticTextCOMBlockSize = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTCOMBLOCKSIZE,
              label='Select block size (in bytes): ',
              name='staticTextCOMBlockSize', parent=self.windowHostInterface,
              style=0)

        self.comboBoxCOMBlockSize = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXCOMBLOCKSIZE,
              name='comboBoxCOMBlockSize', parent=self.windowHostInterface,
              style=0, value='')
        self.comboBoxCOMBlockSize.SetLabel('')
        self.comboBoxCOMBlockSize.Bind(wx.EVT_COMBOBOX,
              self.OnComboBoxCOMBlockSizeCombobox,
              id=wxID_MAINFRAMECOMBOBOXCOMBLOCKSIZE)
        self.comboBoxCOMBlockSize.Bind(wx.EVT_TEXT,
              self.OnComboBoxCOMBlockSizeText,
              id=wxID_MAINFRAMECOMBOBOXCOMBLOCKSIZE)

        self.checkBoxAUDIOCFG = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXAUDIOCFG,
              label='Audio Config', name='checkBoxAUDIOCFG',
              parent=self.windowFirmware, style=0)
        self.checkBoxAUDIOCFG.SetValue(True)

        self.windowAdbApInterface = wx.Panel(id=wxID_MAINFRAMEWINDOWADBAPINTERFACE,
              name='windowAdbApInterface', parent=self.notebook,
              style=wx.TAB_TRAVERSAL)

        self.staticBoxAdbApIfConnection = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXADBAPIFCONNECTION,
              label='Connection', name='staticBoxAdbApIfConnection',
              parent=self.windowAdbApInterface, style=0)

        self.staticBoxAdbApIfForward = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXADBAPIFFORWARD,
              label='Forward', name='staticBoxAdbApIfForward',
              parent=self.windowAdbApInterface, style=0)

        self.staticBoxAdbApIfSystemProperties = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXADBAPIFSYSTEMPROPERTIES,
              label='System Properties',
              name='staticBoxAdbApIfSystemProperties',
              parent=self.windowAdbApInterface, style=0)

        self.comboBoxAdbApIfDevices = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXADBAPIFDEVICES,
              name='comboBoxAdbApIfDevices', parent=self.windowAdbApInterface,
              style=wx.CB_READONLY, value='')
        self.comboBoxAdbApIfDevices.SetLabel('')
        self.comboBoxAdbApIfDevices.Bind(wx.EVT_COMBOBOX,
              self.OnComboBoxAdbApIfDevicesCombobox,
              id=wxID_MAINFRAMECOMBOBOXADBAPIFDEVICES)

        self.staticTextAdbApIfDevices = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFDEVICES,
              label='Select device to use: ', name='staticTextAdbApIfDevices',
              parent=self.windowAdbApInterface, style=0)

        self.buttonAdbApIfScan = wx.Button(id=wxID_MAINFRAMEBUTTONADBAPIFSCAN,
              label='Scan...', name='buttonAdbApIfScan',
              parent=self.windowAdbApInterface, style=0)
        self.buttonAdbApIfScan.Bind(wx.EVT_BUTTON,
              self.OnButtonAdbApIfScanButton,
              id=wxID_MAINFRAMEBUTTONADBAPIFSCAN)

        self.staticTextAdbApIfForward = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFFORWARD,
              label='Forwarded port (i.e. /dev/ttyACM0...): ',
              name='staticTextAdbApIfForward', parent=self.windowAdbApInterface,
              style=0)

        self.comboBoxAdbApIfForward = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXADBAPIFFORWARD,
              name='comboBoxAdbApIfForward', parent=self.windowAdbApInterface,
              style=0, value='')
        self.comboBoxAdbApIfForward.SetLabel('')

        self.buttonAdbApIfForward = wx.Button(id=wxID_MAINFRAMEBUTTONADBAPIFFORWARD,
              label='Forward...', name='buttonAdbApIfForward',
              parent=self.windowAdbApInterface, style=0)
        self.buttonAdbApIfForward.Bind(wx.EVT_BUTTON,
              self.OnButtonAdbApIfForwardButton,
              id=wxID_MAINFRAMEBUTTONADBAPIFFORWARD)

        self.staticTextAdbApIfForwardSocket = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFFORWARDSOCKET,
              label='Forwarded socket (i.e tcp:12345): ',
              name='staticTextAdbApIfForwardSocket',
              parent=self.windowAdbApInterface, style=0)

        self.comboBoxAdbApIfForwardSocket = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXADBAPIFFORWARDSOCKET,
              name='comboBoxAdbApIfForwardSocket',
              parent=self.windowAdbApInterface, style=0, value='')
        self.comboBoxAdbApIfForwardSocket.SetLabel('')

        self.staticTextAdbApIfSystemProperties = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFSYSTEMPROPERTIES,
              label='Property: ', name='staticTextAdbApIfSystemProperties',
              parent=self.windowAdbApInterface, style=0)

        self.comboBoxAdbApIfSystemProperties = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXADBAPIFSYSTEMPROPERTIES,
              name='comboBoxAdbApIfSystemProperties',
              parent=self.windowAdbApInterface, style=0, value='')
        self.comboBoxAdbApIfSystemProperties.SetLabel('')

        self.buttonAdbApIfSystemPropertiesSet = wx.Button(id=wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESSET,
              label='Set...', name='buttonAdbApIfSystemPropertiesSet',
              parent=self.windowAdbApInterface, style=0)
        self.buttonAdbApIfSystemPropertiesSet.Bind(wx.EVT_BUTTON,
              self.OnButtonAdbApIfSystemPropertiesSetButton,
              id=wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESSET)

        self.buttonAdbApIfSystemPropertiesGet = wx.Button(id=wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESGET,
              label='Get...', name='buttonAdbApIfSystemPropertiesGet',
              parent=self.windowAdbApInterface, style=0)
        self.buttonAdbApIfSystemPropertiesGet.Bind(wx.EVT_BUTTON,
              self.OnButtonAdbApIfSystemPropertiesGetButton,
              id=wxID_MAINFRAMEBUTTONADBAPIFSYSTEMPROPERTIESGET)

        self.staticTextAdbApIfActionSelect = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFACTIONSELECT,
              label='Select action: ', name='staticTextAdbApIfActionSelect',
              parent=self.windowAdbApInterface, style=0)

        self.choiceAdbApIfActions = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICEADBAPIFACTIONS,
              name='choiceAdbApIfActions', parent=self.windowAdbApInterface,
              style=0)

        self.buttonAdbApIfActionsStart = wx.Button(id=wxID_MAINFRAMEBUTTONADBAPIFACTIONSSTART,
              label='Start...', name='buttonAdbApIfActionsStart',
              parent=self.windowAdbApInterface, style=0)
        self.buttonAdbApIfActionsStart.Bind(wx.EVT_BUTTON,
              self.OnButtonAdbApIfActionsStartButton,
              id=wxID_MAINFRAMEBUTTONADBAPIFACTIONSSTART)

        self.checkBoxAdbApIfConnection = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXADBAPIFCONNECTION,
              label='Use ADB device(s) automatic selection.',
              name='checkBoxAdbApIfConnection',
              parent=self.windowAdbApInterface, style=0)
        self.checkBoxAdbApIfConnection.SetValue(True)
        self.checkBoxAdbApIfConnection.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxAdbApIfConnectionCheckbox,
              id=wxID_MAINFRAMECHECKBOXADBAPIFCONNECTION)

        self.checkBoxBT3 = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXBT3,
              label='Tertiary Boot', name='checkBoxBT3',
              parent=self.windowFirmware, style=0)
        self.checkBoxBT3.SetValue(True)

        self.comboBoxAdbApIfSystemPropertiesValue = wx.ComboBox(choices=[],
              id=wxID_MAINFRAMECOMBOBOXADBAPIFSYSTEMPROPERTIESVALUE,
              name='comboBoxAdbApIfSystemPropertiesValue',
              parent=self.windowAdbApInterface, style=0, value='')
        self.comboBoxAdbApIfSystemPropertiesValue.SetLabel('')

        self.staticTextAdbApIfSystemPropertiesValue = wx.StaticText(id=wxID_MAINFRAMESTATICTEXTADBAPIFSYSTEMPROPERTIESVALUE,
              label='Value: ', name='staticTextAdbApIfSystemPropertiesValue',
              parent=self.windowAdbApInterface, style=0)

        self.staticBoxAdbApIfActions = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXADBAPIFACTIONS,
              label='Actions', name='staticBoxAdbApIfActions',
              parent=self.windowAdbApInterface, style=0)

        self.staticBoxUpdateOptions = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXUPDATEOPTIONS,
              label='Options', name='staticBoxUpdateOptions',
              parent=self.windowUpdate, style=0)

        self.checkBoxUpdateEnableCbc = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXUPDATEENABLECBC,
              label='Enable CBC', name='checkBoxUpdateEnableCbc',
              parent=self.windowUpdate, style=0)
        self.checkBoxUpdateEnableCbc.SetValue(True)
        self.checkBoxUpdateEnableCbc.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxUpdateEnableCbcCheckbox,
              id=wxID_MAINFRAMECHECKBOXUPDATEENABLECBC)

        self.checkBoxUpdateFilRestart = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXUPDATEFILRESTART,
              label='Restart FIL after update', name='checkBoxUpdateFilRestart',
              parent=self.windowUpdate, style=0)
        self.checkBoxUpdateFilRestart.SetValue(True)
        self.checkBoxUpdateFilRestart.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxUpdateFilRestartCheckbox,
              id=wxID_MAINFRAMECHECKBOXUPDATEFILRESTART)

        self.checkBoxUpdateEnableKrm = wx.CheckBox(id=wxID_MAINFRAMECHECKBOXUPDATEENABLEKRM,
              label='Check Keys', name='checkBoxUpdateEnableKrm',
              parent=self.windowUpdate, style=0)
        self.checkBoxUpdateEnableKrm.SetValue(True)
        self.checkBoxUpdateEnableKrm.Bind(wx.EVT_CHECKBOX,
              self.OnCheckBoxUpdateEnableKrmCheckbox,
              id=wxID_MAINFRAMECHECKBOXUPDATEENABLEKRM)

        self.staticBoxUnlock = wx.StaticBox(id=wxID_MAINFRAMESTATICBOXUNLOCK,
              label=u'Unlock board', name=u'staticBoxUnlock',
              parent=self.windowConfigFiles, pos=wx.Point(305, 152),
              size=wx.Size(285, 121), style=0)
        self.staticBoxUnlock.Show(False)

        self.buttonUnlock = wx.Button(id=wxID_MAINFRAMEBUTTONUNLOCK,
              label=u'Get module lock state\n', name=u'buttonUnlock',
              parent=self.windowConfigFiles, pos=wx.Point(310, 193),
              size=wx.Size(275, 55), style=0)
        self.buttonUnlock.Show(False)
        self.buttonUnlock.Enable(False)
        self.buttonUnlock.Bind(wx.EVT_BUTTON, self.OnButtonUnlockButton,
              id=wxID_MAINFRAMEBUTTONUNLOCK)

        self._init_coll_notebook_Pages(self.notebook)
        self._init_coll_notebookUpdate_Pages(self.notebookUpdate)
        self._init_coll_notebookBoardRepair_Pages(self.notebookBoardRepair)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.pcid_to_unlock = None
        self.initialised = False

        # Bind event on notebook board repair now to avoid callback to be called at init...
        self.settings = RistrettoCommon.GetSettings()

        # Bind event on notebook board repair now to avoid callback to be called at init...
        self.notebookBoardRepair.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
              self.OnNotebookBoardRepairNotebookPageChanged,
              id=wxID_MAINFRAMENOTEBOOKBOARDREPAIR)

        # Get tool config
        self.tool_config = RistrettoCommon.GetToolConfig()

        # Init log interface
        self.log = FrameLog(aWxStatusBar=self.statusBar1, processCb=self._logCb)
        self._devLog = DevLogFrame.DevLogWrapper(self)

        # To use thread & hif when connecting to the platform:
        self.currentAction = None
        self.ongoingThread = False # at init no thread is running...
        self.portList = []
        self.deviceList = []
        self.defaultSerialPort = '/dev/at_modem'
        self.defaultSerialSocket= 'tcp:12345'
        self.platform = RistrettoThreads.Platform(self.log, disCb=self._disableActions, updCb=self._updateConnectionStatus)
        self.conn = self.platform.conn
        match = re.match('(\d*)\.(\d*)(.*)', self.platform.LibVersion())
        if match:
            major, minor, build = match.groups()
            self.libversion = float('%s.%s' % (major, minor))
        else:
            self.libversion = 0.0
        self.AdbDevice=None   # unique device name used when auto-detect de-activated
        self.ComPort = None   # unique comport name used when auto-detect de-activated
        self.multiPlatform = False

        # Display start up tool info:
        RistrettoFrameShare.ToolInfo(self.tool_config, self.platform)

        # Apply ristretto configuration file if exists
        try:
            self._applyConfig()
        except Exception:
            PrintException()

        # Perform 1st scan
        self._disableActions()
        self.conn.Scan()
        self._updateConnectionStatus()

        # Some Frame variables inits:
        self.OriginalBtnColor = self.buttonPathBrowse.GetBackgroundColour()
        self._enableFileListButtons()
        self._disableComPortSelection()
        self._disableAdbDeviceSelection()
        self.selectedThroughComboBoxAtCommands = False
        self.eventComboAtCommands = False
        self.defaultDir = os.getcwd()
        self.updaterLibDir = os.path.realpath(os.path.dirname(IceraToolbox.LIBNAME))
        self.statusBar1.SetStatusWidths([0, -1, -1])
        self.informationSource = None
        self.consoleEditable = False
        self.addedItemsList = {}
        self._initKeysSettings()
        self._addMenuElem(self.UpdaterLibMenu, os.path.realpath(IceraToolbox.LIBNAME), self._onSelectedUpdaterLib)
        self._disableFactFileListButtons()

        # Default discovery server
        self.uartDiscoveryComPort = None

        # Board repair default values.
        self.dbgBoardRepairStarted = False
        self.factBoardRepairStarted = False
        self.uartBoardRepairComPort = None
        self.boardRepairFactory = False
        self.boardRepairDebug = True

        # Unzip & Untargz extract_folder
        self.extract_folder = TMP_EXTRACT_FOLDER

        # Init drag/drop events on combo box...
        FrameFileDragDrop(box=self.comboBoxPath)
        FrameFileDragDrop(box=self.comboBoxSingle)
        FrameFileDragDrop(box=self.comboBoxXmlSourcePath)
        FrameFileDragDrop(box=self.comboBoxCalibrationFiles)
        FrameFileDragDrop(box=self.comboBoxUartBT2)
        FrameFileDragDrop(box=self.comboBoxUartAppli)
        FrameFileDragDrop(box=self.comboBoxFirmwareInfo)
        FrameFileDragDrop(box=self.comboBoxFactReleaseUpdate)
        FrameFileDragDrop(box=self.comboBoxCrashInfoLogPath)
        
        
        # Settings serialization
        self._applySettings()
        # init some GUI items
        self._initXmlSourceChoiceBox()
        self._initCrashInfoData()
        self._initPlatInfoData()
        self._initBaudrateChoiceBoxes()
        self._initBlockSizeChoiceBoxes()
        self.textCtrlEnterImei.SetValidator(TextCtrlValidator(TxtCtrl=self.textCtrlEnterImei, pattern='^\d{0,14}$'))
        self._initInterfaceTab()

        if self.platform.conn.mode == RistrettoCommon.RISTRETTO_ADB and not self.platform.conn.IsSingleFlash():
            self._initPortForwarding()

        # Default annex frames
        self.UserGuideDlg  = None
        self.ArchInfoDlg   = None
        self.BuildDlg      = None

        # Init some infos at init
        try:
            self.stringToGetVal = ''
            self._initChipTypeMenu()
        except:
            PrintException()

        self.initialised = True

    #################################################
    #                                               #
    # Internal Frame functions                      #
    #  (i.e. not to be used outside the Frame class #
    #                                               #
    #################################################
    def _deInitPortForwarding(self):
        try:
            # Enable forward utility...
            self.buttonAdbApIfForward.Enable()
            # Re-enable port selection
            self.comboBoxAdbApIfForward.SetLabel("")
            self.comboBoxAdbApIfForward.SetValue("")
            self.comboBoxAdbApIfForward.Enable()
            # Re-enable socket selection
            self.comboBoxAdbApIfForwardSocket.SetLabel("")
            self.comboBoxAdbApIfForwardSocket.SetValue("")
            self.comboBoxAdbApIfForwardSocket.Enable()
        except Exception:
            PrintException()

    def _initPortForwarding(self):
        try:
            if len(self.platform.conn.devices) > 0:
                # Enable forward utility...
                #self.buttonAdbApIfForward.Disable()
                # Set self.defaultSerialPort and disable selection
                self.comboBoxAdbApIfForward.SetLabel(self.defaultSerialPort)
                self.comboBoxAdbApIfForward.SetValue(self.defaultSerialPort)
                #self.comboBoxAdbApIfForward.Disable()
                # Set self.defaultSerialSocket and disable selection
                self.comboBoxAdbApIfForwardSocket.SetLabel(self.defaultSerialSocket)
                self.comboBoxAdbApIfForwardSocket.SetValue(self.defaultSerialSocket)
                #self.comboBoxAdbApIfForwardSocket.Disable()
                # Always keep ADB actions enabled...
                self.buttonAdbApIfSystemPropertiesSet.Enable()
                self.buttonAdbApIfSystemPropertiesGet.Enable()
                self.buttonAdbApIfActionsStart.Enable()
                # Forward port...:
                forwardThread=MainFrameThreads(self, RistrettoCommon.ADB, args=['FORWARD', self.defaultSerialPort,self.defaultSerialSocket], thread=False)
                if forwardThread.err==0:
                    if self.platform.allowUnlock:
                        checkLockThread=MainFrameThreads(self, RistrettoCommon.CHECK_LOCK_TYPE, thread=False)
                        if checkLockThread.rsp == 'production':
                            m=MainFrameThreads(self, RistrettoCommon.CHECK_PCID, thread=False)
                            self.pcid_to_unlock=m.rsp
                            if self.pcid_to_unlock:
                                self.buttonUnlock.Enable(True)
                                self.buttonUnlock.SetLabel(u'Download/Flash certificate\nChip version: {0}'.format(checkLockThread.rsp))
                            else:
                                self.buttonUnlock.Enable(False)
                                self.buttonUnlock.SetLabel(u'Fail to retreive PCID\nChip version: {0}'.format(checkLockThread.rsp))
                        else:
                            self.buttonUnlock.Enable(False)
                            self.buttonUnlock.SetLabel(u'Board unlocked\nChip version: {0}'.format(checkLockThread.rsp))
                else:
                    print "Fail to forward modem port to {0}, please enable port forwading manually".format(self.defaultSerialSocket)

        except Exception:
            PrintException()

    def _initInterfaceTab(self):
        '''
        Init GUI regarding interface used: HIF or ADB
        '''
        if self.interfaceMode==RistrettoCommon.RISTRETTO_ADB:
            #Change frame title
            title=self.SetTitle('Ristrettoid')
            # Remove board repair tab
            self.notebook.RemovePage(RistrettoCommon.BOARD_REPAIR_PAGE_NUMBER)
            #Remove host interface tab
            page_to_remove=RistrettoCommon.SETTINGS_PAGE_NUMBER
            item = self.File.FindItemById(wxID_MAINFRAMEFILEINTERFACESWITCH)
            item.SetItemLabel('Switch to Datacard Mode')
            #Check ADB tool has been found
            browse=False
            if not self.conn.adb:
                browse=True
            elif not self.conn.adb.path:
                browse=True
            if browse:
                path=self.BrowseForDir(msg='Indicate valid ADB tool path...')
                if not path:
                    print 'WARNING: NO VALID ADB TOOL FOUND.'
                    print 'PLEASE USE Tools MENU TO INDICATE ADB TOOL PATH'
                else:
                    err = self.conn.UpdateAdbPath(path)
                    if err:
                        print u'ERROR: no valid ADB tool found in {0}'.format(path)
                    else:
                        print u'Will use {0} for ADB tool'.format(path)
                        print 'WARNING: IT IS PREFERIBLE TO INDICATE ADB TOOL PATH IN SYSTEM ENVIRONMENT \'PATH\' VARIABLE'
            # Init actions choice box...
            self._initAdbActions()
            # Init sys prop comboBox...
            self._initProperties()
        else:
            #Remove ADB tool menu entry
            self.Tools.Remove(wxID_MAINFRAMETOOLSADBTOOLPATHESELECT)
            self.Tools.Remove(wxID_MAINFRAMETOOLSADBLOGCAT)
            #Remove update options:
            self.checkBoxUpdateEnableCbc.Hide()
            self.checkBoxUpdateEnableKrm.Hide()
            self.checkBoxUpdateFilRestart.Hide()
            self.staticBoxUpdateOptions.Hide()
            self.boxSizerUpdateTabs.RemoveSizer(self.staticBoxSizerUpdateOptions)
            #Remove adb interface tab
            page_to_remove=RistrettoCommon.ADB_AP_IF_PAGE_NUMBER

        self.notebook.RemovePage(page_to_remove)

    def _logCb(self, string):
        '''
        Logging callback: all text displayed in console can be filtered here...
        '''
        self.txtCtrlConsole.AppendText(string)

    def _applyConfig(self):
        # Get Interface mode
        if self.platform.useAdb == True:
            self.interfaceMode=RistrettoCommon.RISTRETTO_ADB
            if self.platform.allowUnlock and IceraToolbox.IsWindows():
                self.staticBoxUnlock.Show(True)
                self.buttonUnlock.Show(True)
            # No loader by default
            self.checkBoxLDR.SetValue(False)
        else:
            self.interfaceMode=RistrettoCommon.RISTRETTO_HIF
            # No BT3
            self.checkBoxBT3.SetValue(False)
            if self.platform.allowUnlock and IceraToolbox.IsWindows():
                self.staticBoxUnlock.Show(False)
                self.buttonUnlock.Show(False)
            self.checkBoxBT3.Hide()


    def _applySettings(self):
        '''
        Update Frame based on settings file read at init.

        This settings are updated regularly at runtime and saved once when
         closing Frame.
        '''
        try:
            if self.settings.has_key("advancedFrameSize"):
                self.SetSize(self.settings["advancedFrameSize"])
            else:
                self.SetSize((634, 690))
            if self.settings.has_key("advancedFramePosition"):
                self.SetPosition(self.settings["advancedFramePosition"])

            if self.settings.has_key("releaseItems"):
                self.comboBoxPath.SetItems(self.settings["releaseItems"])
            else:
                self.settings["releaseItems"] = []

            if self.settings.has_key("TcpSocket"):
                self.comboBoxComPort.SetItems(self.settings["TcpSocket"])
            else:
                self.settings["TcpSocket"] = []

            if self.settings.has_key("singleItems"):
                self.comboBoxSingle.SetItems(self.settings["singleItems"])
            else:
                self.settings["singleItems"] = []

            if self.settings.has_key("xmlItems"):
                self.comboBoxXmlSourcePath.SetItems(self.settings["xmlItems"])
            else:
                self.settings["xmlItems"] = []

            if self.settings.has_key("atCmdItems"):
                self.comboBoxAtCommands.SetItems(self.settings["atCmdItems"])
            else:
                self.settings["atCmdItems"] = []

            if self.settings.has_key("bt2BoardRepairItems"):
                self.comboBoxUartBT2.SetItems(self.settings["bt2BoardRepairItems"])
            else:
                self.settings["bt2BoardRepairItems"] = []

            if self.settings.has_key("appliBoardRepairIitems"):
                self.comboBoxUartAppli.SetItems(self.settings["appliBoardRepairIitems"])
            else:
                self.settings["appliBoardRepairIitems"] = []

            if self.settings.has_key("packageBoardRepairIitems"):
                self.comboBoxFactReleaseUpdate.SetItems(self.settings["packageBoardRepairIitems"])
            else:
                self.settings["packageBoardRepairIitems"] = []

            if self.settings.has_key("calibItems"):
                self.comboBoxCalibrationFiles.SetItems(self.settings["calibItems"])
            else:
                self.settings["calibItems"] = []

            if self.settings.has_key("fileInfoItems"):
                self.comboBoxFirmwareInfo.SetItems(self.settings["fileInfoItems"])
            else:
                self.settings["fileInfoItems"] = []

            if self.settings.has_key("keysDirItems"):
                self._initKeyMenus()
            else:
                self.settings["keysDirItems"] = {}
                for key in self.platform.keys:
                    acr=self.platform.GetAcr(key)
                    self.settings["keysDirItems"][acr] = []

            if self.settings.has_key("UpdaterItems"):
                self._initUpdaterLibMenu(self.settings["UpdaterItems"])
            else:
                self.settings["UpdaterItems"] = []

            if self.settings.has_key("crashInfoItems"):
                self.comboBoxCrashInfoLogPath.SetItems(self.settings["crashInfoItems"])
            else:
                self.settings["crashInfoItems"] = []

            if self.settings.has_key("crashInfoFolderItems"):
                self.comboBoxLogFolder.SetItems(self.settings["crashInfoFolderItems"])
            else:
                self.settings["crashInfoFolderItems"] = []

            if self.settings.has_key("chipTypeItem"):
                self.platform.chip = self.settings["chipTypeItem"]
            else:
                self.settings["chipTypeItem"] = self.platform.chip

            if not self.settings.has_key("gangimagedir"):
                self.settings["gangimagedir"] = os.getcwd()
            self.gangimagedir = self.settings["gangimagedir"]

            if self.settings.has_key("interfaceMode"):
                self.interfaceMode = self.settings["interfaceMode"]

            if self.settings.has_key("sysPropertyItems"):
                self.comboBoxAdbApIfSystemProperties.SetItems(self.settings["sysPropertyItems"])
            else:
                self.settings["sysPropertyItems"] = []

            if self.settings.has_key("sysPropertyValueItems"):
                self.comboBoxAdbApIfSystemPropertiesValue.SetItems(self.settings["sysPropertyValueItems"])
            else:
                self.settings["sysPropertyValueItems"] = []

            if self.settings.has_key("portForwardItems"):
                self.comboBoxAdbApIfForward.SetItems(self.settings["portForwardItems"])
            else:
                self.settings["portForwardItems"] = []

            if self.settings.has_key("socketForwardItems"):
                self.comboBoxAdbApIfForwardSocket.SetItems(self.settings["socketForwardItems"])
            else:
                self.settings["socketForwardItems"] = []

        except Exception, message:
            PrintException(msg=message)

    def _updateSettingsDict(self, field, subfield, value, number=10, list=True):
        update = False
        if list == True:
            # Update a list
            if value not in self.settings[field][subfield]:
                # Store setting value: no more than indicated number.
                if len(self.settings[field][subfield]) == number:
                    self.settings[field][subfield].__delitem__(0)
                update = True
        else:
            # Update a single item in dict
            update = True

        if update:
            self.settings[field][subfield].append(value)

    def _disableComPortSettings(self):
        self.staticTextHifBaudrate.Disable()
        self.choiceHifBaudrate.Disable()
        self.checkBoxFlowControl.Disable()
        self.comboBoxCOMBlockSize.Disable()
        self.staticTextCOMBlockSize.Disable()

    def _enableComPortSettings(self):
        if self.libversion >= 9.04:
            self.staticTextHifBaudrate.Enable()
            self.choiceHifBaudrate.Enable()
        self.checkBoxFlowControl.Enable()
        self.comboBoxCOMBlockSize.Enable()
        self.staticTextCOMBlockSize.Enable()

    def _initBaudrateChoiceBoxes(self):
        if self.libversion >= 9.04:
            for rate in RistrettoCommon.SUPPORTED_UART_BAUDRATES:
                self.choiceBromComBaudrate.Append(rate)
                self.choiceAppComBaudrate.Append(rate)
                self.choiceHifBaudrate.Append(rate)
        else:
            self.choiceBromComBaudrate.Disable()
            self.choiceAppComBaudrate.Disable()
            self.staticTextBromComBaudrate.Disable()
            self.staticTextAppComBaudrate.Disable()
        if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
            self.choiceHifBaudrate.SetStringSelection(str(self.conn.baudrate))
            self.choiceAppComBaudrate.SetStringSelection(str(self.conn.appBaudrate))
            self.choiceBromComBaudrate.SetStringSelection(str(self.conn.bromBaudrate))

    def _initBlockSizeChoiceBoxes(self):
        if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
            for rate in RistrettoCommon.SUPPORTED_UART_BLOCKSIZE:
                self.comboBoxCOMBlockSize.Append(rate)
            self.comboBoxCOMBlockSize.SetLabel(str(self.conn.blockSize))

    def _disableActions(self, event_button=None):
        '''
        Disable some GUI items responsible for actions on target.
        '''
        try:
            # Disable all buttons supposed to cause action on target
            self.buttonApplyHifSwitch.Disable()
            if self.choiceCrashInfo.GetStringSelection() != 'DECODE_COREDUMP':
                self.buttonCrashInfo.Disable()
            if self.choicePlatInfo.GetStringSelection() != 'DECODE_FLASH_DUMP':
                self.buttonStartPlatInfo.Disable()
            if event_button:
                event_button.Disable()
                event_button.SetBackgroundColour(wx.RED)
            # Disable all txtCtrl or combo box supposed to cause action on target
            self.comboBoxAtCommands.Disable()
            # Disable all checkBox/radiobutton supposed to cause action on target
            self.radioButtonUartHif.Disable()
            self.radioButtonUsbHif.Disable()

            self.buttonFlashRelease.Disable()
            self.buttonFlashSingle.Disable()
            self.buttonFlashImei.Disable()
            self.buttonFlashCalibrationFiles.Disable()
            self.buttonProgramXmlSource.Disable()

            if self.conn.mode == RistrettoCommon.RISTRETTO_ADB:
                self.buttonAdbApIfForward.Disable()
                self.buttonAdbApIfSystemPropertiesSet.Disable()
                self.buttonAdbApIfSystemPropertiesGet.Disable()
                self.buttonAdbApIfActionsStart.Disable()
                if self._devLog._devLog:
                    if self._devLog._devLog.adb.State == IceraAdb.ConnectionState.DISCONNECTED:
                        self._devLog.Hide()
                self.menuLogcat.Enable(False)

        except Exception:
            PrintException()

    def _enableActions(self, event_button):
        '''
        Enable some GUI items responsible for actions on target.
        '''
        try:
            # Re-enable buttons
            self.buttonFlashRelease.Enable()
            self.buttonFlashSingle.Enable()
            self.buttonFlashImei.Enable()
            self.buttonFlashCalibrationFiles.Enable()
            self.buttonProgramXmlSource.Enable()
            if event_button:
                event_button.Enable()
                event_button.SetBackgroundColour(self.OriginalBtnColor)
                if event_button == self.buttonStopBoardRepair:
                    self.buttonStartBoardRepair.SetBackgroundColour(self.OriginalBtnColor)
            # Re-enable checkBox
            self.radioButtonUartHif.Enable()
            self.radioButtonUsbHif.Enable()

            self.buttonApplyHifSwitch.Enable()
            self.buttonCrashInfo.Enable()
            self.buttonStartPlatInfo.Enable()
            self.comboBoxAtCommands.Enable()
            self.buttonAdbApIfForward.Enable()

            if self.conn.mode == RistrettoCommon.RISTRETTO_ADB:
                if self.platform.conn.IsSingleFlash():
                    
                    # Re-enable port selection
                    self.comboBoxAdbApIfForward.Enable()
                    # Re-enable socket selection
                    self.comboBoxAdbApIfForwardSocket.Enable()
                self.buttonAdbApIfSystemPropertiesSet.Enable()
                self.buttonAdbApIfSystemPropertiesGet.Enable()
                self.buttonAdbApIfActionsStart.Enable()
                self.menuLogcat.Enable(True)

        except Exception:
            PrintException()

    def _reEnableActions(self, button=None):
        '''
        Re-enable some GUI items responsible for actions on target regarding
         USB detection results.
        '''
        if self.multiPlatform == False or self.conn.autoSelect == False:
            # Re-enable all functionalities
            self._enableActions(button)
        else:
            # Re-enable only release/single update functionality
            if button:
                button.SetBackgroundColour(self.OriginalBtnColor)
            self.buttonFlashRelease.Enable()
            self.buttonFlashSingle.Enable()
            self.buttonProgramXmlSource.Enable()

    def _updateDeviceChoiceBox(self, deviceList):
        '''
        Update device list combo box after a scan.
        '''
        # Append new detected ports:
        for dev in deviceList:
            if dev not in self.deviceList:
                self.deviceList.append(dev)

        # Get current values before clear all
        current_device = self.comboBoxAdbApIfDevices.GetValue()

        # Remove useless ports:
        self.comboBoxAdbApIfDevices.Clear()
        self.deviceList.sort()
        for dev in self.deviceList:
            if dev not in deviceList:
                self.deviceList.remove(dev)

        if current_device not in deviceList:
            current_device = ""

        if current_device == "" and self.deviceList != []:
            current_device = self.deviceList[0]

        # Update devices combo box:
        for dev in self.deviceList:
            self.comboBoxAdbApIfDevices.Append(dev)

        # Put back current value
        self.comboBoxAdbApIfDevices.SetValue(current_device)
        if current_device != "":
            self._getAdbDeviceValue()
            self.log.DisplayConnectStatus("Connected with %s" % current_device)
        else:
            self.log.DisplayConnectStatus("No ADB device connected")
            self.checkBoxBT3.Enable()
            self.checkBoxUpdateEnableCbc.Enable()

    def _updateComportChoiceBox(self, portList, uartList):
        '''
        Update all port combo boxes after a scan.
        '''
        # Append new detected ports:
        for port in portList:
            if port not in self.portList:
                self.portList.append(port)

        # Get current values before clear all
        current_port = self.comboBoxComPort.GetValue()

        # Remove useless ports:
        self.comboBoxComPort.Clear()
        self.portList.sort()
        for port in self.portList:
            if port not in portList:
                self.portList.remove(port)

        # Update ports Combo box (and UART ports Combo box used for Board Repair...)
        self.comboBoxUartDiscoverySelectPort.Clear()
        self.comboBoxFactUartServer.Clear()
        for port in self.portList:
            self.comboBoxComPort.Append(port)
            if port in uartList:
                self.comboBoxUartDiscoverySelectPort.Append(port)
                self.comboBoxFactUartServer.Append(port)
        #Add tcp ports saved
        if self.settings.has_key("TcpSocket"):
            for tcpsocket in self.settings["TcpSocket"]:
                self.comboBoxComPort.Append(tcpsocket)
        else:
            self.settings["TcpSocket"] = []

        # Put back current value
        self.comboBoxComPort.SetValue(current_port)
        if current_port != "":
            self.log.DisplayConnectStatus("Connected on %s" % current_port)
        else:
            self.log.DisplayConnectStatus("No COM port selected")

    def _updateConnectionStatus(self):
        if self.conn.mode == RistrettoCommon.RISTRETTO_HIF:
            self._updateComportChoiceBox(self.conn.comPortList, self.conn.uartPortList)
            if self.conn.autoSelect == True:
                if self.conn.detected == 0:
                    self.log.DisplayConnectStatus('No platform connected on USB')
                    self._disableActions()
                else:
                    if len(self.conn.mdmPortList) > 1:
                        self.multiPlatform = True
                        if self.platform.verboseLevel > IceraToolbox.VERB_INFO:
                            print 'WARNING: multiple platforms detected'
                            print '\n%d platforms connected on: ' % len(self.conn.mdmPortList)
                            for i in self.conn.mdmPortList: print i
                            print '\nONLY FIRMWARE UPDATE ENABLED FOR MULTI PLATFORMS.'
                            print 'For any other feature, please, disable autodetect configuration and indicate a valid COM port value.\n'
                        self.log.DisplayConnectStatus('Multiple platforms connected')
                    else:
                        self.multiPlatform = False
                        self.log.DisplayConnectStatus('Connected on %s' % self.conn.mdmPortList[0])
                        if self.conn.mdmPortList[0] == 'MBIM':
                            self.comboBoxCOMBlockSize.SetLabel(str(4000))
                            self.conn.UpdateBlockSize(4000)
                    if self.ongoingThread == False:
                        self._reEnableActions()
            else:
                self._enableActions(None)
        elif self.conn.mode == RistrettoCommon.RISTRETTO_ADB:
            self._updateDeviceChoiceBox(self.conn.devices)
            if self.conn.autoSelect == True:
                if self.conn.detected == 0:
                    self.log.DisplayConnectStatus('No ADB device connected')
                    self._disableActions()
                    self.buttonUnlock.Enable(False)
                    self.buttonUnlock.SetLabel("No ADB device connected\n")
                else:
                    if len(self.conn.devices)>1:
                        self.multiPlatform = True
                        if self.platform.verboseLevel > IceraToolbox.VERB_INFO:
                            print 'INFO: multiple platforms detected'
                            print '\n %d platforms connected on: ' % len(self.conn.devices)
                            for i in self.conn.devices: print i
                            print ' NOT SUPPORTED: please use ADB devices separately with Ristretto.'
                            print ' For any feature, disable automatic device selection and indicate a valid ADB device value.\n'
                        self.log.DisplayConnectStatus('Multiple platforms connected')
                        self._disableActions()
                        self.buttonUnlock.SetLabel("Multiple platforms detected\nUnable to unlock")
                        self.buttonUnlock.Enable(False)
                    else:
                        self.multiPlatform = False
            else:
                self._enableActions(None)

    def _frameClose(self, exit=True):
        close = True
        if self.ongoingThread:
            close = CloseConfirmation()
        if close:
            self._devLog.Close()
            self.platform.Close()
            if self.settings:
                if self.GetPosition() == wx.Point(-32000, -32000):
                    # main windows is iconized: at next start-up apply default size & pos
                    size = wx.Size(572, 634)
                    pos= wx.Point(-1, -1)
                else:
                    size = self.GetSize()
                    pos = self.GetPosition()
                self.settings["advancedFrameSize"] = size
                self.settings["advancedFramePosition"] = pos
                RistrettoCommon.StoreSettings(self.settings)
                if hasattr(sys, 'frozen') and exit:
                    for (dirpath, dirnames, filenames) in os.walk(RistrettoCommon.valid_basename):
                        for dirname in dirnames:
                            os.chmod(os.path.join(dirpath,dirname), 0755)
                        for filename in filenames:
                            os.chmod(os.path.join(dirpath,filename),0755)
                    for folder_name in ['drivers','icera-log-utils']:
                        if os.path.exists(os.path.join(RistrettoCommon.valid_basename,folder_name)):
                            shutil.rmtree(os.path.join(RistrettoCommon.valid_basename,folder_name))
                    for path in os.listdir(RistrettoCommon.RISTRETTO_PATH):
                        if path not in ['Dumps','config.txt','ristretto_core.exe','.ristretto']:
                            if os.path.isdir(path):
                                shutil.rmtree(path)
                            else:
                                os.remove(path)
            if exit:
                sys.exit()

    def _frameRestart(self):
        self._frameClose(exit=False)
        RistrettoCommon.Restart()

    def _displayConfig(self, out=True, fd=None):
        '''
        Displays Ristretto's config: the one contained in config.txt
        '''
        str = ''
        if self.platform.existingConfig == False:
            str += 'Ristretto is using standard default value.\n'
        else:
            file = open(self.platform.configFile, 'r')
            lines = file.readlines()
            for line in lines:
                if line[0] != '#':
                    str += '{0}\n'.format(line.strip('\n'))
            file.close()

        str += '\n'
        str += 'UpdaterLib:\n'
        str += u'{0}\n'.format(self.platform.GetLibPath())
        for key in self.platform.keys:
            acr=self.platform.GetAcr(key)
            str += '\n%s keys:\n' % acr
            str += u'{0}'.format(self.platform.GetKeyPath(acr))
        str += '\n\n'

        if out:
            print str
        if fd:
            fd.write(str)

    def _comboDirname(self, combobox):
        dirname = None
        current = combobox.GetValue()
        if current == '':
            items=combobox.GetItems()
            if items != []:
                current = items[-1]
        if current != '':
            if os.path.isfile(current):
                dirname = os.path.dirname(current)
            elif os.path.isdir(current):
                dirname = current
        return dirname

    def _dispDlgFrame(self, frame, create_cb):
        try:
            if frame == None:
                frame = create_cb()
                frame.Show()
            else:
                if frame.GetPosition() == wx.Point(-32000, -32000):
                    # iconized frame
                    frame.Iconize(False)
                else:
                    frame.SetFocus()
        except Exception:
            PrintException()
        finally:
            return frame

    def _addMenuElem(self, menu, elem, event_cb):
        id = wx.NewId()
        title = menu.GetTitle()
        menu.Append(id=id, kind=wx.ITEM_RADIO, text=elem)
        self.Bind(wx.EVT_MENU, event_cb, id=id)
        item = menu.FindItemById(id)
        item.Check()
        self.addedItemsList[id] = [title, elem]

    def _updateMenuList(self, menu, list, event_cb):
        menuItemsLabelList = []
        try:
            for i in menu.GetMenuItems():
                menuItemsLabelList.append(i.GetLabel())
            for i in list:
                if i not in menuItemsLabelList:
                    self._addMenuElem(menu, i, event_cb)
        except Exception:
            PrintException()

    ################################################
    #                                              #
    # Below are some exported Frame functions      #
    #                                              #
    # To be cleaned...                             #
    #                                              #
    ################################################
    def BrowseForFile(self, msg='Select a file...', wildcard='*', defaultDir=None, defaultFile="", comboBox=None, parent=None, style=wx.OPEN):
        if defaultDir== None:
            defaultDir = self.defaultDir
        file = None
        if parent == None:
            parent = self
        dlg = wx.FileDialog(parent, message=msg, defaultDir=defaultDir,
                            defaultFile=defaultFile, wildcard=wildcard, style=style)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            file = dlg.GetPath()
            if comboBox != None:
                if file not in comboBox.GetItems():
                    comboBox.Append(file)
                comboBox.SetValue(file)
            self.defaultDir = os.path.dirname(file)
        else:
            dlg.Destroy()
        return file

    def BrowseForDir(self, msg='Select a directory...', defaultDir=None, title='Browsing...', comboBox=None, parent=None):
        if defaultDir== None:
            defaultDir = self.defaultDir
        dir = None
        if parent == None:
            parent = self
        dlg = wx.DirDialog(parent, msg, defaultPath=defaultDir, style=wx.DD_DEFAULT_STYLE, pos=wx.Point(104, 32), size=wx.Size(320, 64), name=title)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            dir = dlg.GetPath()
            if comboBox != None:
                if dir in comboBox.GetItems():
                    Items=comboBox.GetItems()
                    comboBox.Clear()
                    Items.remove(dir)
                    Items.append(dir)
                    comboBox.AppendItems(Items)
                else:
                    comboBox.Append(dir)
                comboBox.SetValue(dir)
            self.defaultDir = dir
        else:
            dlg.Destroy()
        return dir

    def UpdateSettings(self, field, value, number=10, list=True):
        update = False
        if list == True:
            # Update a list
            if value not in self.settings[field]:
                # Store setting value: no more than indicated number.
                if len(self.settings[field]) == number:
                    self.settings[field].__delitem__(0)
                update = True
        else:
            # Update a single item
            update = True

        if update:
            self.settings[field].append(value)

    def BrowseFileForCombo(self, combobox, parent=None, msg='Select file...', wildcard='*', style=wx.OPEN):
        # Start browsing from current box path if exists
        dir = self._comboDirname(combobox)
        self.BrowseForFile(msg=msg, wildcard=wildcard, defaultDir=dir, comboBox=combobox, parent=parent, style=style)

    def BrowseDirForCombo(self, combobox, parent=None, msg='Select path...', title=''):
        # Start browsing from current box path if exists
        dir = self._comboDirname(combobox)
        self.BrowseForDir(msg=msg, defaultDir=dir, title=title, comboBox=combobox, parent=parent)

    ############################################################################
    #                                                                          #
    # Below are all the Frame events handlers for:                             #
    #    - File menu items                                                     #
    #    - Help menu items                                                     #
    #    - Flashing tab                                                        #
    #    - Configuration files tab                                             #
    #    - Debug tab                                                           #
    #    - Board repair tab                                                    #
    #    - Settings tab                                                        #
    #                                                                          #
    ############################################################################
    def OnFrame1Close(self, event):
        self._frameClose()

    ############################################################################
    #                                                                          #
    # FILE MENU ITEMS                                                          #
    #                                                                          #
    ############################################################################
    # EXIT
    def OnFileItems2Menu(self, event):
        self._frameClose()

    # SAVE LOG
    def OnFileItemssavelogMenu(self, event):
        fd = None
        timeStr = time.strftime("%Y%m%d-%Hh%M")
        try:
            logfile = 'rislog_' + timeStr + '.txt'
            file = self.BrowseForFile(msg='Log file', wildcard='*.txt', defaultFile=logfile, style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
            if file:
                ok = self.log.StoreLog(self.platform, file, console_log=self.txtCtrlConsole, tool_config=self.tool_config)
                if ok: PopUpInfo(u"Ristretto log stored in {0}".format(file))

        except Exception:
            PrintException()
            print 'ERROR. Fail to store Ristretto log...'

        finally:
            if fd:
                fd.close()

        fd = None
        # if we used ADB interface, try saving the logcat messages
        log = self._devLog.GetLog()
        if log != "": # no need to do anything for an empty log
            try:
                logfile = 'logcat_' + timeStr + '.txt'
                file = self.BrowseForFile(msg='Logcat file', wildcard='*.txt', defaultFile=logfile)
                if file:
                    fd = open(file, "wb")
                    fd.write(log)
            except Exception:
                PrintException()
                print 'ERROR. Fail to store logcat log...'
            finally:
                if fd:
                    fd.close()

    # SCAN CONNECTED PLATFORM
    def OnFileItems3Menu(self, event):
         self._disableActions() # re-enabled or not with _updateConnectionStatus...
         self.conn.Scan() # force re-scan when enable autodetect is ticked manually
         self._updateConnectionStatus()

    # VERBOSITY
    def OnVerbosityVerbinfoMenu(self, event):
        self.platform.UpdateVerbosity(IceraToolbox.VERB_INFO)

    def OnVerbosityVerbsilentMenu(self, event):
        self.platform.UpdateVerbosity(IceraToolbox.VERB_NONE)

    def OnVerbosityVerberrMenu(self, event):
        self.platform.UpdateVerbosity(IceraToolbox.VERB_ERROR)

    def OnVerbosityVerbdebugMenu(self, event):
        self.platform.UpdateVerbosity(IceraToolbox.VERB_DEBUG)

    def OnVerbosityVerbdumpMenu(self, event):
        self.platform.UpdateVerbosity(IceraToolbox.VERB_DUMP)

    #  CHANGE KEY PATH
    def OnICE_ICEIce_iceMenu(self, event):
        self._updateKeyFolder('ICE_ICE')

    def OnICE_OEMIce_oemMenu(self, event):
        self._updateKeyFolder('ICE_OEM')

    def OnOEM_FACTOem_factMenu(self, event):
        self._updateKeyFolder('OEM_FACT')

    def OnOEM_FIELDOem_fieldMenu(self, event):
        self._updateKeyFolder('OEM_FIELD')

    def OnICE_DBGIce_dbgMenu(self, event):
        self._updateKeyFolder('ICE_DBG')

    def _onSelectedKeyPath(self, event):
        src_id = event.GetId()
        key_acr = self.addedItemsList[src_id][0]
        self.keysDir[key_acr] = self.addedItemsList[src_id][1]
        (err, signing) = self.platform.IsKeyFolderOk(self.keysDir[key_acr], key_acr)
        self.platform.UpdateKeyPath(self.keysDir[key_acr], key_acr, signing)
        print '%s key set selected in %s' % (key_acr, self.keysDir[key_acr])

    def _initKeysSettings(self):
        self.keyMenus = {}
        self.keysDir = {}
        for key in self.platform.keys:
            acr=self.platform.keys[key]['acr']
            self.keyMenus[acr] = getattr(self, acr)
            self.keysDir[acr] = self.platform.GetKeyPath(acr)
            self._addMenuElem(self.keyMenus[acr], self.keysDir[acr], self._onSelectedKeyPath)

    def _initKeyMenus(self):
        for key in self.platform.keys:
            acr=self.platform.keys[key]['acr']
            if self.keyMenus[acr]:
                if not self.settings["keysDirItems"].has_key(acr):
                    self.settings["keysDirItems"][acr]=[]
                self._updateMenuList(self.keyMenus[acr], self.settings["keysDirItems"][acr], self._onSelectedKeyPath)
        # The last in list has been checked whereas it is not always the default at start-up...
        # Let's Check the default for each key set menu
        for key in self.platform.keys:
            acr=self.platform.keys[key]['acr']
            if self.keyMenus[acr]:
                for i in self.keyMenus[acr].MenuItems:
                    if i.GetLabel() == self.keysDir[acr]:
                        i.Check()

    def _updateKeyFolder(self, key_set):
        if key_set in self.keysDir:
            key_folder = self.BrowseForDir(msg='Select %s keys folder...:' %  str(key_set), defaultDir=self.keysDir[key_set], title='KeyFiles')
            if key_folder != None:
                (err, signing) = self.platform.IsKeyFolderOk(key_folder, key_set)
                if err:
                    print 'ERROR: Incomplete key folder...'
                else:
                    self.keysDir[key_set] = key_folder
                    self._updateSettingsDict("keysDirItems", key_set, key_folder)
                    self._updateMenuList(self.keyMenus[key_set], self.settings["keysDirItems"][key_set], self._onSelectedKeyPath)
                    self.platform.UpdateKeyPath(key_folder, key_set, signing)
                    print '\nWill use %s keys from: %s\n' % (str(key_set), key_folder)

    # CLEAR CONSOLE
    def OnFileItemsclearconsoleMenu(self, event):
        self.txtCtrlConsole.Clear()

    # SELECT CHIP TYPE
    def _onSelectedChipType(self, event):
        id = event.GetId()
        chip = self.addedItemsList[id][1]
        self.platform.chip = chip
        self.settings["chipTypeItem"] = self.platform.chip

    def _initChipTypeMenu(self):
        try:
            # update default platform value (if needed...):
            if const.CHIP_TYPES.get(int(self.platform.chip)) == None:
                # default platform chip is not supported here...
                self.platform.chip = None
                for type,value in const.CHIP_TYPES.items():
                    if value != None:
                        # take 1st available chip in list...
                        self.platform.chip = str(type)
                        self.settings["chipTypeItem"] = self.platform.chip
                        break
                if self.platform.chip == None:
                    # ...
                    print '\n #######################\n'
                    print 'THIS RISTRETTO VERSION DOESN\'T SUPPORT ANY ICERA\'S CHIP TYPE !!!!!!'
                    print '\n #######################\n'
                    self.notebook.Disable()

            # update chip type select menu:
            for type,value in const.CHIP_TYPES.items():
                if value != None:
                    self._addMenuElem(self.chipType, str(type), self._onSelectedChipType)
            for i in self.chipType.MenuItems:
                if i.GetLabel() == self.platform.chip:
                    i.Check()

        except Exception:
            PrintException()

    # SWITCH INTERFACE MODE
    def OnFileInterfaceswitchMenu(self, event):
        try:
            if self.conn.mode == RistrettoCommon.RISTRETTO_HIF:
                # Switch to adb mode:
                # In advanced mode, will remove Host Interface tab at start-up
                self.settings["interfaceMode"] = RistrettoCommon.RISTRETTO_ADB
            elif self.conn.mode == RistrettoCommon.RISTRETTO_ADB:
                # Switch to hif advanced mode: will remove ADB Interface tab at start-up
                self.settings["interfaceMode"] = RistrettoCommon.RISTRETTO_HIF
            RistrettoCommon.StoreSettings(self.settings)
            self._frameRestart()
        except Exception:
            PrintException()

    ############################################################################
    #                                                                          #
    # TOOLS MENU ITEMS                                                         #
    #                                                                          #
    ############################################################################
    # build_icera_file
    def _createBuildDataFileFrame(self):
        return BuildDataFileFrame.create(self)

    def OnToolsItems0Menu(self, event):
        self.BuildDlg = self._dispDlgFrame(self.BuildDlg, self._createBuildDataFileFrame)

    # updaterLib
    def _onSelectedUpdaterLib(self, event):
        src_id = event.GetId()
        libname = self.addedItemsList[src_id][1]
        self._updateUpdaterLibUsage(libname)

    def _updateUpdaterLibUsage(self, libname):
        self.updaterLibDir = os.path.dirname(libname)
        self.platform.LibSwitch(libname)
        self.libversion = float(self.platform.LibVersion())

    def _initUpdaterLibMenu(self, list):
        self._updateMenuList(self.UpdaterLibMenu, list, self._onSelectedUpdaterLib)
        # The last in list has been checked whereas it is not always the default at start-up...
        # Let's Check the default updater lib in menu
        for i in self.UpdaterLibMenu.MenuItems:
            if i.GetLabel() == self.platform.GetLibPath():
                i.Check()

    def _updateUpdaterLib(self,libname):
        try:
            self.UpdateSettings("UpdaterItems", libname)
            self._updateMenuList(self.UpdaterLibMenu, self.settings["UpdaterItems"], self._onSelectedUpdaterLib)
            self._updateUpdaterLibUsage(libname)
        except Exception:
            PrintException()

    def OnUpdaterLibMenuItems0Menu(self, event):
        if IceraToolbox.IsWindows():
            libname = self.BrowseForFile(msg='Select UpdaterLib dll...', wildcard='*.dll', defaultDir=self.updaterLibDir)
        else:
            libname = self.BrowseForFile(msg='Select UpdaterLib so...', wildcard='*.so', defaultDir=self.updaterLibDir)
        if libname != None:
            self._updateUpdaterLib(libname)

    #ADB tool path
    def OnToolsAdbtoolpatheselectMenu(self, event):
        path=self.BrowseForDir(msg='Indicate valid ADB tool path...')
        if not path:
            print 'ERROR: NO VALID ADB TOOL PATH SELECTED.'
        else:
            err = self.conn.UpdateAdbPath(path)
            if err:
                print u'ERROR: no valid ADB tool found in {0}'.format(path)
            else:
                print u'Will use {0} for ADB tool'.format(path)
                print 'WARNING: IT IS PREFERIBLE TO INDICATE ADB TOOL PATH IN SYSTEM ENVIRONMENT \'PATH\' VARIABLE'

    def OnToolsAdbLogcat(self, event):
        device = self.comboBoxAdbApIfDevices.GetValue()
        if not device: # we have no autodiscovered devices
            print 'ERROR: NO ANDROID DEVICES DISCOVERED.'
            return

        self._devLog.ShowLog(device)

    ############################################################################
    #                                                                          #
    # HELP MENU ITEMS                                                          #
    #                                                                          #
    ############################################################################
    # USER GUIDE
    def _createUserGuideFrame(self):
        return UserGuideFrame.create(self)

    def OnHelpItems2Menu(self, event):
        self.UserGuideDlg = self._dispDlgFrame(self.UserGuideDlg, self._createUserGuideFrame)

    # CONFIGURATION
    def OnHelpItems3Menu(self, event):
        self._displayConfig()

    # ABOUT
    def OnHelpItems0Menu(self, event):
        PopUpInfo('Ristretto ' + self.tool_config["version"] + '\n------\nUpdater DLL ' + str(self.libversion) + '\n------\nnVIDIA')

    ############################################################################
    #                                                                          #
    # UPDATE TAB                                                               #
    #                                                                          #
    ############################################################################
    # FULL RELEASE UPDATE
    ### Browse for a folder...
    def OnButtonPathBrowseButton(self, event):
        self.BrowseDirForCombo(self.comboBoxPath, msg='Select Release Package:', title='Release Package')

    ### Browse for a zip file...
    def OnButtonBrowseReleaseArchiveButton(self, event):
        self.BrowseFileForCombo(self.comboBoxPath, msg='Select Release Archive...', wildcard='*.zip;*.tar.gz;*.tgz;*.ipkg')

    def _getReleaseFiles(self):
        releaseFiles = {}
        releaseFiles["BT2"] = self.checkBoxBT2.GetValue()
        releaseFiles["BT3"] = self.checkBoxBT3.GetValue()
        releaseFiles["LDR"] = self.checkBoxLDR.GetValue()
        releaseFiles["IFT"] = False
        releaseFiles["MDM"] = self.checkBoxMDM.GetValue()
        releaseFiles["MASS"] = False
        releaseFiles["ZEROCD"] = False
        releaseFiles["DEVICECFG"] = self.checkBoxDEVICECFG.GetValue()
        releaseFiles["PRODUCTCFG"] = self.checkBoxPRODUCTCFG.GetValue()
        releaseFiles["AUDIOCFG"] = self.checkBoxAUDIOCFG.GetValue()
        return releaseFiles

    def OnButtonFlashReleaseButton(self, event):
        release_path = self.comboBoxPath.GetValue()
        comPort = self.comboBoxComPort.GetValue()
        if not release_path:
            print 'ERROR: PLEASE INDICATE A VALID RELEASE FOLDER.\n'
        else:
            if release_path.endswith('.zip') or release_path.endswith('.tgz') or release_path.endswith('.tar.gz') or release_path.endswith('.ipkg'):
                release_path = self.platform.ExtractArchive(self.extract_folder, release_path)
            if release_path:
                if (os.path.isdir(release_path) == 0):
                    print 'ERROR: %s NOT A VALID DIRECTORY\n' % release_path
                else:
                    print 'Selected release package: %s' % release_path
                    try:
                        releaseFiles = self._getReleaseFiles()
                        if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                            self._devLog.MonitorFlashing(self.comboBoxAdbApIfDevices.GetValue())
                        MainFrameThreads(self, RistrettoCommon.UPDATE_RELEASE, args=(release_path, releaseFiles), action_button=self.buttonFlashRelease, multi=True)

                    except Exception:
                        PrintException()

                    finally:
                        if release_path:
                            self.UpdateSettings("releaseItems", self.comboBoxPath.GetValue())
                        if "tcp:" in comPort:
                            self.UpdateSettings("TcpSocket", self.comboBoxComPort.GetValue())


    def _disableFileListButtons(self):
        try:
            self.checkBoxBT2.SetValue(False)
            self.checkBoxMDM.SetValue(False)
            self.checkBoxDEVICECFG.SetValue(False)
            self.checkBoxPRODUCTCFG.SetValue(False)
            self.checkBoxAUDIOCFG.SetValue(False)

            self.checkBoxBT3.SetValue(False)
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF or not self.conn.IsSingleFlash():
                self.checkBoxLDR.Enable()
                self.checkBoxLDR.SetValue(False)

        except Exception:
            PrintException()

    def _enableFileListButtons(self):
        try:
            self.checkBoxBT2.SetValue(True)
            self.checkBoxMDM.SetValue(True)
            self.checkBoxDEVICECFG.SetValue(True)
            self.checkBoxPRODUCTCFG.SetValue(True)
            self.checkBoxAUDIOCFG.SetValue(True)
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and self.conn.IsSingleFlash():
                self.checkBoxBT3.SetValue(True)
                self.checkBoxLDR.SetValue(False)
            else:
                self.checkBoxLDR.SetValue(True)

        except Exception:
            PrintException()

    def OnCheckBoxALLCheckbox(self, event):
        if self.checkBoxALL.GetValue() == False:
            self._disableFileListButtons()
        else:
            self._enableFileListButtons()

    def OnCheckBoxUpdateEnableCbcCheckbox(self, event):
        self.platform.UpdateCbcValue(self.checkBoxUpdateEnableCbc.GetValue())

    def OnCheckBoxUpdateEnableKrmCheckbox(self, event):
        self.platform.UpdateKrmValue(self.checkBoxUpdateEnableKrm.GetValue())

    def OnCheckBoxUpdateFilRestartCheckbox(self, event):
        self.platform.UpdateFilRestart(self.checkBoxUpdateFilRestart.GetValue())

    # SINGLE FILE UPDATE
    def OnButtonBrowseSingleButton(self, event):
        self.BrowseFileForCombo(self.comboBoxSingle, msg='Select File to program...', wildcard='*.wrapped;*.bin;*.icz')

    def OnButtonFlashSingleButton(self, event):
        ifile = self.comboBoxSingle.GetValue()
        if ifile:
            if (os.path.isfile(ifile) == 0):
                print 'ERROR: %s FILE DOESN\'T EXIST\n' % ifile
            else:
                print 'Selected file: %s' % ifile
                try:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        self._devLog.MonitorFlashing(self.comboBoxAdbApIfDevices.GetValue())
                    MainFrameThreads(self, RistrettoCommon.FILE_UPDATE, args=ifile, action_button=self.buttonFlashSingle, multi=True)

                except Exception:
                    PrintException()

                finally:
                    self.UpdateSettings("singleItems", ifile)
        else:
            print 'ERROR: PLEASE INDICATE A VALID FILE TO UPDATE.\n'

    # XML SOURCES
    def _initXmlSourceChoiceBox(self):
        self.xmlSourceType = None
        used_archive = ['PLATCFG', 'DEVICECFG', 'PRODUCTCFG']
        used_archive.append('AUDIOCFG')
        for key in const.ArchTypes.keys():
            if key in used_archive:
                self.choiceXmlSourceType.Append(key)

    def OnChoiceXmlSourceTypeChoice(self, event):
        self.xmlSourceType = self.choiceXmlSourceType.GetStringSelection()

    def OnButtonBrowseXmlSourceButton(self, event):
        self.BrowseFileForCombo(self.comboBoxXmlSourcePath, msg='Select File to program...', wildcard='*.xml')

    def OnButtonProgramXmlSourceButton(self, event):
        ifile = self.comboBoxXmlSourcePath.GetValue()
        if not ifile:
            print 'ERROR: you must select a valid XML source.'
        else:
            if os.path.isfile(ifile) and ifile.endswith('.xml'):
                print 'Will use %s to build and program %s data file' % (self.xmlSourceType, ifile)
                try:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        self._devLog.MonitorFlashing(self.comboBoxAdbApIfDevices.GetValue())
                    MainFrameThreads(self, RistrettoCommon.PROGRAM_XML, args=[self.xmlSourceType, ifile], action_button=self.buttonProgramXmlSource, multi=True)

                except Exception:
                    PrintException()

                finally:
                    self.UpdateSettings("xmlItems", ifile)
            else:
                print '%s NOT a valid file OR is a directory.' % ifile

    # IMEI
    def _programImei(self):
        imei = self.textCtrlEnterImei.GetValue()
        if not imei:
            print 'ERROR: you must enter a valid IMEI value.'
        elif not re.match('[0-9]{14}', imei):
            print 'ERROR: Invalid IMEI.'
        else:
            try:
                imei = imei + 'x'
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    self._devLog.MonitorFlashing(self.comboBoxAdbApIfDevices.GetValue())
                MainFrameThreads(self, RistrettoCommon.PROGRAM_IMEI, args=imei, action_button=self.buttonFlashImei)

            except Exception:
                PrintException()

    def OnTextCtrlEnterImeiTextEnter(self, event):
        self._programImei()

    def OnButtonFlashImeiButton(self, event):
        self._programImei()

    # CALIB
    def OnButtonBrowseCalibrationFilesButton(self, event):
        self.BrowseFileForCombo(self.comboBoxCalibrationFiles, msg='Select calibration file to program...', wildcard='*.bin')

    def OnButtonFlashCalibrationFilesButton(self, event):
        if self.libversion < 7.8:
            PopUpError("Invalid Updater DLL version.\nFound %s where required is at least 7.8" % libversion)
        else:
            ifile = self.comboBoxCalibrationFiles.GetValue()
            if not ifile:
                print 'ERROR, you must select a valid calibration source.'
            else:
                if os.path.isfile(ifile) and ifile.endswith('bin'):
                    print 'Will use %s to build and program calibration files' % ifile
                    print '2 versions of the file will be stored in file system.'
                    try:
                        if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                            self._devLog.MonitorFlashing(self.comboBoxAdbApIfDevices.GetValue())
                        MainFrameThreads(self, RistrettoCommon.PROGRAM_CALIB, args=ifile, action_button=self.buttonFlashCalibrationFiles)

                    except Exception:
                        PrintException()

                    finally:
                        self.UpdateSettings("calibItems", ifile)
                else:
                    print '%s NOT a valid file OR is a directory.' % ifile

    ############################################################################
    #                                                                          #
    # DEBUG TAB                                                                #
    #                                                                          #
    ############################################################################
    # CRASH INFO
    def _initCrashInfoData(self):
        self.crashInfoDecoded = True
        self.crashInfoDir = os.path.join(os.getcwd(), 'Dumps')
        if os.path.isdir(self.crashInfoDir) == False:
            os.mkdir(self.crashInfoDir)
        crash_infos=['CRASH_INFO','CRASH_DUMP', 'RAM_DUMP', 'CLEAR_HISTORY', 'DECODE_COREDUMP']
        if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
            crash_infos.remove('CRASH_INFO')
            crash_infos.remove('CRASH_DUMP')
            crash_infos.remove('RAM_DUMP')
            crash_infos.remove('DECODE_COREDUMP')
            crash_infos.insert(0,'FULL_COREDUMP')
            crash_infos.insert(0,'MINI_COREDUMP')
            self.checkBoxCrashInfo.Hide()
            self.crashInfoDecoded = False
            self.staticTextLogFile.Hide()
            self.buttonCrashInfoBrowse.Hide()
            self.comboBoxCrashInfoLogPath.Hide()
        for info in crash_infos:
            self.choiceCrashInfo.Append(info)
        self.comboBoxLogFolder.SetLabel(self.crashInfoDir)

    def OnButtonCrashInfoButton(self, event):
        error = 0
        action = self.choiceCrashInfo.GetStringSelection()
        try:
            dir = self.comboBoxLogFolder.GetValue()
            if dir:
                # Update self.crashInfoDir
                if os.path.isdir(dir):
                    self.crashInfoDir = dir
                if os.path.isfile(dir):
                    self.crashInfoDir = os.path.dirname(dir)

            if action:
                if action == 'CRASH_INFO':
                    MainFrameThreads(self, RistrettoCommon.DISPLAY_CRASHINFO, action_button=self.buttonCrashInfo)

                elif action == 'MINI_COREDUMP' or action == 'FULL_COREDUMP' or action == 'CRASH_DUMP':
                    print ('\nCoredump will be stored in: %s\n' % self.crashInfoDir)
                    if action == 'MINI_COREDUMP':
                        print ('Retreive mini coredump...')
                        MainFrameThreads(self, RistrettoCommon.BUILD_COREDUMP, args=['MINI', self.crashInfoDir, self.crashInfoDecoded], action_button=self.buttonCrashInfo)
                    elif action == 'FULL_COREDUMP':
                        print ('Retreive full coredump...')
                        MainFrameThreads(self, RistrettoCommon.BUILD_COREDUMP, args=['FULL', self.crashInfoDir, self.crashInfoDecoded], action_button=self.buttonCrashInfo)
                    else:
                        print ('Retreive coredump...')
                        MainFrameThreads(self, RistrettoCommon.BUILD_COREDUMP, args=['DUMP', self.crashInfoDir, self.crashInfoDecoded], action_button=self.buttonCrashInfo)

                elif action == 'CLEAR_HISTORY':
                    MainFrameThreads(self, RistrettoCommon.CLEAR_CRASHINFO, action_button=self.buttonCrashInfo)

                elif action == 'DECODE_COREDUMP':
                    ifile = self.comboBoxCrashInfoLogPath.GetValue()
                    if ifile:
                        MainFrameThreads(self, RistrettoCommon.DECODE_COREDUMP, args=ifile, action_button=self.buttonCrashInfo, always=True, com_usage=False)
                    else:
                        error = 1
                        print 'ERROR: Please indicate a file to decode'
                        
                elif action == 'RAM_DUMP':
                    print ('Retreive mini coredump...')
                    MainFrameThreads(self, RistrettoCommon.BUILD_COREDUMP, args=['RAM', self.crashInfoDir], action_button=self.buttonCrashInfo)


                else:
                    error = 1
                    print 'ERROR: Unknown action. Please select a valid one.'
            else:
                error = 1
                print 'ERROR: Please select a valid action.'

        except Exception:
            error = 1
            PrintException()

        finally:
            if not error:
                if action == 'DECODE_COREDUMP':
                    self.UpdateSettings("crashInfoItems", ifile)
                if action == 'MINI_COREDUMP' or action == 'FULL_COREDUMP' or action == 'RAM_DUMP':
                    self.UpdateSettings("crashInfoFolderItems", self.crashInfoDir)

    def OnChoiceCrashInfoChoice(self, event):
        action = self.choiceCrashInfo.GetStringSelection()
        if action == 'DECODE_COREDUMP':
            if self.currentAction != RistrettoCommon.DECODE_COREDUMP:
                self.buttonCrashInfo.Enable()
            self.buttonCrashInfoBrowse.Enable()
            self.comboBoxCrashInfoLogPath.Enable()
        else:
            self.buttonCrashInfoBrowse.Disable()
            self.comboBoxCrashInfoLogPath.Disable()
            if self.conn.autoSelect == True:
                if self.conn.detected == 0:
                    # No platform connected on USB...
                    self.buttonCrashInfo.Disable()
        if action == 'MINI_COREDUMP' or action == 'FULL_COREDUMP':
            if self.currentAction != RistrettoCommon.BUILD_COREDUMP:
                self.checkBoxCrashInfo.Enable()
        else:
            self.checkBoxCrashInfo.Disable()

    def OnCheckBoxCrashInfoCheckbox(self, event):
        if self.checkBoxCrashInfo.GetValue() == True:
            self.crashInfoDecoded = False
        else:
            self.crashInfoDecoded = True

    def OnButtonCrashInfoBrowseButton(self, event):
        self.BrowseFileForCombo(self.comboBoxCrashInfoLogPath, msg='Indicate log dump to decode', wildcard='log (*.log)|*.log| All files (*.*)|*.*')

    def OnButtonBrowseLogFolderButton(self, event):
        self.BrowseDirForCombo(self.comboBoxLogFolder, msg='Indicate folder to store log dump', title='Coredump folder.')

    # PLATFORM INFO
    def _initPlatInfoData(self):
        plat_info=['LIST_FILE_SYSTEM', 'FIRMWARE_INFOS', 'GET_FLASH_DUMP', 'DECODE_FLASH_DUMP', 'EXTRACT_FILES']
        if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
            plat_info.remove('EXTRACT_FILES')
        elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
            plat_info.remove('GET_FLASH_DUMP')
            plat_info.remove('DECODE_FLASH_DUMP')
        for info in plat_info:
            self.choicePlatInfo.Append(info)

    def OnChoicePlatInfoChoice(self, event):
        action = self.choicePlatInfo.GetStringSelection()
        if action == 'DECODE_FLASH_DUMP':
            if self.currentAction != RistrettoCommon.DECODE_MEMORY_DUMP:
                self.buttonStartPlatInfo.Enable()
        else:
            if self.conn.autoSelect == True:
                if self.conn.detected == 0:
                    # No platform connected on USB...
                    self.buttonStartPlatInfo.Disable()

    def OnButtonStartPlatInfoButton(self, event):
        try:
            action = self.choicePlatInfo.GetStringSelection()
            if action == 'LIST_FILE_SYSTEM':
                MainFrameThreads(self, RistrettoCommon.LIST_FILESYSTEM, action_button=self.buttonStartPlatInfo)
            elif action == 'FIRMWARE_INFOS':
                MainFrameThreads(self, RistrettoCommon.DISPLAY_PLATINFO, action_button=self.buttonStartPlatInfo)
            elif action == 'EXTRACT_FILES':
                folder=self.BrowseForDir(msg='Indicate where to store extracted files...')
                if not folder:
                    print 'ERROR: no valid folder indicated for platform files storage'
                else:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        MainFrameThreads(self, RistrettoCommon.ADB, args=['EXTRACT_FILES', folder], action_button=self.buttonStartPlatInfo)
                    else:
                        print 'ERROR: this action is not supported...'
            elif action == 'GET_FLASH_DUMP':
                if self.gangimagedir:
                    dir = self.gangimagedir
                else:
                    dir = self.defaultDir
                gangimagefile = self.BrowseForFile(msg='Indicate a file name to store encoded flash image...', wildcard='*', defaultDir=dir)
                if gangimagefile != None:
                    self.gangimagedir = os.path.dirname(gangimagefile)
                    print 'Encoded flash memory dump will be stored in %s' % gangimagefile
                    MainFrameThreads(self, RistrettoCommon.GET_MEMORY_DUMP, args=gangimagefile, action_button=self.buttonStartPlatInfo)
                    self.settings["gangimagedir"] = self.gangimagedir
                else:
                    print 'Memory dump aborted: no valid file indicated'
            elif action == 'DECODE_FLASH_DUMP':
                if self.gangimagedir:
                    dir = self.gangimagedir
                else:
                    dir = self.defaultDir
                gangimagefile = self.BrowseForFile(msg='Indicate encoded flash image...', wildcard='*', defaultDir=dir)
                if gangimagefile != None:
                    print u'{0} will be decoded in {1}\n'.format(gangimagefile, os.path.join(os.path.dirname(gangimagefile),'mem_dump.bin'))
                    MainFrameThreads(self, RistrettoCommon.DECODE_MEMORY_DUMP, args=gangimagefile, always=True, com_usage=False, action_button=self.buttonStartPlatInfo)
                else:
                    print 'Memory dump decoding aborted: no valid file indicated'
            else:
                print 'ERROR. Please select a valid action.'

        except Exception:
            PrintException()

    # FILE(s) INFO
    def _createArchInfoDialog(self):
        return ArchInfoDialog.create(self)

    def _displayArchInfo(self):
        self.ArchInfoDlg = self._dispDlgFrame(self.ArchInfoDlg, self._createArchInfoDialog)

    def OnButtonBrowseFirmwareInfoButton(self, event):
        self.BrowseFileForCombo(self.comboBoxFirmwareInfo, msg='Select File to check...')

    def OnButtonBrowseDirFirmwareInfoButton(self, event):
        self.BrowseDirForCombo(self.comboBoxFirmwareInfo, msg='Choose directory to check:', title='Directory Check')

    def OnButtonGetFirmwareInfoButton(self, event):
        extract_folder = None
        info = self.comboBoxFirmwareInfo.GetValue()
        infoIsDir = False
        try:
            if info:
                if (os.path.isdir(info) == 0): # it is a file.
                    if info.endswith('.zip') or info.endswith('.tgz') or info.endswith('.tar.gz') or info.endswith('.ipkg') :
                        extract_folder = self.platform.ExtractArchive(os.path.realpath(os.path.join(IceraToolbox.BASE_PATH,'InfoTmp')), info)
                        if extract_folder != None:
                            info = extract_folder
                            infoIsDir = True
                else:
                    infoIsDir = True

                self._displayArchInfo()
                MainFrameThreads(self, RistrettoCommon.GET_ARCH_INFO, args=(info, infoIsDir, self.ArchInfoDlg.UpdateDisplay), action_button=self.buttonGetFirmwareInfo, always=True, com_usage=False)
            else:
                print 'No file to check...'

        except Exception:
            PrintException()

        finally:
            if info:
                self.UpdateSettings("fileInfoItems", self.comboBoxFirmwareInfo.GetValue())

    # AT CMDs
    def _sendAtCommand(self, cmd):
        err=0
        socket=None
        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                err, port, socket = self._getAdbForwardInfos()
                if err or 'tcp:' not in socket:
                    err = 1
                    print 'ERROR: Cannot communicate with board if ADB port is not forwarded (see ADB interface tab).\n'
            if not err:
                MainFrameThreads(self, RistrettoCommon.LAUNCH_AT_CMD, args=[cmd, socket])

        except Exception:
            PrintException()

    def OnComboBoxAtCommandsTextEnter(self, event):
        at_cmd = self.comboBoxAtCommands.GetValue()
        try:
            self._sendAtCommand(at_cmd)

        except Exception:
            PrintException()

        finally:
            if at_cmd not in self.comboBoxAtCommands.GetItems():
                self.comboBoxAtCommands.Append(at_cmd)
            self.UpdateSettings("atCmdItems", at_cmd, number=20)

    ############################################################################
    #                                                                          #
    # HOST INTERFACE TAB                                                       #
    #                                                                          #
    ############################################################################
    # CONNECTION
    def _disableComPortSelection(self):
        self.staticTextSelectPort.Disable()
        self.comboBoxComPort.Disable()
        self._disableComPortSettings()

    def _enableComPortSelection(self):
        self.staticTextSelectPort.Enable()
        self.comboBoxComPort.Enable()
        self._enableComPortSettings()

    def _disableAdbDeviceSelection(self):
        self.comboBoxAdbApIfDevices.Disable()
        self.staticTextAdbApIfDevices.Disable()

    def _enableAdbDeviceSelection(self):
        self.comboBoxAdbApIfDevices.Enable()
        self.staticTextAdbApIfDevices.Enable()

    def _updateAutoDetect(self, activated):
        if activated:
            self._disableComPortSelection()
            self._disableAdbDeviceSelection()
            self.conn.autoSelect = True
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                self.log.DisplayConnectStatus('COM port auto-detect enabled')
            elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                self.log.DisplayConnectStatus('ADB device(s) auto-detect enabled')
            self._disableActions() # re-enabled or not with _updateConnectionStatus...
            self.conn.Scan() # force re-scan when enable autodetect is ticked manually
            self._updateConnectionStatus()
        else:
            self._updateConnectionStatus()
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                current_port = self.comboBoxComPort.GetValue()
                if current_port in self.portList or "tcp:" in current_port:
                    self.log.DisplayConnectStatus("Connected on %s" % current_port)
                    if current_port == 'MBIM':
                            self.comboBoxCOMBlockSize.SetLabel(str(4000))
                            self.conn.UpdateBlockSize(4000)
                else:
                    self.log.DisplayConnectStatus("No valid COM port selected")
            self._enableActions(None)
            self._enableComPortSelection()
            self._enableAdbDeviceSelection()
            self.conn.autoSelect = False

    def _getComPortValue(self):
        self.ComPort = str(self.comboBoxComPort.GetValue())
        self.log.DisplayConnectStatus("Connected on %s" % self.ComPort)
        if self.ComPort == 'MBIM':
            self.comboBoxCOMBlockSize.SetLabel(str(4000))
            self.conn.UpdateBlockSize(4000)

    def OnCheckBoxAutoDetectCheckbox(self, event):
        self._updateAutoDetect(self.checkBoxAutoDetect.GetValue())

    def OnComboBoxComPortCombobox(self, event):
        self._getComPortValue()

    def OnComboBoxComPortText(self, event):
        self._getComPortValue()

    def OnCheckBoxFlowControlCheckbox(self, event):
        if self.checkBoxFlowControl.GetValue() == True:
            self.conn.flowControl = 0
        else:
            self.conn.flowControl = 1

    # SETTINGS
    def OnChoiceHifBaudrateChoice(self, event):
        self.conn.baudrate = eval(self.choiceHifBaudrate.GetStringSelection())

    def OnComboBoxCOMBlockSizeCombobox(self, event):
        self.conn.UpdateBlockSize(eval(self.comboBoxCOMBlockSize.GetValue()))

    def OnComboBoxCOMBlockSizeText(self, event):
        self.conn.UpdateBlockSize(eval(self.comboBoxCOMBlockSize.GetValue()))

    # HIF
    def OnRadioButtonUsbHifRadiobutton(self, event):
        if self.radioButtonUsbHif.GetValue() == True:
            self.conn.hifType = RistrettoCommon.HIF_USB

    def OnRadioButtonUartHifRadiobutton(self, event):
        if self.radioButtonUartHif.GetValue() == True:
            self.conn.hifType = RistrettoCommon.HIF_UART

    def OnButtonApplyHifSwitchButton(self, event):
        MainFrameThreads(self, RistrettoCommon.SET_HIF_TYPE, action_button=self.buttonApplyHifSwitch)

    def OnTxtCtrlConsoleTextEnter(self, event):
        if self.consoleEditable == True:
            self.txtCtrlConsole.SetInsertionPointEnd()
            cmd = self.stringToGetVal
            self.stringToGetVal = ''
            if 'closelib' in cmd.lower():
                self.platform.LibClose()
            if 'openlib' in cmd.lower():
                self.platform.LibOpen()
            if 'at' in cmd.lower():
                self._sendAtCommand(cmd)
            if cmd.lower() == 'clear':
                self.txtCtrlConsole.Clear()

    def OnTxtCtrlConsoleChar(self, event):
        event.Skip()
        if self.consoleEditable == True:
            if len(self.stringToGetVal):
                if event.GetKeyCode() < 32:
                    # upper is a valid char in ascii table...: definitely not bug free...
                    if event.GetKeyCode() == 8:
                        # backspace
                        self.stringToGetVal = self.stringToGetVal[:len(self.stringToGetVal)-1]
                    return
            if (event.GetKeyCode() >= 312) and (event.GetKeyCode() <= 317):
                # keyboard arrows + end & home...
                return

            # always continue to type at the end of the editing line...
            self.txtCtrlConsole.SetInsertionPointEnd()
            # append char to current string cmd since next 'Enter' event
            self.stringToGetVal = self.stringToGetVal + chr(event.GetKeyCode())

    # UART Discovery
    def OnComboBoxUartDiscoverySelectPortCombobox(self, event):
        '''
        Select UART COM port to use in available list.
        '''
        self.uartDiscoveryComPort = self.comboBoxUartDiscoverySelectPort.GetValue()
        self.log.DisplayConnectStatus("%s selected  for UART discovery" % self.uartDiscoveryComPort)

    def OnComboBoxUartDiscoverySelectPortText(self, event):
        '''
        Indicate manually UART COM port to use.
        '''
        self.uartDiscoveryComPort = str(self.comboBoxUartDiscoverySelectPort.GetValue())
        self.log.DisplayConnectStatus("%s selected  for UART discovery" % self.uartDiscoveryComPort)

    def OnButtonUartDiscoveryStartServerButton(self, event):
        if self.libversion < 8.00:
            PopUpError("Invalid Updater DLL version.\nFound %s where required is at least 8.00" % libversion)
        else:
            try:
                if self.uartDiscoveryComPort == None:
                    print 'ERROR. Please select a valid COM port.'
                else:
                    MainFrameThreads(self, RistrettoCommon.START_UART_SERVER, args=['DISCOVERY', self.uartDiscoveryComPort], action_button=self.buttonUartDiscoveryStartServer, always=True, com_usage=False)

            except Exception:
                PrintException()

    def OnButtonUartDiscoveryStopServerButton(self, event):
        MainFrameThreads(self, RistrettoCommon.STOP_UART_SERVER, args=['DISCOVERY', self.uartDiscoveryComPort], action_button=self.buttonUartDiscoveryStopServer, always=True, com_usage=False)

    def OnNotebookNotebookPageChanged(self, event):
        if event.GetSelection() == RistrettoCommon.DEBUG_PAGE_NUMBER: # debug tab selected...
            # Set Console with R/W access
            self.txtCtrlConsole.SetEditable(1)
            self.consoleEditable = True
        else:
            # Set Console with RO access
            self.txtCtrlConsole.SetEditable(0)
            self.consoleEditable = False
        event.Skip()

    #####################################
    #                                   #
    # Boot and Board Repair Tab         #
    #                                   #
    #####################################
    def OnNotebookBoardRepairNotebookPageChanged(self, event):
        if event.GetSelection() == 1: # repair agent tab selected
            self.boardRepairFactory = True
            self.boardRepairDebug = False
            if self.dbgBoardRepairStarted:
                self.buttonStopBoardRepair.Disable()
            else:
                self.buttonStopBoardRepair.Enable()
        if event.GetSelection() == 0: # boot agent tab selected
            self.boardRepairFactory = False
            self.boardRepairDebug = True
            if self.factBoardRepairStarted:
                self.buttonStopBoardRepair.Disable()
            else:
                self.buttonStopBoardRepair.Enable()
        event.Skip()

    ### Repair Agent Sub tab:
    def OnButtonFactReleaseUpdateButton(self, event):
        self.BrowseDirForCombo(self.comboBoxFactReleaseUpdate, msg='Select Release Package:', title='Factory Release Package')

    def OnButtonFactBrowseArchiveButton(self, event):
        self.BrowseFileForCombo(self.comboBoxFactReleaseUpdate, msg='Select Release Archive...', wildcard='*.zip;*.tar.gz;*.tgz;*.ipkg')

    def _disableFactFileListButtons(self):
        try:
            self.checkBoxFactReleaseUpdateListMDM.SetValue(True)
            self.checkBoxFactReleaseUpdateListMDM.Disable()

            self.checkBoxFactUpdateReleaseListCALIB.SetValue(True)
            self.checkBoxFactUpdateReleaseListCALIB.Disable()

            self.checkBoxFactReleaseUpdateListDEVICECFG.SetValue(True)
            self.checkBoxFactReleaseUpdateListDEVICECFG.Disable()

            self.checkBoxFactReleaseUpdateListPRODUCTCFG.SetValue(True)
            self.checkBoxFactReleaseUpdateListPRODUCTCFG.Disable()

        except Exception:
            PrintException()

    def _enableAllFactFileListButtons(self):
        try:
            self.checkBoxFactReleaseUpdateListMDM.SetValue(False)
            self.checkBoxFactReleaseUpdateListMDM.Enable()

            self.checkBoxFactUpdateReleaseListCALIB.SetValue(False)
            self.checkBoxFactUpdateReleaseListCALIB.Enable()

            self.checkBoxFactReleaseUpdateListDEVICECFG.SetValue(False)
            self.checkBoxFactReleaseUpdateListDEVICECFG.Enable()

            self.checkBoxFactReleaseUpdateListPRODUCTCFG.SetValue(False)
            self.checkBoxFactReleaseUpdateListPRODUCTCFG.Enable()

        except Exception:
            PrintException()

    def OnCheckBoxFactReleaseListAllCheckbox(self, event):
        if self.checkBoxFactReleaseListAll.GetValue() == True:
            self._disableFactFileListButtons()
        else:
            self._enableAllFactFileListButtons()

    def _getFactReleaseFiles(self):
        factReleaseFiles = {}
        factReleaseFiles["BT2"] = True
        factReleaseFiles["LDR"] = True
        factReleaseFiles["PLATCFG"] = True
        factReleaseFiles["MASS"] = False
        factReleaseFiles["IFT"] = False
        factReleaseFiles["MDM"] = self.checkBoxFactReleaseUpdateListMDM.GetValue()
        factReleaseFiles["ZEROCD"] = False
        factReleaseFiles["CALIB"] = self.checkBoxFactUpdateReleaseListCALIB.GetValue()
        factReleaseFiles["DEVICECFG"] = self.checkBoxFactReleaseUpdateListDEVICECFG.GetValue()
        factReleaseFiles["PRODUCTCFG"] = self.checkBoxFactReleaseUpdateListPRODUCTCFG.GetValue()
        return factReleaseFiles

    def _boardRepairFactStart(self):
        '''
        Start factory board repair process
        '''
        self.factBoardRepairStarted = True
        err = 0

        try:
            package_path = self.comboBoxFactReleaseUpdate.GetValue()
            if not package_path:
                print 'ERROR: PLEASE INDICATE A VALID FACTORY RELEASE FOLDER.\n'
                err = 1
            else:
                if package_path.endswith('.zip') or package_path.endswith('.tgz') or package_path.endswith('.tar.gz') or package_path.endswith('.ipkg'):
                    package_path = self.platform.ExtractArchive(self.extract_folder, package_path)
                    if package_path == None:
                        print 'ERROR: not possible to deflate archive correctly.\n'
                        err = 1

                if self.uartBoardRepairComPort == None:
                    print 'ERROR: PLEASE SELECT A VALID COM PORT.'
                    err = 1

                if err == 0:
                    factReleaseFiles = self._getFactReleaseFiles()
                    MainFrameThreads(self, RistrettoCommon.START_FACTORY_BOARD_REPAIR, args=[package_path, factReleaseFiles, self.uartBoardRepairComPort, self.gaugeFactStatus, self.fullFlashFormat], action_button=self.buttonStartBoardRepair)

        except Exception:
            err = 1
            PrintException()

        finally:
            if package_path:
                self.UpdateSettings("packageBoardRepairIitems", self.comboBoxFactReleaseUpdate.GetValue())
            if err:
                self.factBoardRepairStarted = False

    def _boardRepairFactStop(self):
        '''
        Stop factory board repair process
        '''
        try:
            MainFrameThreads(self, RistrettoCommon.STOP_FACTORY_BOARD_REPAIR, args=[self.uartBoardRepairComPort], action_button=self.buttonStopBoardRepair)

        except Exception:
            PrintException()

        finally:
            self.factBoardRepairStarted = False

    ### Boot Agent Sub tab:
    def OnButtonDbgBrowseUartBT2Button(self, event):
        self.BrowseFileForCombo(self.comboBoxUartBT2, msg='Select BT2 to program...', wildcard='*.wrapped')

    def OnButtonDbgBrowseUartAppliButton(self, event):
        self.BrowseFileForCombo(self.comboBoxUartAppli, msg='Select APP to program...', wildcard='*.wrapped')

    def OnChoiceBromComBaudrateChoice(self, event):
        self.conn.UpdateBromBaudrate(eval(self.choiceBromComBaudrate.GetStringSelection()))

    def OnChoiceAppComBaudrateChoice(self, event):
        self.conn.UpdateAppBaudrate(self.choiceAppComBaudrate.GetStringSelection())

    def _boardRepairDbgStartServer(self):
        '''
        Start UART server for debug...
        '''
        missing = ''
        err = 0
        self.dbgBoardRepairStarted = True

        try:
            bt2ToSend = self.comboBoxUartBT2.GetValue()
            appToSend = self.comboBoxUartAppli.GetValue()
            if not bt2ToSend:
                missing = missing + '\n - indicate a valid secondary_boot '
            if not appToSend:
                missing  = missing + '\n - indicate a valid application'
            if self.uartBoardRepairComPort == None:
                missing = missing + '\n - indicate a valid COM port'
            if missing != '':
                print 'ERROR: Some information is missing: %s\n' % missing
                err = 1
            else:
                if (os.path.isfile(bt2ToSend) == 0):
                    print 'ERROR: %s NOT A VALID FILE.\n' % bt2ToSend
                    err = 1
                if (os.path.isfile(appToSend) == 0):
                    print 'ERROR: %s NOT A VALID FILE.\n' % appToSend
                    err = 1

                if err == 0:
                    MainFrameThreads(self, RistrettoCommon.START_UART_SERVER, args=['BOARD_REPAIR', bt2ToSend, appToSend, self.uartBoardRepairComPort, self.gaugeFactStatus], action_button=self.buttonStartBoardRepair, always=True, com_usage=False)

        except Exception:
            err = 1
            PrintException()

        finally:
            if bt2ToSend:
                self.UpdateSettings("bt2BoardRepairItems", bt2ToSend)
            if appToSend:
                self.UpdateSettings("appliBoardRepairIitems", appToSend)
            if err:
                self.dbgBoardRepairStarted = False

    def _boardRepairDbgStopServer(self):
        '''
        Stop UART server.
        '''
        try:
            MainFrameThreads(self, RistrettoCommon.STOP_UART_SERVER, args=['BOARD_REPAIR', self.uartBoardRepairComPort], action_button=self.buttonStopBoardRepair, always=True, com_usage=False)

        except Exception:
            PrintException()

        finally:
            self.dbgBoardRepairStarted = False

    ### Common items:
    def OnCheckBoxFlashFormatCheckbox(self, event):
        if self.checkBoxFlashFormat.GetValue() == True:
            self.fullFlashFormat = True
        else:
            self.fullFlashFormat = False

    def OnComboBoxFactUartServerText(self, event):
        '''
        When indicating manually a COM port to use
        '''
        self.uartBoardRepairComPort = str(self.comboBoxFactUartServer.GetValue())
        self.log.DisplayConnectStatus("%s selected  for UART board repair" % self.uartBoardRepairComPort)

    def OnComboBoxFactUartServerCombobox(self, event):
        '''
        When selecting a valid UART COM port in the combo box available list
        '''
        self.uartBoardRepairComPort = self.comboBoxFactUartServer.GetValue()
        self.log.DisplayConnectStatus("%s selected  for UART board repair" % self.uartBoardRepairComPort)

    def OnButtonBoardRepairStartButton(self,event):
        if self.boardRepairFactory:
            self._boardRepairFactStart()
        if self.boardRepairDebug:
            self._boardRepairDbgStartServer()

    def OnButtonBoardRepairStopButton(self, event):
        try:
            if self.boardRepairFactory:
                self._boardRepairFactStop()
            if self.boardRepairDebug:
                self._boardRepairDbgStopServer()
        except Exception:
            PrintException()
        finally:
            self.gaugeFactStatus.SetValue(0)

    #####################################
    #                                   #
    # ADB interface tab                 #
    #                                   #
    #####################################
    def _initProperties(self):
        props=[#FILD
        'modem.fild.coredump',
        'modem.fild.coredumpdir',
        'modem.fild.baudrate',
        'modem.fild.blocksize',
        'modem.fild.dbgblocksize',
        'modem.fild.maxcoredump',
        'modem.fild.maxcrashdump',
        #RIL
        'ro.ril.devicename',
        'rild.libpath',
        'rild.libargs',
        #MODEM
        'modem.power.device',
        'modem.powercontrol',
        'modem.power.usbdevice'
        ]
        for prop in props:
            if prop not in self.comboBoxAdbApIfSystemProperties.GetItems():
                self.comboBoxAdbApIfSystemProperties.Append(prop)

    def _initAdbActions(self):
        adb_actions=['STOP_RIL', 'START_RIL', 'RESTART_RIL', 'STOP_FIL', 'START_FIL', 'RESTART_FIL', 'REBOOT', 'REMOUNT_FS', 'SET_ROOT']
        for action in adb_actions:
            self.choiceAdbApIfActions.Append(action)

    def _getAdbDeviceValue(self):
        self.AdbDevice = str(self.comboBoxAdbApIfDevices.GetValue())
        if self.platform.conn.IsSingleFlash():
            print 'INFO: {0} detected as a single flash ADB device\n'.format(self.conn.devices[0])
            self._reEnableActions()
            self.buttonUnlock.SetLabel("Get module lock state\n")
            self.buttonUnlock.Enable(True)
            if self.initialised:
                self._deInitPortForwarding()
        else:
            print 'INFO: {0} detected as a dual flash ADB device'.format(self.conn.devices[0])
            if self.conn.forwarded:
                self._reEnableActions()
            else:
                print 'INFO: You may need to perform a port forwarding to communicate with the platform.'
                if self.initialised and self.conn.autoSelect == True:
                    self._initPortForwarding()
                else:
                    self.comboBoxAdbApIfForward.SetLabel(self.defaultSerialPort)
                    self.comboBoxAdbApIfForward.SetValue(self.defaultSerialPort)
                    self.comboBoxAdbApIfForwardSocket.SetLabel(self.defaultSerialSocket)
                    self.comboBoxAdbApIfForwardSocket.SetValue(self.defaultSerialSocket)
                    self.buttonAdbApIfForward.Enable()
            self.checkBoxUpdateEnableCbc.SetValue(False)
            self.checkBoxUpdateEnableCbc.Disable()
            self.checkBoxUpdateEnableKrm.SetValue(False)
            self.checkBoxUpdateEnableKrm.Disable()
            self.checkBoxBT3.SetValue(False)
            self.checkBoxBT3.Disable()
            self.checkBoxLDR.SetValue(True)
            self.platform.UpdateCbcValue(self.checkBoxUpdateEnableCbc.GetValue())
            self.platform.UpdateKrmValue(self.checkBoxUpdateEnableKrm.GetValue())

    def _getAdbForwardInfos(self):
        err=0
        port=''
        socket=''
        try:
            port=str(self.comboBoxAdbApIfForward.GetValue())
            if not port:
                print 'ERROR: Please indicate a port to forward'
                err=1
            else:
                socket=str(self.comboBoxAdbApIfForwardSocket.GetValue())
                if not socket:
                    print 'ERROR: Please indicate a socket for port forwarding'
                    err=1
        except Exception:
            PrintException()
            err=1
        finally:
            return err, port, socket

    def OnCheckBoxAdbApIfConnectionCheckbox(self, event):
        self._updateAutoDetect(self.checkBoxAdbApIfConnection.GetValue())

    def OnComboBoxAdbApIfDevicesCombobox(self, event):
        self._getAdbDeviceValue()

    def OnButtonAdbApIfScanButton(self, event):
        MainFrameThreads(self, RistrettoCommon.SCAN_TARGET, com_usage=False)

    def OnButtonAdbApIfForwardButton(self, event):
        err=0
        try:
            err, port, socket =self._getAdbForwardInfos()
            if not err:
                forwardThread=MainFrameThreads(self, RistrettoCommon.ADB, args=['FORWARD', port, socket], action_button=self.buttonAdbApIfForward, thread=False)
                if forwardThread.err==0:
                    if self.platform.allowUnlock:
                        checkLockThread=MainFrameThreads(self, RistrettoCommon.CHECK_LOCK_TYPE, thread=False)
                        if checkLockThread.rsp == 'production':
                            m=MainFrameThreads(self, RistrettoCommon.CHECK_PCID, thread=False)
                            self.pcid_to_unlock=m.rsp
                            if self.pcid_to_unlock:
                                self.buttonUnlock.Enable(True)
                                self.buttonUnlock.SetLabel(u'Download/Flash certificate\nChip version: {0}'.format(checkLockThread.rsp))
                            else:
                                self.buttonUnlock.Enable(False)
                                self.buttonUnlock.SetLabel(u'Fail to retreive PCID\nChip version: {0}'.format(checkLockThread.rsp))
                        else:
                            self.buttonUnlock.Enable(False)
                            self.buttonUnlock.SetLabel(u'Board unlocked\nChip version: {0}'.format(checkLockThread.rsp))
                else:
                    print "Fail to forward modem port {0} to {1}".format(port, socket)

        except Exception:
            PrintException()
            err=1
        finally:
            self.UpdateSettings("portForwardItems", self.comboBoxAdbApIfForward.GetValue())
            if self.comboBoxAdbApIfForward.GetValue() not in self.comboBoxAdbApIfForward.GetItems():
                self.comboBoxAdbApIfForward.Append(self.comboBoxAdbApIfForward.GetValue())
            self.UpdateSettings("socketForwardItems", self.comboBoxAdbApIfForwardSocket.GetValue())
            if self.comboBoxAdbApIfForwardSocket.GetValue() not in self.comboBoxAdbApIfForwardSocket.GetItems():
                self.comboBoxAdbApIfForwardSocket.Append(self.comboBoxAdbApIfForwardSocket.GetValue())

    def OnButtonAdbApIfSystemPropertiesSetButton(self, event):
        try:
            prop=self.comboBoxAdbApIfSystemProperties.GetValue()
            if not prop:
                print 'ERROR: Please select a system property to SET'
            else:
                value=self.comboBoxAdbApIfSystemPropertiesValue.GetValue()
                if not value:
                    print 'ERROR: Please select a value for property {0}'.format(prop)
                else:
                    MainFrameThreads(self, RistrettoCommon.ADB, args=['SETPROP', prop,value], action_button=self.buttonAdbApIfSystemPropertiesSet)
        except Exception:
            PrintException()
        finally:
            self.UpdateSettings("sysPropertyItems", self.comboBoxAdbApIfSystemProperties.GetValue())
            if self.comboBoxAdbApIfSystemProperties.GetValue() not in self.comboBoxAdbApIfSystemProperties.GetItems():
                self.comboBoxAdbApIfSystemProperties.Append(self.comboBoxAdbApIfSystemProperties.GetValue())
            self.UpdateSettings("sysPropertyValueItems", self.comboBoxAdbApIfSystemPropertiesValue.GetValue())
            if self.comboBoxAdbApIfSystemPropertiesValue.GetValue() not in self.comboBoxAdbApIfSystemPropertiesValue.GetItems():
                self.comboBoxAdbApIfSystemPropertiesValue.Append(self.comboBoxAdbApIfSystemPropertiesValue.GetValue())

    def OnButtonAdbApIfSystemPropertiesGetButton(self, event):
        try:
            prop=self.comboBoxAdbApIfSystemProperties.GetValue()
            if not prop:
                print 'ERROR: Please select a system property to GET'
            else:
                MainFrameThreads(self, RistrettoCommon.ADB, args=['GETPROP', prop], action_button=self.buttonAdbApIfSystemPropertiesGet)
        except Exception:
            PrintException()
        finally:
            self.UpdateSettings("sysPropertyItems", self.comboBoxAdbApIfSystemProperties.GetValue())
            if self.comboBoxAdbApIfSystemProperties.GetValue() not in self.comboBoxAdbApIfSystemProperties.GetItems():
                self.comboBoxAdbApIfSystemProperties.Append(self.comboBoxAdbApIfSystemProperties.GetValue())

    def OnButtonAdbApIfActionsStartButton(self, event):
        action=self.choiceAdbApIfActions.GetStringSelection()
        if not action:
            print 'ERROR: Please select an action to start...'
        else:
            MainFrameThreads(self, RistrettoCommon.ADB, args=[action], action_button=self.buttonAdbApIfActionsStart)

    def OnButtonUnlockButton(self, event):
        if self.buttonUnlock.GetLabel() == 'Get module lock state\n':
            self._initPortForwarding()
        elif self.pcid_to_unlock != None:
            err=0
            self.buttonUnlock.Enable(False)
            
            ifile='unlock_'+str(self.pcid_to_unlock)+'.bin'
            ifile=os.path.abspath(ifile)            
            if not os.path.exists(ifile):
                print "Loading list of pre-existing unlock certificates -- Might take some time"
                err=self.platform.checkUnlockFileOnServer(self.pcid_to_unlock)
            print err
            if err==0:
                try:
                    if (os.path.exists(ifile)):
                        MainFrameThreads(self, RistrettoCommon.FILE_UPDATE, args=ifile, action_button=self.buttonFlashSingle, multi=False)

                except Exception:
                    PrintException()
            
            self.buttonUnlock.Enable(True)


###################################################################
#                                                                 #
# MainFrame Threads Class                                         #
#                                                                 #
# Used to launch specific calls to Platform inside a              #
#  Python Thread: the time platform takes to handle the required  #
#  action, the GUI remains accessible...                          #
#                                                                 #
# Args can be propagated to Platform                              #
# Action & Button information is for Frame internal usage to      #
#  enable/disable the correct features while Thread on going      #
#                                                                 #
#                                                                 #
# TODO: Handling of error returned by Platform thread in          #
#        resultThread...                                          #
#                                                                 #
###################################################################

class MainFrameThreads():
    def __init__(self, aWxFrame, action, args=None, action_button=None, always=False, com_usage=True, thread=True, multi=False):
        if IceraToolbox.IsLinux(): thread=False
        self.err = 0
        self.rsp = None
        self.frame = aWxFrame
        self.platform = self.frame.platform
        self.action = action
        self.button = action_button
        self.handle = None
        self.args = args
        self.gotResult = False
        self.always = always
        self.com_usage = com_usage

        try:
            self.frame.currentAction = self.action
            if self.always:
                # This action can be started independantly of the target state:
                #  only disable the action until it is completed, but other one can be launched
                self.button.Disable()
                self.button.SetBackgroundColour(wx.RED)
            else:
                self.frame._disableActions(event_button=self.button)
                # Indicates a thread is running: used to signal not to enable buttons after a mode
                #  switching for example that causes an update of connection status...:
                self.frame.ongoingThread = True
                if self.action == RistrettoCommon.START_FACTORY_BOARD_REPAIR:
                    self.frame.buttonStopBoardRepair.Enable()

            comport = None
            sock_port = None

            if self.platform.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                # ADB device
                if self.frame.comboBoxAdbApIfDevices.GetValue() != '':
                    # Use this device through ADB forward except for direct ADB actions...
                    if action != RistrettoCommon.ADB:
                        err, port, socket = self.frame._getAdbForwardInfos()
                        if err or 'tcp:' not in socket:
                            if  not self.platform.conn.IsSingleFlash(): 
                                self.err = 1
                                print 'ERROR: Cannot communicate with board if ADB port is not forwarded (see ADB interface tab).\n'
                        else:
                            sock_port = socket
                elif action == RistrettoCommon.FILE_UPDATE:
                    err, port, socket = self.frame._getAdbForwardInfos()
                    if 'tcp:' in socket:
                        sock_port = socket

            if self.com_usage:
                # Set COM port to use. Default is None to indicate
                # platform to use its own available port list if exists.
                # Or it is part from self.args concerning UART stuff...
                if self.platform.conn.autoSelect == False:
                    if self.platform.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                        if self.frame.ComPort:
                            comport = self.frame.ComPort
                        else:
                            print 'ERROR. Please select a valid COM port.'
                            self.err = 1
                    elif self.platform.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        if self.frame.AdbDevice:
                            comport = self.frame.AdbDevice
                        else:
                            print 'ERROR. Please select a valid ADB device.'
                            self.err = 1
                else:
                    if not multi:
                        # This action doesn't support list of devices, even if list is with one element...
                        if self.platform.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                            comport = self.platform.conn.mdmPortList[0]
                        elif self.platform.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                            comport = self.platform.conn.devices[0]

                if self.frame.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    adb=True
                    if not self.frame.conn.adb:
                        adb=False
                    elif not self.frame.conn.adb.path:
                        adb=False
                    if not adb:
                        print 'ERROR. Please select a valid ADB tool.'
                        self.err=1

            if not self.err:
                if thread:
                    # Start Platform Thread and result thread
                    delayedresult.startWorker(self.resultThread, self.platform.CallAction,
                                          wargs=(self.action, comport, sock_port, self.args), jobID=1)
                else:
                    # Start blocking call to platform functionalities
                    self.rsp,self.err=self.platform.CallAction(self.action, comport, sock_port, self.args)

        except Exception:
            self.err = 1
            PrintException()

        finally:
            if self.err or not thread:
                self.updateFrame()

    def resultThread(self, delayedResult):
        self.err = 0
        self.gotResult = True
        try:
            # Wait until Platform thread ends
            self.rsp,self.err = delayedResult.get()
        except Exception:
            PrintException()
            self.err = 1
        finally:
            self.updateFrame()

    def updateFrame(self):
        self.frame.currentAction = None
        if self.always:
            self.button.Enable()
            self.button.SetBackgroundColour(self.frame.OriginalBtnColor)
            if self.action == RistrettoCommon.START_UART_SERVER or self.action == RistrettoCommon.STOP_UART_SERVER:
                if self.action == RistrettoCommon.STOP_UART_SERVER:
                    if self.args[1] == 'BOARD_REPAIR':
                        self.frame.buttonStartBoardRepair.SetBackgroundColour(self.frame.OriginalBtnColor)
                        self.frame.buttonStartBoardRepair.Enable()
                    if self.args[1] == 'DISCOVERY':
                        self.frame.buttonUartDiscoveryStartServer.SetBackgroundColour(self.frame.OriginalBtnColor)
                        self.frame.buttonUartDiscoveryStartServer.Enable()
                if self.action == RistrettoCommon.START_UART_SERVER:
                    if self.args[1] == 'BOARD_REPAIR':
                        self.frame.dbgBoardRepairStarted = False
        else:
            # Indicates that no Thread is running anymore.
            self.frame.ongoingThread = False
            if self.action != RistrettoCommon.SCAN_TARGET:
                # SCAN_TARGET is automatically for enabling/disabling actions
                # regarding SCAN results...
                self.frame._reEnableActions(button=self.button)
            if self.action == RistrettoCommon.START_FACTORY_BOARD_REPAIR:
                self.frame.factBoardRepairStarted = False
            if (self.action == RistrettoCommon.ADB) and (self.args[0] == 'FORWARD'):
                if self.platform.conn.forwarded == True:
                    self.frame._reEnableActions(button=self.button)
