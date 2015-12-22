# -*- coding: utf-8 -*-
import sys, os, traceback, ctypes, wx, time, zipfile, subprocess, re, stat, struct, shutil, gc, urllib2
from threading import Thread
from copy import deepcopy

import RistrettoCommon, RistrettoFrameShare
from RistrettoCommon import PrintException, SearchAndGetFiles, FileExist, NullFunc

import at_debug
from at_memdump import MemDump
from memdump_decoder import MemDumpDecoder
try:
    from download_all import download_all
    from icera_datafile import icera_datafile, readPCID
except:
    # Do not catch exception raised in case ADB tool path is not
    # in env variables...
    pass
import icera_const as const
import IceraAdb, IceraPortDetect, IceraToolbox, espresso_detect, rsa_sign_icera
from unzip import Unzip
from untargz import Untargz
from build_icera_file import BuildIceraFile, DecodeExtendedHeader, ReadBt2ExtendedTrailer, ReadFooter
try:
    import unlock_board
except:
    print "WARNING: unlock_board module not found..."
from atdebug_decoder import AtDebugDecoder
from IceraSingleFlash import IceraSingleFlashAndroid
from IceraDualFlash import IceraDualFlashAndroid

if IceraToolbox.IsWindows():
    import win32api
    import IceraWinSupport
    GUIDS = [ IceraWinSupport.DeviceClassesModemGuid, IceraWinSupport.ClassAndroidUsbGuid, IceraWinSupport.ClassAndroidUsbGuidCust  ]
else:
    GUIDS = ['serial']

COM_HANDLES = []
PRODUCTCFGNAME='productConfig'

WRAPPEDNAMES = {'DEVICECFG':'device_config'
,'PRODUCTCFG':'product_config'
,'AUDIOCFG':'audio_config'
,'LDR':'loader'
,'BT2':'secondary_boot'
,'BT3':'tertiary_boot'
,'IFT':'factory_tests'
,'MDM':'modem'
}

def PrintCb(msg):
    msg.strip('\r')
    msg.strip('\n')
    print msg

def ReadHeader(file, chip=None, cb=None):
    fd = None
    status = 0
    hdr = None
    ext_hdr_bin = None
    zipped = False

    try:
        if os.path.isfile(file):
            fd = open(file, 'rb')
        else:
            msg = 'ERROR. No such file %s' % (file)
            if cb:
                cb(msg)
            else:
                print msg
            status = -1

        if status == 0:
            # Read header:
            hdr_bin = fd.read(const.ARCH_HEADER_BYTE_LEN)
            hdr = struct.unpack("<8L", hdr_bin)

            # Check Icera tag is found:
            if chip:
                magic_tag = const.CHIP_TYPES[int(chip)]
                if hdr[0] != magic_tag:
                    if magic_tag:
                        arch_type = None
                        for type,value in const.CHIP_TYPES.items():
                            if value == hdr[0]:
                                arch_type = type
                        if arch_type:
                            msg = '\nERROR. Ristretto set to use {0} chip type, archive generated for {1}.\n'.format(chip, arch_type)
                        else:
                            msg = '\nERROR. Found unknown/unsupported 0x%x tag in archive %s\n' % (hdr[0], file)
                    else:
                        msg = '\nERROR. Found archive generated for %s chip type not supported by this tool revision.\n' % (chip)

                    if cb:
                        cb(msg)
                    else:
                        print msg
                    status = -1
            else:
                if hdr[0] not in const.CHIP_TYPES.values():
                    msg = 'ERROR. %s not a valid archive: found 0x%x as file header magic tag\n' % (os.path.basename(file), hdr[0])
                    msg = msg + 'Supported chip(s) list: {0}\n'.format(const.CHIP_TYPES)
                    if cb:
                        cb(msg)
                    else:
                        print msg
                    status = -1

            if status == 0:
                # Read extended header if found and verify checksum
                checksum = 0
                hdr_len = hdr[1]
                if hdr_len > const.ARCH_HEADER_BYTE_LEN: # there's an extended header
                    ext_hdr_len = hdr_len - const.ARCH_HEADER_BYTE_LEN
                    ext_hdr_bin = fd.read(ext_hdr_len)
                    # Need to compute ext_hdr checksum32
                    num_items = ext_hdr_len / 4
                    ext_hdr = struct.unpack("<%dL" % num_items, ext_hdr_bin)
                    for item in ext_hdr:
                        checksum = checksum ^ item
                for field in hdr:
                    checksum = checksum ^ field

                if checksum != 0:
                    msg = 'ERROR. Invalid header: bad checksum.'
                    if cb:
                        cb(msg)
                    else:
                        print msg
                    raise

                # Check it is a zipped archive or no
                if (hdr[4] & const.ZIP_MODE_MASK):
                    zipped = True

    except Exception:
        PrintException()
        status = -1

    finally:
        if fd:
            fd.close()
        return (status, hdr, ext_hdr_bin, zipped)

def ReadArchiveIdAndChip(file, chip=None, prodChecked=False):
    '''
    Return archive ID and chip and chip type.
    Archive header must be a valid one (check magic tag only).
    '''
    status = 0
    arch_id = -1
    prod = None

    try:
        # Read header:
        (status, hdr, ext_hdr_bin, zipped) = ReadHeader(file, chip)
        if status != -1:
            arch_id = hdr[4] & ~const.ZIP_MODE_MASK
            chip = 'invalid'
            for x,y in const.CHIP_TYPES.items():
                if hdr[0] == y:
                    chip =str(x)

        # Read signature:
        if prodChecked:
            status, prod = rsa_sign_icera.GetSigType(file)

    except Exception:
        PrintException()

    finally:
        return arch_id, chip, prod

def SwitchInLoaderIfRequired(lib, handle):
    '''
    Switch in loader mode on demand.
    '''
    error = 0

    try:
        ans = lib.SwitchModeEx(handle, IceraToolbox.MODE_LOADER, False)
        if ans != 1:
            print 'Switch in loader mode failure...: %d' % ans
            error = 1

    except Exception:
        error = 1
        PrintException()

    finally:
        if error == 1:
            print 'ERROR trying to switch in loader mode...'
        return error

def SendAtCmd(lib, handle, cmd, disp=True, verboseLevel=IceraToolbox.VERB_INFO):
    resp = None
    try:

        if disp == False:
            lib.VerboseLevelEx(handle, IceraToolbox.VERB_NONE)

        ans = lib.SendCmdAndWaitResponse(handle, None, None, '%s\r\n', cmd)
        if ans:
            buf_size = 512
            buf = ctypes.c_buffer(buf_size)
            resp = ''
            start =  time.time()
            while True:
                len = lib.Read(handle, buf, buf_size)
                resp += buf.raw[:len]
                if RistrettoCommon.AT_RSP_OK in resp:
                    break
                if RistrettoCommon.AT_RSP_ERROR in resp:
                    break
                if time.time() - start > 20.0:
                    # 60 seconds timeout
                    print 'ERROR timeout...\n'
                    break
        else:
            print 'ERROR sending AT command...\n'

    except Exception:
        PrintException()

    finally:
        if disp:
            print "-> {0}".format(resp)
        else:
            lib.VerboseLevelEx(handle, verboseLevel)
        return resp

def CheckOnBoardChipType(isf, chip):
    ''' Check on board chip type is compatible with selected chip type...'''
    err = 0
    try:
        bt2_dir, bt2_name = isf.GetWrapped('BT2')
        if bt2_dir == "":
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print 'WARNING: No BT2 found in platform to get platform chip type'
            print 'ANY CONFIG FILE WILL BE WRAPPED FOR PLATFORM {0}'.format(chip)
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            val = RistrettoFrameShare.PopUpYesOrNo("No BT2 found in platform to get platform chip type...\nAre you OK to generate any wrapped file for {0} chip type ?\n\n If NOK, please select valid chip type in File menu".format(chip), caption='Confirm {0} usage...'.format(chip))
            if val != wx.ID_YES:
                err = 1
        else:
            (status, hdr, ext_hdr_bin, zipped) = ReadHeader(os.path.join(bt2_dir, bt2_name))
            if status != -1:
                for chip_type,value in const.CHIP_TYPES.items():
                    if value == hdr[0]:
                        found_chip = chip_type
                if int(found_chip) != int(chip):
                    print 'ERROR: Ristretto set to use {0} platform whereas {1} platform is used'.format(chip, found_chip)
                    err = 1
            else:
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print 'WARNING: Fail to read BT2 header'
                print 'ANY CONFIG FILE WILL BE WRAPPED FOR PLATFORM {0}'.format(chip)
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                val = RistrettoFrameShare.PopUpYesOrNo("Fail to read on board BT2 header to get platform chip type...\nAre you OK to generate any wrapped file for {0} chip type ?\n\n If NOK, please select valid chip type in File menu".format(chip), caption='Confirm {0} usage...'.format(chip))
                if val != wx.ID_YES:
                    err = 1
    except Exception:
        PrintException()
        err = 1
    finally:
        return err

def productCfgFWID(productCFG):
    file_fwid=''
    err = 0
    try:
        with open(productCFG,'r') as file:
            pattern = re.compile('<fwid>(.*)</fwid>')
            for line in file:
                search=pattern.search(line)
                if search:
                    file_fwid=search.group(1)
                    break

    except Exception:
        err=-1

    print 'Product Config FWID: {0}'.format(file_fwid)
    return err, file_fwid

def readFWID(lib, handle):
    fwid=''
    err = 0

    ans = lib.SwitchModeEx(handle, IceraToolbox.MODE_LOADER,False)
    if ans != 1:
        print 'Switch in loader mode failure...: %d' % ans
        err = 1

    pattern=re.compile('IGETFWID: (.*)')
    # ask for IGETFWID
    rsp=SendAtCmd(lib, handle, "AT%IGETFWID\r\n")
    for A_buffer in rsp.splitlines():
        if pattern.search(A_buffer):
            A_FWID=re.split(': ',A_buffer)
            if len(A_FWID)<2: raiseError(1,"failed to respond to at%%FWID: [%s]"%A_buffer[1])
            fwid=A_FWID[1]
            break
    if fwid=='' and 'OK' not in rsp:
        print "WARNING: failed to read fwid from AT%%IGETFWID {0}".format(rsp)
        err=1

    return err,fwid

class ProgrammingThread(Thread):
    '''
    Class used for common initialisation for threads
    used for platform access.
    '''
    def __init__(self, conn, lib, comPort, verbosity, name, sockport=None, asn1_tool=None, chip="9040", prod_keys=None):
        try:
            Thread.__init__(self)
            self.handle = None
            self.conn = conn
            self.lib = lib
            self.comPort = comPort
            self.sock_port = sockport
            self.verbosity = verbosity
            self.chip=chip
            self.setName('%s' % name)
            self.handle=None
            self.error = 0
            self.msg=''
            self.isf=None
            self.fwid=''
            self.throughUpdater=False
            if (comPort == None) or (len(comPort) == 0):
                if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                    print 'Aborting. NULL COM port indicated'
                elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    print 'Aborting. NULL ADB device indicated'
            else:
                if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                    self.throughUpdater = True
                    self.handle = self.conn.OpenComPort(self.comPort, cb=False)
                    if self.handle == 0:
                        print 'ERROR. Thread %s, opening %s' % (self.getName(), self.comPort)
                        self.error = 1
                    else:
                        # Register handle callback
                        CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
                        self.c_callback = CFUNC(self.updaterlibCb)
                        self.lib.SetLogCallbackFuncEx(self.handle, self.c_callback)
                        if self.verbosity > IceraToolbox.VERB_INFO:
                            print 'Handle {0} for port {1}'.format(self.handle, self.comPort)

                elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    if self.conn.forwarded and self.sock_port:
                        self.handle = self.conn.OpenComPort(self.sock_port, cb=False)
                        if self.handle == 0:
                            print 'ERROR. Thread %s, opening %s' % (self.getName(), self.sock_port)
                            self.error = 1
                        else:
                            # Register handle callback
                            CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
                            self.c_callback = CFUNC(self.updaterlibCb)
                            self.lib.SetLogCallbackFuncEx(self.handle, self.c_callback)
                            if self.verbosity > IceraToolbox.VERB_INFO:
                                print 'Handle {0} for port {1}'.format(self.handle, self.sock_port)
                    if self.conn.IsSingleFlash(comPort):
                        self.isf=IceraSingleFlashAndroid(self.conn.adb.path, self.comPort, asn1_tool=asn1_tool, verbosity=verbosity, check_adb=False, chip=chip, prod_keys=prod_keys)
                    else:
                        self.isf=IceraDualFlashAndroid(self.conn.adb.path, self.comPort, asn1_tool=asn1_tool, verbosity=verbosity, check_adb=False, chip=chip, prod_keys=prod_keys, handle=self.handle, UpdaterLib=self.lib)

        except Exception:
            PrintException()
            self.error=1

    def updaterlibCb(self, msg):
        # UpdaterLib callback handler.
        if self.verbosity != IceraToolbox.VERB_NONE:
            self.msg = RistrettoCommon.ParseAndDispMsg(self.msg, msg)
        return 0

class ProgramConfigFileThread(ProgrammingThread):
    '''
    Class ProgramConfigFileThread:
    Config file building & programming performed in a thread context.
    Assumption is that platform was already switched in loader mode.
    '''
    def __init__(self, conn, lib, comPort, sockport, verbosity, xml_type, source, keys, asn1_tool, chip, enable_cbc, enable_krm, prod_keys):
        try:
            thread_name = 'configFileUpdate_'+ comPort
            ProgrammingThread.__init__(self, conn, lib, comPort, verbosity, thread_name, sockport=sockport, chip=chip, prod_keys=prod_keys)
            self.keys = keys
            self.asn1_tool = asn1_tool
            self.type = xml_type
            self.source = source
            self.sockport = sockport
            self.enable_cbc=enable_cbc
            self.enable_krm=enable_krm
            if self.error == 0:
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and self.conn.IsSingleFlash():
                    self.error = CheckOnBoardChipType(self.isf, chip)
            self.start()

        except Exception:
            if self.handle:
                self.conn.CloseComPort(self.handle, self.comPort)
            PrintException()

    def run(self):
        ans = 0
        err = 0
        fileToProg = True
        fileType = None
        err=0

        # Some default icera_datafile values
        oemFactKeys = self.keys[const.ARCH_OEM_FACT_KEY_SET]['path']
        oemFieldKeys = self.keys[const.ARCH_OEM_FIELD_KEY_SET]['path']
        imei=''
        configFile=''
        deviceFile=''
        productFile=''
        audioFile=''
        platcfgFile=''

        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                forceFlash=False
                (err,self.fwid)=self.isf.readFWID()
            else:
                (err,self.fwid) = readFWID(self.lib, self.handle)

            if err > 0:
                val = RistrettoFrameShare.PopUpYesOrNo("Failed to read FWID\nAre you sure you want to flash {0}?\n".format(self.source), caption='Confirm Flashing...')
                if val != wx.ID_YES:
                    self.error = err
                else:
                    forceFlash = True

            if self.error == 0:
                if self.type == 'IMEI':
                    fileToProg = False
                    fileType = 'IMEI'
                    imei = str(self.source)

                elif self.type == 'DEVICECFG':
                    fileType = 'Device Config'
                    deviceFile = self.source

                elif self.type == 'PRODUCTCFG':
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and not self.conn.singleFlash:
                        (self.error,cfg_fwid)=productCfgFWID(self.source)
                        if self.fwid != cfg_fwid and not forceFlash:
                            val = RistrettoFrameShare.PopUpYesOrNo("FWID is not matching \nAre you OK to change it ?\n".format(cfg_fwid), caption='Confirm FWID...')
                            if val != wx.ID_YES:
                                self.error = 1
                            else:
                                forceFlash=True
                        if forceFlash:
                            self.isf.fwid=cfg_fwid
                            self.isf.force_update=True
                            if cfg_fwid != '':
                                self.isf.Flash_fwid=True

                    fileType = 'Product Config'
                    productFile = self.source

                elif self.type == 'PLATCFG':
                    fileType = 'Platform Config'
                    platcfgFile = self.source
                    oemFactKeys = None
                    self.enable_cbc=False

                elif self.type == 'AUDIOCFG':
                    fileType = 'Audio Config'
                    audioFile = self.source
                    self.enable_cbc=False

                else:
                    print 'ERROR: %s is not a supported file' % self.type
                    self.error = 1

                if self.error == 0:
                    # Check key folder
                    if oemFactKeys != None and self.keys[const.ARCH_OEM_FACT_KEY_SET]['secret'] == False:
                        print 'ERROR: cannot use %s folder to sign a data file.' % self.keys[const.ARCH_OEM_FACT_KEY_SET]['path']
                        self.error = 1
                    if oemFieldKeys != None and self.keys[const.ARCH_OEM_FIELD_KEY_SET]['secret'] == False:
                        print 'ERROR: cannot use %s folder to sign a data file.' % self.keys[const.ARCH_OEM_FIELD_KEY_SET]['path']
                        self.error = 1

                if self.error == 0:
                    # Build config file
                    if fileToProg and (os.path.exists(self.source) == 0):
                        print 'ERROR: %s FILE NOT FOUND' % self.source
                        self.error = 1
                    else:
                        print 'Config File Update started on %s' % self.comPort
                        if self.throughUpdater:
                            if not self.handle:
                                self.error=1
                        if self.error==0:
                            if self.throughUpdater:
                                # No mode switching after update
                                self.lib.SetModeChange(self.handle, IceraToolbox.MODE_LOADER)
                                port=self.comPort
                                adb_tool=None
                                singleFlash=False
                            elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                                port='adb:{0}'.format(self.comPort)
                                self.handle=self.isf
                                adb_tool=self.conn.adb.path
                                singleFlash=self.conn.IsSingleFlash()
                            ans = -1
                            (ans, ofiles) = icera_datafile(self.lib,
                            port,
                            self.handle,
                            chip=self.chip,
                            imei=imei,
                            configFile=configFile,
                            deviceFile=deviceFile,
                            productFile=productFile,
                            platcfgFile=platcfgFile,
                            audioFile=audioFile,
                            flash=1,
                            keyFilesOemFact=oemFactKeys,
                            keyFilesOemField=oemFieldKeys,
                            adb_tool=adb_tool,
                            verbosity=self.verbosity,
                            enable_cbc=self.enable_cbc,
                            enable_krm=self.enable_krm,
                            SingleFlash=singleFlash)
                            if ans != 1:
                                print 'ERROR. Thread %s, building and programming %s on %s' % (self.getName(), fileType, self.comPort)
                                self.error = 1

        except Exception:
            PrintException(verb=self.verbosity)
            self.error = 1

        finally:
            if self.throughUpdater:
                # close COM
                if self.handle:
                    self.conn.CloseComPort(self.handle, self.comPort)
            elif self.isf.handle:
                self.conn.CloseComPort(self.isf.handle, self.comPort)
            if self.error:
                print 'ERROR. Programming %s' % self.type
            else:
                print '%s programming successful.' % self.type

class UnlockBoardThread(ProgrammingThread):
    '''
    Class UnlockBoardThread:
    Unlock certificate extraction and programming performed in a thread context
    Assumption is that platform was already switched in loader mode.
    '''
    def __init__(self, conn, lib, comPort, sockport, verbosity, file, ice_dbg, chip, prod_keys):
        try:
            thread_name = 'unlockBoard_'+ comPort
            ProgrammingThread.__init__(self, conn, lib, comPort, verbosity, thread_name, sockport=sockport, chip=chip, prod_keys=prod_keys)
            self.sock_port = sockport
            self.file = file
            self.ice_dbg=ice_dbg
            self.prod_keys=prod_keys
            if self.error==0:
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    self.adb_tool=self.conn.adb.path
                    self.comPort = 'adb:'+comPort
                else:
                    self.adb_tool = None
                    self.comPort= comPort
            self.start()

        except Exception:
            if self.handle:
                self.conn.CloseComPort(self.handle, self.comPort)
            PrintException()

    def run(self):
        ans = 0
        try:
            if self.error == 0:
                if self.throughUpdater:
                    if self.handle:
                        # No mode switching after update
                        self.lib.SetModeChange(self.handle, IceraToolbox.MODE_LOADER)
                        ans = unlock_board.unlock_board(self.file, self.lib, self.comPort, self.handle,
                                            verbosity=self.verbosity, chip=self.chip)
                        if ans != 1:
                            print "ERROR. Thread: %s, unlocking with %s" % (self.getName(), self.file)
                            self.error = 1
                    else:
                        print 'ERROR: No valid handle found for {0}'.format(self.comPort)
                elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    if self.conn.forwarded:
                        ans = unlock_board.unlock_board(self.file, self.lib, self.comPort, self.handle,
                                        verbosity=self.verbosity, adb_tool=self.adb_tool, ice_dbg=self.ice_dbg, chip=self.chip,
                                        SingleFlash=self.conn.singleFlash, prod_keys=self.prod_keys)
                    else:
                        print 'ERROR: You need to perform a port forwarding to unlock this platform.'
                        self.error = 1
                    if ans != 1:
                        print "ERROR. Thread: %s, unlocking with %s" % (self.getName(), self.file)
                        self.error = 1
        except Exception:
            PrintException(verb=self.verbosity)

        finally:
            # close COM
            if self.handle:
                self.conn.CloseComPort(self.handle, self.comPort)

class FileUpdateThread(ProgrammingThread):
    '''
    Class FileUpdateThread:
    File update performed in a thread context.
    Assumption is that platform was already switched in loader mode.
    '''
    def __init__(self, conn, lib, comPort, sockport, verbosity, file, enable_cbc, enable_krm, keys, asn1_tool, chip, prod_keys):
        try:
            thread_name = 'fileUpdate_'+ comPort
            ProgrammingThread.__init__(self, conn, lib, comPort, verbosity, thread_name, sockport=sockport, asn1_tool=asn1_tool, chip=chip, prod_keys=prod_keys)
            self.file = file
            self.sockport = sockport
            self.enable_cbc=enable_cbc
            self.enable_krm=enable_krm
            self.keys=keys
            self.start()

        except Exception:
            if self.handle:
                if self.throughUpdater:
                    self.conn.CloseComPort(self.handle, self.comPort)
            PrintException()

    def run(self):
        ans = 0
        try:
            if self.error == 0:
                (arch_id, unused1, unused2) = ReadArchiveIdAndChip(self.file)
                if arch_id == 6: # ISO image
                    libversion = ctypes.c_buffer(255)
                    libversion = ctypes.c_char_p(self.lib.GetLibVersion(libversion, len(libversion))).value
                    if libversion in ISO_UPDATE_INCOMPATIBLE_LIB:
                        print "ERROR: This Updaterlib version is not compatible for ISO image udpate."
                        self.error = 1
                if self.error == 0:
                    print 'File Update started on %s' % self.comPort
                    if self.throughUpdater:
                        if self.handle:
                            # No mode switching after update
                            self.lib.SetModeChange(self.handle, IceraToolbox.MODE_LOADER)
                            ans = self.lib.UpdaterEx(self.handle, ctypes.c_char_p(self.file), True, False)
                        else:
                            print 'ERROR: No valid handle found for {0}'.format(self.comPort)
                    elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        forceFlash=False
                        (err,self.fwid)=self.isf.readFWID()
                        if err > 0:
                            val = RistrettoFrameShare.PopUpYesOrNo("Failed to read FWID\nAre you sure you want to flash {0}?\n".format(self.file), caption='Confirm Flashing...')
                            if val != wx.ID_YES:
                                self.error = 1
                            else:
                                forceFlash=True
                                
                        arch_id, chip, prod = ReadArchiveIdAndChip(file=self.file, chip=self.chip, prodChecked=True)
                        if arch_id == -1:
                            print 'ERROR: what is this file ?: {0}'.format(file)
                            self.error = 1
                        else:
                            prop=const.GetArchPropById(arch_id)
                                
                        if err >= 0 and prop.acr == "PRODUCTCFG":
                            (self.error,cfg_fwid)=productCfgFWID("{0}.xml".format(os.path.splitext(win32api.GetLongPathName(self.file))[0]))
                            if self.fwid != cfg_fwid and not forceFlash:
                                val = RistrettoFrameShare.PopUpYesOrNo("FWID is not matching \nAre you OK to change it to {0}?\n".format(cfg_fwid), caption='Confirm FWID...')
                                if val != wx.ID_YES:
                                    self.error = 1
                                else:
                                    forceFlash = True
                            if forceFlash:
                                self.isf.fwid = cfg_fwid
                                self.isf.force_update=True

                        if self.error == 0:
                            ans=self.isf.UpdateFiles(files=self.file,
                            enable_cbc=self.enable_cbc,
                            enable_krm=self.enable_krm)
                        
                        if prop.acr == "UNLOCK":
                            print """

PLEASE REBOOT YOUR PLATFORM TO FINISH UNLOCKING PROCESS

"""
                            
                    if ans != 1:
                        print "ERROR. Thread: %s, updating %s" % (self.getName(), self.file)
                        self.error = 1

        except Exception:
            PrintException(verb=self.verbosity)
            self.error = 1

        finally:
            if self.throughUpdater:
                # close COM
                if self.handle:
                    self.conn.CloseComPort(self.handle, self.comPort)
            elif self.isf.handle:
                self.conn.CloseComPort(self.isf.handle, self.comPort)

class DetectChipTypeThread(ProgrammingThread):
    '''
    Class DetectChipTypeThread:
    Switch in loader mode and parse AT+GMR/AT%IPROD/AT%IPLATCFG responses performed in a thread context.
    Assumption is that platform was already switched in loader mode.
    '''
    def __init__(self, hif, lib, comPort, verbosity, asn1_tool, file_list):
        self.lib=lib
        try:
            thread_name = 'detectChipType_'+ comPort
            ProgrammingThread.__init__(self, hif, lib, comPort, verbosity, thread_name)
            self.files = file_list
            self.asn1_tool= asn1_tool
            self.chipType=None
            self.chipProd=None
            self.platCfg=None
            self.platFW=None
            self.start()

        except Exception:
            if self.handle:
                self.hif.CloseComPort(self.handle, self.comPort)
            PrintException()

    def run(self):
        ans = 0
        try:
            if self.error == 0:
                if self.handle:
                    print 'Detect chip type started on %s' % self.comPort
                    # Read AT+GMR in loader mode
                    at_rsp = SendAtCmd(self.lib, self.handle,"AT+GMR")
                    ice = re.search("boot\srom\ +(\w*)\ *", at_rsp).group(1)
                    if ice=='': self.chipType='8060' #patch for ICE8060 revA0 and A1
                    elif ice.find('ice')==-1:
                        print "ERROR. Error detecting chip type on %s" % (self.comPort)
                        self.error = 3
                    else: self.chipType=ice.replace('ice','')

                    # Read AT%IPROD in loader mode
                    at_rsp = SendAtCmd(self.lib, self.handle,"AT%IPROD")
                    prod = re.search("IPROD:\ Chip\ version:\ *(\w*)\ *", at_rsp).group(1)
                    if prod.find('development')==-1: self.chipProd=True
                    else: self.chipProd=False

                    # Read AT%IPLATCFG in loader mode
                    at_rsp = SendAtCmd(self.lib, self.handle,"AT%IPLATCFG")
                    self.platCfg = re.search("IPLATCFG:\ +(.*)\ *", at_rsp).group(1)

        except Exception:
            PrintException(verb=self.verbosity)
            self.error = 4

        finally:
            # close COM
            if self.handle:
                self.hif.CloseComPort(self.handle, self.comPort)
            # Detect supportHwPlatform if possible (FW present)
            if self.files!=[]:
                self.platFW = self._fwSupportedHwPlatform(files=self.files)
                if not self.platFW: self.error = 5

    def _fwSupportedHwPlatform(self, files):
        supportedHwPlat=None
        try:
            for file in files:
                ext_hdr = subprocess.Popen('%s -s EXTHDR -d -b \"%s\"' % (self.asn1_tool, file), shell=True, stdout=subprocess.PIPE).stdout.readlines()
                for l in ext_hdr:
                    print l
                    m = re.match('.*<compatibleHwPlatPattern>([\w\.\*]*)</compatibleHwPlatPattern>.*',l)
                    if m:
                        plat=m.group(1)
                        break
                if supportedHwPlat:
                    if plat!=supportedHwPlat: return None
                else:
                    supportedHwPlat=plat
        except Exception:
            PrintException(verb=self.verboseLevel)
        finally:
            return supportedHwPlat

class ReleaseUpdateThread(ProgrammingThread):
    '''
    Class ReleaseUpdateThread:
    Release update performed in a thread context.
    Assumption is that platform was already switched in loader mode.
    '''
    def __init__(self, conn, lib, comPort, sockport, verbosity, releaseFiles, keys, asn1_tool, chip, enable_cbc, enable_krm, prod_keys=None):
        try:
            thread_name = 'releaseUpdate_'+ comPort
            ProgrammingThread.__init__(self, conn, lib, comPort, verbosity, thread_name, sockport=sockport, asn1_tool=asn1_tool, chip=chip, prod_keys=prod_keys)
            self.releaseFiles = releaseFiles
            self.keys = keys
            self.sockport = sockport
            self.asn1_tool = asn1_tool
            self.enable_cbc = enable_cbc
            self.enable_krm = enable_krm
            if self.error == 0:
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and self.conn.singleFlash:
                    self.error = CheckOnBoardChipType(self.isf, chip)
            self.start()

        except Exception:
            if self.throughUpdater:
                if self.handle:
                    self.conn.CloseComPort(self.handle, self.comPort)
            elif self.isf.handle:
                self.conn.CloseComPort(self.isf.handle, self.comPort)
            PrintException()

    def run(self):
        ans = 1
        err = 0
        oemFactKeys = self.keys[const.ARCH_OEM_FACT_KEY_SET]['path']
        oemFieldKeys = self.keys[const.ARCH_OEM_FIELD_KEY_SET]['path']

        try:
            if self.error == 0:
                if self.releaseFiles['device_config'] !='':
                    if self.keys[const.ARCH_OEM_FACT_KEY_SET]['secret'] == False:
                        print 'ERROR: cannot use %s to sign a device config file' % self.keys[const.ARCH_OEM_FACT_KEY_SET]['path']
                        self.error = 1

                if self.releaseFiles['product_config'] != '' and self.keys[const.ARCH_OEM_FIELD_KEY_SET]['secret'] == False:
                    print 'ERROR: cannot use %s to sign a product config file' % self.keys[const.ARCH_OEM_FIELD_KEY_SET]['path']
                    self.error = 1

                if self.error == 0:
                    print 'Release Update started on %s' % self.comPort
                    if self.throughUpdater:
                        if self.handle:
                            (err,self.fwid)=readFWID(self.lib,self.handle)

                            # Mode switching after release update configured in config file
                            self.lib.SetModeChange(self.handle, IceraToolbox.MODE_MODEM)
                        else:
                            self.error=1

                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        (err,self.fwid)=self.isf.readFWID()

                    if err > 0:
                        val = RistrettoFrameShare.PopUpYesOrNo("Failed to read FWID from modem \nAre you sure you want to continue to flash ?", caption='Confirm Flashing...')
                        if val != wx.ID_YES:
                            self.error = err

                    if self.releaseFiles['product_config'] !='':
                        (self.error,cfg_fwid)=productCfgFWID(self.releaseFiles['product_config'])
                        if cfg_fwid != self.fwid and self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                            self.isf.force_update=True
                            self.isf.fwid=cfg_fwid
                        self.fwid=cfg_fwid

                    if not self.error:
                        releaseFiles=self.releaseFiles.copy() #avoid cleaning self.releaseFiles

                        # Update release with download_all
                        if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and not self.throughUpdater:
                            port='adb:{0}'.format(self.comPort)
                            self.handle=self.isf
                            adb_tool=self.conn.adb.path
                            singleFlash=self.conn.singleFlash
                        else:
                            port=self.comPort
                            adb_tool=None
                            singleFlash=False
                        ans = download_all(self.lib,
                        port,
                        self.handle,
                        self.chip,
                        self.verbosity,
                        self.verbosity,
                        self.asn1_tool,
                        adb_tool,
                        oemFactKeys,
                        oemFieldKeys,
                        self.keys[const.ARCH_ICE_OEM_KEY_SET]['path'],
                        self.keys[const.ARCH_ICE_ICE_KEY_SET]['path'],
                        releaseFiles,
                        self.enable_cbc,
                        self.enable_krm,
                        SingleFlash=singleFlash)
                        if ans != 1:
                            print "ERROR. Thread: %s, updating %s" % (self.getName(), releaseFiles)
                            if ans==0:  self.error = -1
                            else:       self.error = ans
                    else:
                        self.error = 1

        except Exception:
            PrintException(verb=self.verbosity)
            self.error = 1

        finally:
            if self.throughUpdater:
                # close COM
                if self.handle:
                    self.conn.CloseComPort(self.handle, self.comPort)
            elif self.isf.handle:
                self.conn.CloseComPort(self.isf.handle, self.comPort)

###################################################################
#                                                                 #
# ADB Connection Class                                            #
#                                                                 #
###################################################################
class AdbConnection:
    def __init__(self, UpdaterLib, verbosity):
        self.mode=RistrettoCommon.RISTRETTO_ADB
        self.lib          = UpdaterLib
        self.verbosity    = verbosity
        self.msg          = ''
        self.libversion = ctypes.c_buffer(255)
        self.libversion = ctypes.c_char_p(self.lib.GetLibVersion(self.libversion, len(self.libversion))).value
        CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.c_callback = CFUNC(self.updaterlibLoggingCallback)
        self.detected=0
        self.devices=[]
        self.adb=None
        self.autoSelect = True
        self.forwarded = False
        self.singleFlash = True
        try:
            self.adb = IceraAdb.AdbTool(None, verbosity=verbosity)
        except:
            pass

    def Scan(self):
        '''
        Scan for connected ADB devices...
        '''
        self.devices=[]
        self.detected=0
        port = IceraPortDetect.PortDetect()
        # Detect usual Android Composite ADB interface
        self.devices=port.detect('AndroidUsb', bypass=True)[0]
        if len(self.devices)!=0 and self.adb and self.adb.Cmd("get-state")[1] != "device":
            #ADB has not detected the platform yet
            time.sleep(5)
        if len(self.devices)==0 or (self.adb and self.adb.Cmd("get-state")[1] != "device"):
            # Try specific Cust ADB interfaces
            self.devices=port.detect('AndroidUsbCust', bypass=True)[0]
        if len(self.devices)==0 or (self.adb and self.adb.Cmd("get-state")[1] != "device"):
            # Try manual scan with adb...
            if self.adb:
                self.devices=self.adb.Devices()
        if len(self.devices)>0:
            self.forwarded = False
            self.detected=1

    def UpdateAdbPath(self, path):
        '''
        Update ADB tool path
        '''
        err=0
        try:
            self.adb = IceraAdb.AdbTool(path, verbosity=self.verbosity)
            if not self.adb:
                err=1
            elif not self.adb.path:
                err=1
        except Exception:
            # certainly an invalid tool
            err=1
            if self.adb:
                self.adb.path=None
        finally:
            return err

    def updaterlibLoggingCallback(self, msg):
        # UpdaterLib logging callback handler
        if self.verbosity != IceraToolbox.VERB_NONE:
            self.msg = RistrettoCommon.ParseAndDispMsg(self.msg, msg)
        return 0

    def OpenComPort(self, comport, cb=True, block_size=-1):
        '''
        Open a given port (should be a forwarded socket here...)
        and apply specific settings using handle:
            - set verbosity
            - set callback (can be disable with cb=False as arg).
              To be disabled when starting multiple port opening.
              In that case, after valid is returned, user must register
              a callback for each handle and not use the default one to
              avoid conflicts.
            - disable log sys state (misc AT cmds sent during F/W update
               or mode switching...)
        '''
        handle = 0

        if comport:
            port = comport
        else:
            print "ERROR: Please forward a COM port"
            return handle

        # open COM
        try:
            if self.verbosity > IceraToolbox.VERB_INFO:
                print "Opening %s..." % port
            handle = self.lib.Open(port)
            if handle:
                COM_HANDLES.append(handle)
                # Set verbosity
                self.lib.VerboseLevelEx(handle, self.verbosity)
                if cb:
                    # Register handle callback
                    self.lib.SetLogCallbackFuncEx(handle, self.c_callback)
                if self.verbosity > IceraToolbox.VERB_INFO:
                    print "{0}-- Opened with handle {1}".format(port, handle)
                # Disable log system state
                if float(self.libversion) >= 7.9:
                    self.lib.SetLogSysState(handle, 0)

        except Exception:
            PrintException(verb=self.verbosity)
            handle  = 0

        finally:
            if handle == 0:
                print "ERROR: Failed to open %s" % port
                print "Either device is disconnected, port is busy or not forwarded..."
            return handle

    def CloseComPort(self, handle, comport):
        '''
        Close comport related to a given handle.
        '''
        if handle:
            if self.verbosity > IceraToolbox.VERB_INFO:
                print "Closing handle {0} for port {1}".format(handle, comport)
            self.lib.Close(handle)
            COM_HANDLES.remove(handle)

    def IsSingleFlash (self, device=None):
        self.singleFlash = False
        try:
            if self.adb:
                if device == None:
                    devices = self.adb.Devices()
                    if len(devices) > 0:
                        device = devices[0]
                if device:
                    prop=self.adb.GetProp("init.svc.icera-loader", device=device, default="", verbosity= IceraToolbox.VERB_NONE)
                    if prop == "":
                        #icera-loader service might not be started yet (if no OTA), 
                        #then check if /vendor/bin/downloader is here or not
                        (err, stdout, stderr) = self.adb.Cmd("shell", "ls /vendor/bin/downloader", device)
                        if err or "no such file or directory" in stdout.lower():
                            self.singleFlash = True

        except Exception:
            PrintException(verb=self.verbosity)
            self.singleFlash = False
        finally:
            return self.singleFlash

###################################################################
#                                                                 #
# HIF Connection Class                                            #
#                                                                 #
# Handles:                                                        #
#  - COM port auto-detection                                      #
#  - COM port Open/Close                                          #
#  - PnP event notification                                       #
#                                                                 #
###################################################################
class HifConnection:
    def __init__(self, UpdaterLib, verbosity):
        self.mode=RistrettoCommon.RISTRETTO_HIF
        self.lib          = UpdaterLib
        self.verbosity    = verbosity
        self.msg          = ''
        self.libversion = ctypes.c_buffer(255)
        self.libversion = ctypes.c_char_p(self.lib.GetLibVersion(self.libversion, len(self.libversion))).value
        CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
        self.c_callback = CFUNC(self.updaterlibLoggingCallback)

        # Default auto-detect
        self.mdmPortList = None
        self.comPortList = None
        self.uartPortList = None
        self.singleFlash = True

        # Default HIF type: undefined
        self.hifType = None
        self.autoSelect = True

        # Default Flow Control
        self.flowControl = 1

        # Default baudrates
        self.baudrate = 115200
        self.appBaudrate = 115200 # baudrate used to  communicate with APP during boot from UART sequence
        self.bromBaudrate = 115200 # baudrate used to  communicate with BROM during boot from UART sequence

        # Default block size
        self.blockSize = RistrettoCommon.DEFAULT_BLOCK_SIZE
        self.bootUartBlockSize = RistrettoCommon.DEFAULT_BOOT_UART_BLOCK_SIZE

    def IsSingleFlash (self, device=None):
        return False

    def autoModemPortDetection(self):
        '''
        Perform Auto modem ports detection.
         For the moment, modem COM port is the only one used by ristretto
          since it can be used either in MDM or in LDR mode.

         Return 1 if platform(s) detected on Modem COM ports.
        '''

        ok = 0

        try:
            if self.mdmPortList == None:
                self.mdmPortList = []
                try:
                    getModem = self.lib.PortDetect
                    free=self.lib.freePortList
                    filter=ctypes.c_int(IceraToolbox.DETECT_UNKNOWN_TYPE_MASK|\
                        IceraToolbox.DETECT_SERIAL_TYPE_MASK|IceraToolbox.DETECT_MBIM_TYPE_MASK|\
                        IceraToolbox.DETECT_WINUSB_TYPE_MASK|IceraToolbox.DETECT_MODEM_FUNCTION_MASK)
                    fullDeviceName = ctypes.pointer(ctypes.c_char_p())
                    self.deviceFound = ctypes.pointer(ctypes.c_char_p())
                    count = getModem(filter, ctypes.byref(self.deviceFound), ctypes.byref(fullDeviceName))
                    if count == 0:
                        if IceraToolbox.IsLinux():
                            filter=ctypes.c_int(IceraToolbox.DETECT_UNKNOWN_TYPE_MASK|\
                        IceraToolbox.DETECT_SERIAL_TYPE_MASK|IceraToolbox.DETECT_MODEM_FUNCTION_MASK|\
                        IceraToolbox.DETECT_AT_FUNCTION_MASK|IceraToolbox.DETECT_UNKNOWN_FUNCTION_MASK)
                        else:
                            filter=ctypes.c_int(IceraToolbox.DETECT_UNKNOWN_TYPE_MASK|\
                            IceraToolbox.DETECT_SERIAL_TYPE_MASK|IceraToolbox.DETECT_MBIM_TYPE_MASK|\
                            IceraToolbox.DETECT_WINUSB_TYPE_MASK|IceraToolbox.DETECT_AT_FUNCTION_MASK)
                        count = getModem(filter, ctypes.byref(self.deviceFound), ctypes.byref(fullDeviceName))
                    if count != 0:
                        i=0
                        print "\n\nList of Modem detected: "
                        for i in range(count):
                            if self.deviceFound[i] not in self.mdmPortList:
                                self.mdmPortList.append(self.deviceFound[i])
                                print fullDeviceName[i]
                        free(fullDeviceName, count)
                        free(self.deviceFound, count)
                except AttributeError:
                    self.mdmPortList = espresso_detect.autoDetectModemPort(all=True)

            if self.mdmPortList:
                ok = 1

        except Exception:
            PrintException(verb=self.verbosity)

        finally:
            return ok

    def comport_cb(self, handle, spdd):
        '''
        Callback used for COM port detection.
        '''
        if IceraToolbox.IsWindows():
            comport_items=IceraWinSupport.GetDeviceParametersKey(handle, spdd, 'PortName')
            self.comPortList.append(comport_items)
        return True # Carry on

    def autoComPortDetection(self):
        '''
        COM ports detection:
            - physical COM ports
            - USB-to-UART COM ports
            - Modem ports
            - AT and Diagnostic COM ports are removed from final list
              since they are useless  for ristretto.
        '''
        ok = 0

        self.comPortList = []   # List all detected COM ports: Portname

        if IceraToolbox.IsWindows():
            # Detect all COM ports
            IceraWinSupport.WalkOnClasses(IceraWinSupport.ClassPortsGuid, self.comport_cb)

        # Detect all supported COM ports and remove them from portname_list
        # Ristretto should only work with Modem ports or COM ports to be used as UART ports

        try:
            getModem = self.lib.PortDetect
            free=self.lib.freePortList
            filter=ctypes.c_int(IceraToolbox.DETECT_UNKNOWN_TYPE_MASK|IceraToolbox.DETECT_SERIAL_TYPE_MASK|\
                IceraToolbox.DETECT_MBIM_TYPE_MASK|IceraToolbox.DETECT_WINUSB_TYPE_MASK|\
                IceraToolbox.DETECT_AT_FUNCTION_MASK|IceraToolbox.DETECT_DIAG_FUNCTION_MASK)
            fullDeviceName = ctypes.pointer(ctypes.c_char_p())
            self.deviceFound = ctypes.pointer(ctypes.c_char_p())
            count = getModem(filter, ctypes.byref(self.deviceFound), ctypes.byref(fullDeviceName))
            if count != 0:
                i=0
                for i in range(count):
                    if self.deviceFound[i] in self.comPortList:
                        self.comPortList.remove(self.deviceFound[i])
                free(fullDeviceName, count)
                free(self.deviceFound, count)

        #Legacy with the old updaterLib (to be remove)        
        except AttributeError:

            port = IceraPortDetect.PortDetect()
            #All AT ports
            for i in port.detect('AT', all=True)[0]:
                if i in self.comPortList:
                    self.comPortList.remove(i)
            #All Diagnostic 0 ports
            for i in port.detect('Diag0', all=True)[0]:
                if i in self.comPortList:
                    self.comPortList.remove(i)
            #All Diagnostic 1 ports
            for i in port.detect('Diag1', all=True)[0]:
                if i in self.comPortList:
                    self.comPortList.remove(i)

        # Before adding modem COM ports,
        #  let's consider there are only UART
        #  ports in list...
        self.uartPortList = []
        for i in self.comPortList:
            self.uartPortList.append(i)

        # Append modem ports
        ok = self.autoModemPortDetection()
        if ok:
            for i in self.mdmPortList:
                self.comPortList.append(i)

        return ok

    def updaterlibLoggingCallback(self, msg):
        # UpdaterLib logging callback handler
        if self.verbosity != IceraToolbox.VERB_NONE:
            self.msg = RistrettoCommon.ParseAndDispMsg(self.msg, msg)
        return 0

    def OpenComPort(self, comport, cb=True, block_size=-1):
        '''
        Open a given COM port
        and apply specific settings using handle:
            - set verbosity
            - set flow control
            - set callback (can be disable with cb=False as arg).
              To be disabled when starting multiple port opening.
              In that case, after valid is returned, user must register
              a callback for each handle and not use the default one to
              avoid conflicts.
            - disable log sys state (misc AT cmds sent during F/W update
               or mode switching...)
        '''
        handle = 0

        if comport:
            port = comport
        else:
            port = self.mdmPortList[0]

        blockSize = self.blockSize
        if block_size != -1:
            blockSize = block_size

        # open COM
        try:
            if self.verbosity > IceraToolbox.VERB_INFO:
                print "Opening %s..." % port
            libOpen=self.lib.Open
            libOpen.restype = ctypes.c_ulong
            handle = libOpen(port)
            if handle:
                COM_HANDLES.append(handle)
                # Set verbosity
                self.lib.VerboseLevelEx(handle, self.verbosity)
                if cb:
                    # Register handle callback
                    self.lib.SetLogCallbackFuncEx(handle, self.c_callback)
                # Set flow control
                ans = self.lib.SetFlowControl(handle, self.flowControl)
                # Set baudrate
                if float(self.libversion) >= 9.04:
                    if self.verbosity > IceraToolbox.VERB_INFO:
                        print 'Set baudrate: %d' % self.baudrate
                    ans = self.lib.SetBaudrate(handle, self.baudrate)
                # Set block size
                self.lib.SetBlockSize(handle, blockSize)
                if self.verbosity > IceraToolbox.VERB_INFO:
                    print 'Set block size: %d' % blockSize
                if self.verbosity > IceraToolbox.VERB_INFO:
                    print "{0}-- Opened with handle {1}".format(port, handle)
                # Disable log system state
                if float(self.libversion) >= 7.9:
                    self.lib.SetLogSysState(handle, 0)

        except Exception:
            PrintException(verb=self.verbosity)
            handle  = 0

        finally:
            if handle == 0:
                print "ERROR: Failed to open %s" % port
                print "Either device is disconnected or port is busy..."
            return handle

    def CloseComPort(self, handle, comport):
        '''
        Close comport related to a given handle.
        '''
        if handle:
            if self.verbosity > IceraToolbox.VERB_INFO:
                print "Closing handle {0} for port {1}".format(handle, comport)
            self.lib.Close(handle)
            COM_HANDLES.remove(handle)
            if comport and 'tcp' in comport:
                time.sleep(0.5) #leave time for port to close/open properly on slower TCP connection

    def Scan(self):
        # Scan for connected devices on any COM port (Modem COM port only...)
        #
        # Return connection status: 0 = no platform connected
        #                           1 = n platform(s) connected
        #  & multi platform information: True or False
        #
        # Variables like MDMPort or mdmPortList are updated here.

        if self.autoSelect: # only scan if COM port automatic selection is ON
            # Scan all COM ports
            self.mdmPortList = None
            self.detected = 0
            self.detected = self.autoComPortDetection()

    def UpdateBlockSize(self, value):
        self.blockSize = value
        self.bootUartBlockSize = value

    def UpdateAppBaudrate(self, baudrate):
        self.appBaudrate = baudrate

    def UpdateBromBaudrate(self, baudrate):
        self.bromBaudrate = baudrate
        
class LoginDialog(wx.Dialog):
    """
    Class to define login dialog
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Login to netapp-fr - Enter your Nvidia Credentials")
 
        # user info
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        user_lbl = wx.StaticText(self, label="Username:")
        user_sizer.Add(user_lbl, 0, wx.ALL|wx.CENTER, 5)
        self.user = wx.TextCtrl(self)
        user_sizer.Add(self.user, 0, wx.ALL, 5)
 
        # pass info
        p_sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        p_lbl = wx.StaticText(self, label="Password:")
        p_sizer.Add(p_lbl, 0, wx.ALL|wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        p_sizer.Add(self.password, 0, wx.ALL, 5)
 
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.ALL, 5)
        main_sizer.Add(p_sizer, 0, wx.ALL, 5)
 
        btn = wx.Button(self, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
 
        self.SetSizer(main_sizer)
 
    #----------------------------------------------------------------------
    def onLogin(self, event):
        """
        Check credentials and login
        """
        url = 'http://netapp-fr/mobile/Icera_share/Modem_tools/Unlock_certificates'
        username = self.user.GetValue()
        password = self.password.GetValue()
        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
        
        p.add_password(None, url, username, password)
        
        handler = urllib2.HTTPBasicAuthHandler(p)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        self.Destroy()
        

###################################################################
#                                                                 #
# Platform Class                                                  #
#                                                                 #
###################################################################
class Platform:
    def __init__(self, log, verbosity=IceraToolbox.VERB_INFO, disCb=NullFunc, updCb=NullFunc):
        try:
            self.log = log
            self.disCb = disCb
            self.updCb = updCb
            self.msg = ''

            # Default verbose level
            self.verboseLevel = verbosity

            # Default asn1 tool
            self.asn1_tool = None
            
            if IceraToolbox.IsWindows():
                self.crash_check = os.path.realpath(os.path.join(IceraToolbox.BASE_PATH,'icera-log-utils','bin.wx32','crash-check.exe'))
            else:
                self.crash_check = os.path.realpath(os.path.join(IceraToolbox.BASE_PATH,'icera-log-utils','crash-check'))

            # Key init.
            self.keys = deepcopy(rsa_sign_icera.DEVKEYS)
            for key_set in self.keys.keys():
                # Dev keys are stored with secret key to sign files
                self.keys[key_set]['secret'] = True

            # list of all prod keys
            self.prod_keys = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(IceraToolbox.BASE_PATH,'drivers','private','arch','keys')):
                for dirname in dirnames:
                    if os.path.join(dirpath, dirname) in [p['path'] for p in self.keys.values()]: continue
                    if len([key for key in self.keys.values() if key['acr'] in dirpath])==0: continue
                    else: key=key = [key for key in self.keys.values() if key['acr'] in dirpath][0]
                    if os.path.exists(os.path.join(dirpath, dirname, "secret.key.hex")):
                        self.prod_keys.append({'acr': key['acr'], 'path': os.path.realpath(os.path.join(dirpath, dirname)), 'secret': True})
                    elif os.path.exists(os.path.join(dirpath, dirname, "key.modulus.h")):
                        self.prod_keys.append({'acr': key['acr'], 'path': os.path.realpath(os.path.join(dirpath, dirname)), 'secret': False})

            # CBC enabled by default, KRM enabled by default, FIL restarted after update
            self.enable_cbc=True
            self.enable_krm=True
            self.fil_restart=True

            # Default config: DO NOT MODIFY EXCEPT FOR ADDITIONAL CONFIG!!!!!
            # If you need to use a different config, please create a valid config.txt file
            self.configFile = RistrettoCommon.RISTRETTO_CUSTOMIZED_CONFIG_FILE
            self.existingConfig       = False
            self.useAdb               = False
            self.chip                 = '9040'
            self.prod                 = False
            self.allowUnlock          = False
            
            # Read ristretto configuration file if exists
            self._getConfig()

            # Read stored settings that might overwrite config
            settings = RistrettoCommon.GetSettings()
            if settings.has_key("interfaceMode"):
                if settings["interfaceMode"] == RistrettoCommon.RISTRETTO_ADB:
                    self.useAdb = True

            # UART server stopped
            self.bootRepairFromUartAborted = False
            self.boardRepairUartServerHandle = None
            self.uartDiscoveryAborted = False
            self.uartDiscoveryServerHandle = None

            # Unzip & Untargz utilities
            self.unzipper = Unzip()
            self.untarrer = Untargz()

            # Open UpdaterLib
            self.lib=None
            self.libname = os.path.abspath(IceraToolbox.LIBNAME)
            assert os.path.isfile(self.libname), 'Library not found: %s' % self.libname
            self.lib = IceraToolbox.OpenLibrary(self.libname)
            self.libversion = ctypes.c_buffer(255)
            self.libversion = ctypes.c_char_p(self.lib.GetLibVersion(self.libversion, len(self.libversion))).value

            # Open platform interface
            self.hif=None
            self.adb=None
            if self.useAdb:
                # Create ADB connection
                self.adb = AdbConnection(self.lib, self.verboseLevel)
                self.conn=self.adb
            else:
                # Create HIF connection
                self.hif = HifConnection(self.lib, self.verboseLevel)
                self.conn=self.hif
            # Start automatic platform detection
            self._startPnpEvent()
                            
        except Exception:
            PrintException()

    def Close(self):
        if self.lib:
            print 'Closing Platform'
            self._stopPnpEvent()
            for handle in COM_HANDLES:
                self.conn.CloseComPort(handle, 'unknown')

    def _pnpCb(self, event, devicepath):
        '''
        Callback for PnP event notifications:
        only responsible for added or removed events
        '''
        if event == 'added' or event == 'removed':
            if self.verboseLevel >= IceraToolbox.VERB_ERROR:
                print "One device %s." % event
            self.disCb()
            self.conn.Scan()
            self.updCb()

        return False

    def _startPnpEvent(self):
        self.waitPnp = None
        if IceraToolbox.IsWindows():
            self.waitPnp = IceraWinSupport.WaitPnpEvent(self.lib, self._pnpCb, guids=GUIDS, verbosity = IceraToolbox.VERB_ERROR)

    def _stopPnpEvent(self):
        if self.waitPnp:
            self.waitPnp.StopPnpEvent()

    ########################################################
    #                                                      #
    # Ristretto configuration.                             #
    #                                                      #
    # Ristretto can be configured to enable/disable some   #
    #  features.                                           #
    # Available configuration parameters must be set in a  #
    #  file name "config.txt" and situated in the same     #
    #  folder of ristretto main                            #
    #                                                      #
    # Ristretto also uses data serialization to be applied #
    #  at start-up                                         #
    ########################################################
    def _getConfig(self):
        if os.path.isfile(self.configFile):
            self.existingConfig = True
            file = open(self.configFile, 'r')
            line = file.readline()
            while line != '':
                if line.find('ALLOW_UNLOCK_BOARD') != -1:
                    if 'false' in line.lower():
                        self.allowUnlock = False
                    if 'true' in line.lower():
                        self.allowUnlock = True

                line = file.readline()
            file.close()

    def CallAction(self, action, comport, sock_port, args):
        rsp=None
        err = 0
        try:
            if self.conn.mode == RistrettoCommon.RISTRETTO_ADB:
                if not self.conn.IsSingleFlash():
                    # ADB device used through port forwarding
                    if action != RistrettoCommon.ADB and action != RistrettoCommon.UPDATE_RELEASE \
                    and action != RistrettoCommon.FILE_UPDATE and action != RistrettoCommon.PROGRAM_IMEI \
                    and action != RistrettoCommon.PROGRAM_CALIB and action != RistrettoCommon.PROGRAM_XML \
                    and action != RistrettoCommon.BUILD_COREDUMP and action != RistrettoCommon.CLEAR_CRASHINFO:
                        comport = sock_port
                else:
                    if action == RistrettoCommon.CHECK_PCID or action == RistrettoCommon.CHECK_LOCK_TYPE:
                        comport = sock_port
            # Switch required action:
            if action == RistrettoCommon.DISPLAY_CRASHINFO:          self.displayCrashInfo(comport)
            if action == RistrettoCommon.BUILD_COREDUMP:             self.buildCoredump(comport, args)
            if action == RistrettoCommon.DECODE_COREDUMP:            self.decodeCoredump(args)
            if action == RistrettoCommon.CLEAR_CRASHINFO:            self.clearCrashHistory(comport)
            if action == RistrettoCommon.LIST_FILESYSTEM:            self.listFilesystem(comport)
            if action == RistrettoCommon.DISPLAY_PLATINFO:           self.displayPlatformInfo(comport)
            if action == RistrettoCommon.DETECT_CHIP_TYPE:           (rsp,err) = self.detectChipType(comport, args)
            if action == RistrettoCommon.UPDATE_RELEASE:             (rsp,err) = self.releaseUpdate(comport, sock_port, args)
            if action == RistrettoCommon.SCAN_TARGET:                self.scanTarget()
            if action == RistrettoCommon.FILE_UPDATE:                self.singleFileUpdate(comport, sock_port, args)
            if action == RistrettoCommon.START_UART_SERVER:          self.startUartServer(args)
            if action == RistrettoCommon.STOP_UART_SERVER:           self.stopUartServer(args)
            if action == RistrettoCommon.SET_HIF_TYPE:               self.setHifType(comport, args)
            if action == RistrettoCommon.LAUNCH_AT_CMD:              rsp = self.launchAtCommand(comport, args)
            if action == RistrettoCommon.GET_MEMORY_DUMP:            self.getMemoryDump(comport, args)
            if action == RistrettoCommon.STOP_WAIT_PNPEVENT:         self.stopPnpEvent()
            if action == RistrettoCommon.PROGRAM_XML:                self.programXmlCfg(comport, sock_port, args)
            if action == RistrettoCommon.PROGRAM_IMEI:               self.programImei(comport, sock_port, args)
            if action == RistrettoCommon.PROGRAM_CALIB:              self.programCalibrationFiles(comport, sock_port,  args)
            if action == RistrettoCommon.GET_ARCH_INFO:              self.getArchiveInfo(args)
            if action == RistrettoCommon.START_FACTORY_BOARD_REPAIR: self.startFactoryBoardRepair(args)
            if action == RistrettoCommon.STOP_FACTORY_BOARD_REPAIR:  self.stopFactoryBoardRepair(args)
            if action == RistrettoCommon.EXTRACT_ARCHIVE:            self.ExtractArchiveWrapper(args)
            if action == RistrettoCommon.ADB:                        rsp,err=self.adbAction(comport, args)
            if action == RistrettoCommon.DECODE_MEMORY_DUMP:         self.decodeMemoryDump(args)
            if action == RistrettoCommon.CHECK_LOCK_TYPE:            rsp=self.checkLockType(comport)
            if action == RistrettoCommon.CHECK_PCID:                 rsp,err=self.checkPCIDWrapper(comport)
        except Exception:
            PrintException(verb=self.verboseLevel)
            err = 1

        finally:
            return rsp,err

    def _doSwitchInLoaderMode (self, comport, recovery=False):
        '''
        Do switch in loader mode, handling the fact that original COM port number may
        change after mode switching...
        '''
        error = 0
        unused = []
        handle = None
        try:

            if self.conn.autoSelect and (self.conn.mode != RistrettoCommon.RISTRETTO_ADB):
                # In autoSelect mode using HIF, handles COM port change during switch in loader inside Ristretto
                # Get existing COM ports
                exiting_ports = self.hif.mdmPortList
                if comport not in self.hif.mdmPortList:
                    # May not be possible... comport not a detected port...
                    print 'ERROR: {0} not found in detected ports: {1}'.format(comport, self.hif.mdmPortList)
                    error = 1
                else:
                    # keep list of ports not used
                    for port in self.hif.mdmPortList:
                        if port != comport:
                            unused.append(port)

                    # Do a switch in loader
                    handle = self.hif.OpenComPort(comport)
                    if handle:
                        rsp = SendAtCmd(self.lib, handle, "AT%MODE?")
                        if "MODE: 1" in rsp:
                            print 'Board on {0} is in loader mode'.format(comport)
                            self.hif.CloseComPort(handle, comport)
                            handle=None
                        else:
                            if not recovery:
                                SendAtCmd(self.lib, handle, "AT%MODE=1")
                            else:
                                SendAtCmd(self.lib, handle, "AT%MODE=1,3")
                            self.hif.CloseComPort(handle, comport)
                            handle=0
                            timeout=30
                            while timeout:
                                # wait for re-enumeration
                                # wait port per port in case multi ports are used
                                # to ensure we retreive the same num of ports
                                # after switch...
                                time.sleep(1)
                                timeout=timeout-1
                                self.scanTarget()
                                if len(self.hif.mdmPortList)==len(exiting_ports):
                                    # we have the same num of ports as the ones detected
                                    # at the beginning...
                                    break
                            if timeout == 0:
                                print 'ERROR: Timeout. Fail to switch in loader mode'
                                error=1
                    else:
                        print 'ERROR: Fail to open COM {0}. Exiting...'.format(comport)
                        error=1

                if error == 0:
                    for port in self.hif.mdmPortList:
                        if port not in unused:
                            comport = port
            else:
                # When port is manually specified or a socket port, only 1 port is specified so no special handling required
                handle = self.conn.OpenComPort(comport)
                if handle:
                    error = SwitchInLoaderIfRequired(self.lib, handle)
                else:
                    print 'ERROR: Fail to open COM {0}.'.format(comport)
                    error = 1
        except Exception:
            PrintException(verb=self.verboseLevel)
            error=1

        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)
            return error, comport

    def _multiCom(self, type, comport, sockport=None, file_list=None, source=None, xml_type=None):
        '''
        Perform action using all COM ports in comPortList...
        This scheme will support single/multi platform actions using thread context.
        '''
        threads=list()
        error = 0
        rsp = None
        handle = None

        if comport:
            comPortList = [comport]
        else:
            if self.hif:
                comPortList = self.hif.mdmPortList
            elif self.adb:
                comPortList = self.adb.devices

        try:
            if error == 0:
                for comPort in comPortList:
                    if (type=='FILE' or type=='CONFIG FILE' or type=='RELEASE'):
                        if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                            if self.conn.IsSingleFlash():
                                if self.fil_restart:
                                    self._adbFil(comPort, 'STOP_FIL')
                    if self.hif:
                        error, comPort = self._doSwitchInLoaderMode(comPort)
                    if not error:
                        if type == 'DETECT_CHIP_TYPE': thread = DetectChipTypeThread(self.conn, self.lib, comPort, self.verboseLevel, self.asn1_tool, file_list)
                        if type == 'FILE':             thread = FileUpdateThread(self.conn, self.lib, comPort, sockport, self.verboseLevel, file_list, self.enable_cbc, self.enable_krm, self.keys, self.asn1_tool, self.chip, self.prod_keys)
                        if type == 'CONFIG FILE':      thread = ProgramConfigFileThread(self.conn, self.lib, comPort, sockport, self.verboseLevel, xml_type, source, self.keys, self.asn1_tool, self.chip, self.enable_cbc, self.enable_krm, self.prod_keys)
                        if type == 'RELEASE':          thread = ReleaseUpdateThread(self.conn, self.lib, comPort, sockport, self.verboseLevel, file_list, self.keys, self.asn1_tool, self.chip, self.enable_cbc, self.enable_krm, self.prod_keys)
                        if type == 'UNLOCK_BOARD':     thread = UnlockBoardThread(self.conn, self.lib, comPort, sockport, self.verboseLevel, file_list, self.keys[const.ARCH_ICE_DBG_KEY_SET]['path'], self.chip, self.prod_keys)
                        threads.append(thread)

        except Exception:
            PrintException(verb=self.verboseLevel)
            print 'ERROR during update.'
            error = 10

        finally:
            for thread in threads:
                thread.join()
                error = thread.error
                if type == 'DETECT_CHIP_TYPE':
                    if error==0:
                        if rsp:
                            if rsp[0] != thread.chipType:
                                print 'ERROR during chip type detect. Multiple devices with different chip type detected'
                                error=11
                            if rsp[1] != thread.chipProd:
                                print 'ERROR during chip type detect. Multiple devices with different chip security detected'
                                error=12
                            if rsp[2] != thread.platCfg:
                                print 'ERROR during platform detect. Multiple devices with different platforms detected'
                                error=13
                        else:
                            rsp = (thread.chipType, thread.chipProd, thread.platCfg, thread.platFW)
                    else:
                        print 'ERROR {0} during chip type detect'.format(error)
                if (type=='FILE' or type=='CONFIG FILE' or type=='RELEASE') and not error:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        if self.conn.IsSingleFlash():
                            if self.fil_restart:
                                self._adbFil(thread.comPort, 'START_FIL')

            return rsp,error

    def LibClose(self):
        try:
            if self.lib:
                self._stopPnpEvent()
                # Need to know lib has been closed...:
                self.lib = None
        except Exception:
            PrintException()

    def LibOpen(self, libname=None):
        try:
            if not self.lib:
                # Open lib.
                if not libname:
                    libname = self.libname
                self.libname = os.path.realpath(libname)
                self.lib = IceraToolbox.OpenLibrary(libname)
                self.libversion = ctypes.c_buffer(255)
                self.libversion = ctypes.c_char_p(self.lib.GetLibVersion(self.libversion, len(self.libversion))).value
                print '\nWill use %s as updater lib dll' % libname
                print 'Updater Lib version: %s' % self.libversion

                # Re-init HIF with new lib
                self.conn.lib = self.lib
                self.conn.libversion = self.libversion
                self._startPnpEvent()
                self.disCb()
                self.conn.Scan()
                self.updCb()

        except Exception:
            PrintException()

    def LibSwitch(self, libname = None):
        if self.lib:
            # Close lib
            self.LibClose()
            # Open lib...
            self.LibOpen(libname)

    def GetLibPath(self):
        if self.lib:
            return self.libname

    def LibVersion(self):
        # Return lib version
        if self.verboseLevel > IceraToolbox.VERB_INFO:
            print '\nLibrary version: %s\n\n' % self.libversion
        return self.libversion

    def _my_remove(self, func, path, exc_info):
        # Force file removal by changing write access...
        if IceraToolbox.IsWindows():
            os.chmod(win32api.GetShortPathName(path), stat.S_IWRITE)
            os.remove(win32api.GetShortPathName(path))
        else:
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)

    def ExtractArchive(self, extract_folder, zipsource, updateCB=None):
        ans = 1
        try:
            if not os.path.exists(extract_folder):
                os.mkdir(extract_folder)
            else:
                for root, dirs, files in os.walk(extract_folder):
                    for d in dirs:
                        if IceraToolbox.IsWindows():
                            shutil.rmtree(win32api.GetShortPathName(os.path.join(root, d)), ignore_errors=False, onerror=self._my_remove)
                        else:
                            shutil.rmtree(os.path.join(root, d), ignore_errors=False, onerror=self._my_remove)
                    for f in files:
                        self._my_remove(None, os.path.join(root, f), None)
            if IceraToolbox.IsWindows():
                self.extract_folder = win32api.GetShortPathName(extract_folder)
            else:
                self.extract_folder = extract_folder
            if zipsource.endswith('.zip') or zipsource.endswith('.ipkg'):
                ans = self.unzipper.extract(zipsource, self.extract_folder, updateCB)
            if zipsource.endswith('.tgz') or zipsource.endswith('.tar.gz'):
                print 'Extracting:'
                self.untarrer.namelist(zipsource)
                print 'in %s' % extract_folder
                ans = self.untarrer.extract(zipsource, self.extract_folder, updateCB)
            if ans == 0:
                print 'ERROR: Fail to extract %s' % zipsource
                return ans
        except Exception:
            PrintException()
            ans = 0
        finally:
            if ans == 0:
                return None
            else:
                return extract_folder

    def IsKeyFolderOk(self, keypath, key_set):
        # Check content of a standard key folder.
        ans = 1
        err = 0
        signing = True

        ans = FileExist(keypath, 'key.exponent.h')
        if ans == 0:
            err = 1

        ans = FileExist(keypath, 'key.modulus.h')
        if ans == 0:
            err = 1

        ans = FileExist(keypath, 'secret.key.hex')
        if ans == 0:
            signing = False

        return err, signing

    def isBoardUnlocked(self, comport, sock_port):
        handle = None
        throughAT = False # list file system thorugh AT cmd or not...
        unlocked=False
        noModem=False
        error=0
        if comport:
            comPortList = [comport]
        else:
            if self.hif:
                comPortList = self.hif.mdmPortList
            elif self.adb:
                comPortList = self.adb.devices
        for comPort in comPortList:
            try:
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    if self.conn.IsSingleFlash():
                        sf=IceraSingleFlashAndroid(self.conn.adb.path, comPort, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                        unlocked = sf.isUnlocked()
                    else:
                        comPort=sock_port
                        throughAT=True
                else:
                    throughAT=True

                if throughAT:
                    handle = self.conn.OpenComPort(comPort)
                    if handle:
                        self.lib.SendCmd(handle, "AT%%IPROD\r\n")
                        rsp = ctypes.c_char_p(self.lib.GetResponseEx(handle)).value
                        print "{0}\n".format(rsp)
                        if "IPROD: Chip version: unlocked" in rsp:
                            unlocked = True
                        elif rsp == "" or RistrettoCommon.AT_RSP_ERROR in rsp:
                            if not self.conn.IsSingleFlash():
                                noModem=True
                                val = RistrettoFrameShare.PopUpYesOrNo("Modem seems to be dead, it is impossible to know if board is unlocked or not.\n Are you sure you want to push these FW on the board", caption='Confirm unlock board...')
                                if val == wx.ID_YES:
                                    unlocked = True
                                else:
                                    error=1

            except Exception:
                PrintException()
                unlocked = False
            finally:
                if handle:
                    self.conn.CloseComPort(handle, comPort)
                    
                return unlocked, noModem, error

    def GetAcr(self, key):
        try:
            for k in self.keys:
                if k == key:
                    return self.keys[k]['acr']
            raise
        except:
            print 'ERROR. Invalid key set asked: %s' % key

    def GetKeyPath(self, key_set):
        try:
            for key in self.keys:
                if key_set == self.keys[key]['acr']:
                    return self.keys[key]['path']
            raise
        except:
            print 'ERROR. Invalid key set asked: %s' % key_set



    def UpdateKeyPath(self, keypath, key_set, signing):
        try:
            for key in self.keys:
                if key_set == self.keys[key]['acr']:
                    self.keys[key]['path'] = keypath
                    self.keys[key]['secret'] = signing
                    return
            raise
        except:
            print 'ERROR. Invalid key set to update: %s' % key_set

    def UpdateVerbosity(self, verbosity):
        self.verboseLevel = verbosity
        self.conn.verbosity=verbosity
        if self.adb:
            self.adb.adb.UpdateVerbosity(verbosity)

    def UpdateCbcValue(self, value):
        self.enable_cbc=value

    def UpdateKrmValue(self, value):
        self.enable_krm=value

    def UpdateFilRestart(self, value):
        self.fil_restart=value

    def displayByteFromBin(self, fd=None, len=0, bin=None):
        data_disp = ''
        if fd:
            data_bin = fd.read(len)
            data = struct.unpack("<%dB" % len, data_bin)
        else:
            if bin == None:
                print 'ERROR using displayByteFromBin()'
                raise
            data = bin
        for i in data:
            if i < 16:
                data_disp = data_disp+'0%x' % i
            else:
                data_disp = data_disp+'%x' % i
        return data_disp.upper()

    # DISPLAY_CRASHINFO
    def displayCrashInfo(self, comport):
        handle = None

        try:
            handle= self.hif.OpenComPort(comport)
            if handle:
                at_debug.ATDebug (at_debug.ACTION_CRASHINFO, comport, com_hdl=handle, UpdaterLib=self.lib, store_path=None)

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.hif.CloseComPort(handle, comport)

    # BUILD_COREDUMP
    def buildCoredump(self, comport, args):
        error = 0
        type = args[0]
        coredump_dir = args[1]
        ram_action = ""

        try:   
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                num=0
                if self.conn.IsSingleFlash():
                    sf=IceraSingleFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                else:
                    sf=IceraDualFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                error,num=sf.GetCoredumpFiles(coredump_dir, type)
                if not error:
                    if num:
                        print '{0} {2} coredump files stored in {1}'.format(num, coredump_dir, type)
                    else:
                        print 'No {0} coredump files found...'.format(type)
            else:
                if type == 'RAM':
                    ram_action = "--ram-only"
                print comport
                if 'tcp' in comport.lower():
                    if len(comport.split(':'))==2:
                        port = comport.split(':')[1]
                        adress=''
                    else:
                        [port,adress] = comport.split(':')[1:]
                    print("{0} {1} {2} {3} {4} {5} {6}".format(self.crash_check,"--dir",coredump_dir,port,adress,"--verbose",ram_action))
                    print("Please wait...")
                    (stdout,stdout)=subprocess.Popen("{0} {1} {2} {3} {4} {5} {6}".format(self.crash_check,"--dir",coredump_dir,port,adress,"--verbose",ram_action),\
                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
                else:
                    print("{0} {1} {2} {3} {4} ".format(self.crash_check,"--dir",coredump_dir,"--verbose",ram_action))
                    print("Please wait...")
                    (stdout,stdout)=subprocess.Popen("{0} {1} {2} {3} {4}".format(self.crash_check,"--dir",coredump_dir,"--verbose",ram_action),\
                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
                    
                print stdout

        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)

        finally:
            if error:
                print 'ERROR. Coredump failure.'

    # CLEAR_CRASHINFO
    def clearCrashHistory(self, comport):
        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                if self.conn.IsSingleFlash():
                    sf=IceraSingleFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                else:
                     sf=IceraDualFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                sf.ClearDebugFolder()
            else:
                if 'tcp' in comport.lower():
                    if len(comport.split(':'))==2:
                        port = comport.split(':')[1]
                        adress=''
                    else:
                        [port,adress] = comport.split(':')[1:]
                    print("{0} {1} {2} {3} {4} {5} {6}".format(self.crash_check,"--dir",".","--clear-history",port,adress,"--verbose"))
                    (stdout,stdout) = subprocess.Popen("{0} {1} {2} {3} {4} {5} {6}".format(self.crash_check,"--dir",".","--clear-history",port,adress,"--verbose"),\
                    shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
                else:
                    (stdout,stdout) = subprocess.Popen([self.crash_check,"--dir",".","--clear-history","--verbose"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

                print stdout

        except Exception:
            PrintException(verb=self.verboseLevel)

    # DECODE_COREDUMP
    def decodeCoredump(self, logdump):
        error = 0
        try:
            logdir = os.path.dirname(logdump)
            ram_dump = os.path.join(logdir, 'extmem.bin')
            if not os.path.isfile(ram_dump):
                ram_dump = None
            AtDebugDecoder(logdump, extmem=ram_dump)

        except Exception:
            error = 1
            PrintException()

        finally:
            if error == 0:
                print 'Coredump decoded and stored in %s\n' % os.path.dirname(logdump)

    # LIST_FILESYSTEM
    def listFilesystem(self, comport):
        handle = None
        throughAT = False # list file system thorugh AT cmd or not...
        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                throughAT = True
            elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                if self.conn.IsSingleFlash():
                    sf=IceraSingleFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                    folders, content=sf.ListFileSystem()
                    for folder in content:
                        print '{0} ({1}) folder content:'.format(folder, folders[folder])
                        for line in content[folder].split('\r\r\n'):
                            print line
                else:
                    throughAT = True
            if throughAT:
                error, comport = self._doSwitchInLoaderMode(comport)
                if not error:
                    handle = self.conn.OpenComPort(comport)
                    if handle:
                        self.lib.SendCmd(handle, "AT%%IFLIST\r\n")
                        print '{0}'.format(ctypes.c_char_p(self.lib.GetResponseEx(handle)).value)
        except Exception:
            PrintException()
        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)


    # DISPLAY_PLATINFO
    def displayPlatformInfo(self, comport):
        handle = None
        troughAT=False
        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                troughAT=True
            elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                if self.conn.IsSingleFlash():
                    sf=IceraSingleFlashAndroid(self.conn.adb.path, comport, verbosity=self.verboseLevel, check_adb=False)
                    err,folder=sf.GetPlatformFiles()
                    if not err:
                        # Check platfrom config file
                        if os.path.isfile(os.path.join(folder, 'platformConfig.xml')):
                            f=open(os.path.join(folder, 'platformConfig.xml'))
                            plat=f.read()
                            f.close()
                            print 'PLATCFG content:'
                            print plat
                        else:
                            print 'ERROR: No platform config file available.'
                        # Check all wrapped files:
                        wrapped_list = []
                        os.path.walk(folder, SearchAndGetFiles, ['.wrapped', wrapped_list])
                        os.path.walk(folder, SearchAndGetFiles, ['.bin', wrapped_list])# Arguments = extension, list
                        for file in wrapped_list:
                            self.GetFileInfo(file)
                else:
                    troughAT=True
            if troughAT:
                error, comport = self._doSwitchInLoaderMode(comport)
                if not error:
                    handle = self.conn.OpenComPort(comport)
                if not handle:
                    builtfile = -1
                else:
                    platcfg = ''
                    mdm = ''
                    ldr = ''
                    self.lib.SendCmd(handle, "AT%%IPLATCFG\r\n")
                    platcfg = (ctypes.c_char_p(self.lib.GetResponseEx(handle)).value)
                    self.lib.SendCmd(handle, "AT%%IEXTHDR=0\r\n")
                    mdm = (ctypes.c_char_p(self.lib.GetResponseEx(handle)).value)
                    self.lib.SendCmd(handle, "AT%%IEXTHDR=3\r\n")
                    ldr = (ctypes.c_char_p(self.lib.GetResponseEx(handle)).value)

                    try:
                        plat_mess = platcfg.split(':')[1].split('\n')[0]
                    except:
                        plat_mess = 'File not found...'
                    print 'Platform Config: %s' % plat_mess

                    try:
                        mdm_cl = mdm.split('changelist -')[1].split('\n')[0]
                    except:
                        mdm_cl = 'File not found'
                    print 'Modem: %s' % mdm_cl

                    try:
                        ldr_cl = ldr.split('changelist -')[1].split('\n')[0]
                    except:
                        ldr_cl = 'File not found'
                    print 'Loader: %s' % ldr_cl

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)

    # DETECT_CHIP_TYPE
    def detectChipType(self, comport, args):
        releaseFiles = args[0]
        file_list = [f for (t,f) in releaseFiles.iteritems() if f!='' and t in ("loader", "factory_tests", "modem")]
        try:
            rsp,error = self._multiCom('DETECT_CHIP_TYPE', comport, file_list)

        except Exception:
            PrintException(verb=self.verboseLevel)
            error=1

        return rsp,error

    # EXTRACT_ARCHIVE
    def ExtractArchiveWrapper(self, args):
        extract_folder = args[0]
        zipsource = args[1]
        progressCB = args[2]
        self.ExtractArchive(extract_folder, zipsource, progressCB)

    # UPDATE_RELEASE
    def _isPkgvUpdate(self, pkgv_file):
        if FileExist(os.path.dirname(pkgv_file),os.path.basename(pkgv_file)):
            file_package = open(pkgv_file,'r')
            pkgv_lines = [line.rstrip('\r\n') for line in file_package.readlines()]
            file_package.close()
            params = len(pkgv_lines)

            if params == 0:
                print 'WARNING: PKGV file contains no data: %s' % pkgv_file
                return True # this should only be a warning, not an error
            if params > 0 and len(pkgv_lines[0]) > 16:
                print 'WARNING: Package version line too long (max 16 characters): %s' % pkgv_lines[0]
                return False
            if params > 1 and len(pkgv_lines[1]) > 20:
                print 'WARNING: Package date line too long (max 20 characters): %s' % pkgv_lines[1]
                return False
            if params > 2 and (len(pkgv_lines[2])>0 and (not pkgv_lines[2].isdigit() or int(pkgv_lines[2]) > 99)):
                print 'WARNING: Package SVN is not correct (0-99): %s' % pkgv_lines[2]
                return False
            if params > 3 and (len(pkgv_lines[3])>0 and (not pkgv_lines[3].isdigit() or int(pkgv_lines[3]) > 2)):
                print 'WARNING: Package fullcoredumpSetting is not correct (0-2): %s' % pkgv_lines[3]
                return False
            if params > 4:
                print 'WARNING: PKGV file contains more than 4 lines: %s' % pkgv_file

        return True

    def _checkXmlFileContent(self, file, doctype, file_pattern=None, config_pattern=None):
        ok = False
        fd = open(file, 'r')
        lines = fd.readlines()
        fd.close()

        # --> to remove one day...
        # TODO: remove below lines as soon as all .xml files are correctly formatted...
        #       correct format: one (and only one) tag <!DOCTYPE .... > in .xml source
        if file_pattern:
            if os.path.basename(file).lower().find(file_pattern)==-1: return False
        if config_pattern:
            if config_pattern in lines[0]: return True
            if config_pattern in lines[1]: return True
        # <--- to remove one day...

        for line in lines:
            if 'DOCTYPE' in line:
                if doctype in line:
                    ok = True
                break

        return ok

    def _isDeviceConfigFile(self, file):
        return self._checkXmlFileContent(file, 'deviceConfig', file_pattern='device', config_pattern='CustomerConfig')

    def _isProductConfigFile(self, file):
        return self._checkXmlFileContent(file, 'productConfig', file_pattern='product', config_pattern='CustomerConfig')

    def _isAudioConfigFile(self, file):
        return self._checkXmlFileContent(file, 'AudioConfig', file_pattern='audio', config_pattern='AudioParamFile')

    def IsReleasePackageOk(self, package_path=None, list=None, files=None, fwid='', unlockBoard=''):
        ''' Check all files are present, valid and not duplicated. Input can be package_path/list or files '''
        ans = 1
        productCfg_count=0
        productCfg = None
        xml_list = []
        wrapped_list = []
        pkgv_list = []
        chipFW = None
        prodFW = None
        if files:
            error_msg = u'file was found twice in the file list: {0}'.format(files)
        else:
            error_msg = u'file was found twice in the path: {0}'.format(package_path)

        releaseFiles={WRAPPEDNAMES['DEVICECFG']:""
        ,WRAPPEDNAMES['PRODUCTCFG']:""
        ,WRAPPEDNAMES['AUDIOCFG']:""
        ,WRAPPEDNAMES['LDR']:""
        ,WRAPPEDNAMES['BT2']: ""
        ,WRAPPEDNAMES['BT3']: ""
        ,WRAPPEDNAMES['IFT']:""
        ,WRAPPEDNAMES['MDM']:""
        ,"pkgv":""}

        try:
            # Look for .wrapped files
            if files:
                wrapped_list = [w for w in files if w.endswith(('.bin','.wrapped'))]
            else:
                os.path.walk(package_path, SearchAndGetFiles, ['.wrapped', wrapped_list])
                os.path.walk(package_path, SearchAndGetFiles, ['.bin', wrapped_list])# Arguments = extension, list
            for file in wrapped_list:
                if os.path.basename(file)!='bt1_5.wrapped':
                    # Above test is  a dirty temporary way to avoid BT2 duplication detection
                    # TO BE REMOVED, in a while...
                    # ReadArchiveIdAndChip extract data from file's header
                    arch_id, chip, prod = ReadArchiveIdAndChip(file=file, chip=self.chip, prodChecked=True)
                    if arch_id == -1:
                        print 'ERROR: what is this file ?: {0}'.format(file)
                        ans=-1
                        break
                    else:
                        prop=const.GetArchPropById(arch_id)
                        if (not list or list[prop.acr] == True) and prop.acr != 'PRODUCTCFG':
                            if releaseFiles[WRAPPEDNAMES[prop.acr]] != "":
                                print 'ERROR: {0} {1}'.format(prop.acr,error_msg)
                                ans=-1
                            else: releaseFiles[WRAPPEDNAMES[prop.acr]]=file

                        if (not list or list[prop.acr] == True) and prop.acr == 'PRODUCTCFG':
                            #If AT%IGETFWID return a value
                            if fwid != '':
                                # Read FWID from productConfig file
                                (err,prodCFG_fwid) = productCfgFWID(file)
                                if err != 0:
                                    ans=err
                                #Modem FWID and productionCfg FWID are matching
                                if fwid == prodCFG_fwid :
                                    #Only one productCfg is matching => flash
                                    if releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "":
                                        releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = file
                                        #We found the good productCfg => reset the counter as it is no longer needed
                                        productCfg_count = 0
                                    #Several productCfg are matching => ERROR
                                    else:
                                        print 'ERROR: PRODUCTCFG '+error_msg
                                        ans=-1
                                # No FWID returned from productCfg and ProductCfg not choosen yet,
                                elif releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "":
                                    productCfg_count +=1
                                    productCfg = file  
                            #No Fwid returned by the board => count the number of productCfg
                            else:
                                productCfg_count +=1
                                productCfg = file

                        if list[prop.acr] and not unlockBoard:
                            if chipFW:
                                if chipFW!=chip:
                                    print 'ERROR: File ({0}) for {1} is inconsistent with rest of the package'.format(file, chip)
                                    ans=-1
                            else:
                                chipFW=chip
                            if prodFW and self.enable_krm:
                                if prod: # ISO is not signed
                                    if prodFW!=prod:
                                        print 'ERROR: File ({0}) signed for {1} is inconsistent with rest of the package'.format(file, prod)
                                        ans=-1
                            else:
                                prodFW=prod
                                
            if releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "" and productCfg_count == 1:
                if fwid != '':
                    (err,prodCFG_fwid) = productCfgFWID(productCfg)
                    val = RistrettoFrameShare.PopUpYesOrNo("FWID is not matching \nAre you OK to change it from {0} to {1}?\n".format(fwid, prodCFG_fwid), caption='Confirm FWID...')
                    if val == wx.ID_YES:
                        releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = productCfg
                    else:
                        print 'ERROR: Product Config file matching with FWID:{0} not found in {1}'.format(fwid, package_path)
                        ans=-1
                else:
                    releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = productCfg
            # Look for .xml config files
            if files:
                xml_list = [w for w in files if w.endswith('.xml')]
            else:
                os.path.walk(package_path, SearchAndGetFiles, ['.xml', xml_list]) # Arguments = extension, list

            for file in xml_list:
                if self._isDeviceConfigFile(file) and (not list or list["DEVICECFG"] == True)\
                and not releaseFiles[WRAPPEDNAMES['DEVICECFG']].endswith(('.bin','.wrapped')):
                    if releaseFiles[WRAPPEDNAMES['DEVICECFG']] != "":
                        print 'ERROR: DEVICECFG '+error_msg
                        ans=-1
                    else: releaseFiles[WRAPPEDNAMES['DEVICECFG']] = file
                    
                if self._isAudioConfigFile(file) and (not list or list["AUDIOCFG"] == True)\
                and not releaseFiles[WRAPPEDNAMES['AUDIOCFG']].endswith(('.bin','.wrapped')):
                    if releaseFiles[WRAPPEDNAMES['AUDIOCFG']] != "":
                        print 'ERROR: AUDIOCFG '+error_msg
                        ans=-1
                    else: releaseFiles[WRAPPEDNAMES['AUDIOCFG']] = file

                #ProductCfg is selected to be flashed and this file is one
                if self._isProductConfigFile(file) and (not list or list["PRODUCTCFG"] == True)\
                and not releaseFiles[WRAPPEDNAMES['PRODUCTCFG']].endswith(('.bin','.wrapped')):
                    #If AT%IGETFWID return a value
                    if fwid != '':
                        # Read FWID from productConfig file
                        (err,prodCFG_fwid) = productCfgFWID(file)
                        if err != 0:
                            ans=err
                        #Modem FWID and productionCfg FWID are matching
                        if fwid == prodCFG_fwid :
                            #Only one productCfg is matching => flash
                            if releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "":
                                releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = file
                                #We found the good productCfg => reset the counter as it is no longer needed
                                productCfg_count = 0
                            #Several productCfg are matching => ERROR
                            else:
                                print 'ERROR: PRODUCTCFG '+error_msg
                                ans=-1
                        # No FWID returned from productCfg and ProductCfg not choosen yet,
                        elif releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "":
                            productCfg_count +=1
                            productCfg = file

                    #No Fwid returned by the board => count the number of productCfg
                    else:
                        productCfg_count +=1
                        productCfg = file

            #No productCfg file is matching with modem fwid and only one productCfg file found in package => PopUp
            if releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "" and productCfg_count == 1:
                if fwid != '':
                    (err,prodCFG_fwid) = productCfgFWID(productCfg)
                    val = RistrettoFrameShare.PopUpYesOrNo("FWID is not matching \nAre you OK to change it from {0} to {1}?\n".format(fwid, prodCFG_fwid), caption='Confirm FWID...')
                    if val == wx.ID_YES:
                        releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = productCfg
                    else:
                        print 'ERROR: Product Config file matching with FWID:{0}  not found in {1}'.format(fwid, package_path)
                        ans=-1
                else:
                    releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = productCfg
            #Several productionCfg in package, none of them is matching with modem FWID => ERROR
            elif releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == "" and productCfg_count > 1:
                print 'ERROR: Several productCfg found in release package'
                print 'Please select one productCfg in release package'
                RistrettoFrameShare.PopUpInfo("Fail to find to right product Config\n\
Please select one manually")
                
                dlg = wx.FileDialog(None, message='Product config', defaultDir=package_path,
                            defaultFile="", wildcard="*.xml;*.wrapped;*.bin", style=wx.OPEN)
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.Destroy()
                    releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] = dlg.GetPath()
                    self.defaultDir = os.path.dirname(file)
                else:
                    dlg.Destroy()
                    print 'ERROR: No productCfg selected. Abort flashing.'
                    ans=-1
                   

            # Look for .pkgv file
            if files:
                pkgv_list = [w for w in files if w.endswith('.pkgv')]
            else:
                os.path.walk(package_path, SearchAndGetFiles, ['.pkgv', pkgv_list]) # Arguments = extension, list
            if len(pkgv_list) > 1:
                print "WARNING. Found multiple package version. Package version ignored."
            else:
                if len(pkgv_list) == 1:
                    file = pkgv_list[0]
                    if self._isPkgvUpdate(file):
                        releaseFiles['pkgv'] = file
                    else:
                        print "WARNING. Errors in package version file %s. Package version ignored." % file

            # Check all required files
            if list:
                if list["BT2"] and releaseFiles[WRAPPEDNAMES['BT2']] == '':
                    print 'ERROR: BT2 not found in %s' % package_path
                    ans = 0
                if list["BT3"] and releaseFiles[WRAPPEDNAMES['BT3']] == '':
                    print 'ERROR: BT3 not found in %s' % package_path
                    ans = 0
                if list["LDR"] and releaseFiles[WRAPPEDNAMES['LDR']] == '':
                    print 'ERROR: LDR not found in %s' % package_path
                    ans = 0
                if list["MDM"] and releaseFiles[WRAPPEDNAMES['MDM']] == '':
                    print 'ERROR: MDM not found in %s' % package_path
                    ans = 0
                if (list["DEVICECFG"] and releaseFiles[WRAPPEDNAMES['DEVICECFG']] == ''):
                    print 'ERROR: Device Config file not found in %s' % package_path
                    ans = 0
                if (list["PRODUCTCFG"] and releaseFiles[WRAPPEDNAMES['PRODUCTCFG']] == ''):
                    print 'ERROR: Product Config file not found in %s' % package_path
                    ans = 0
                if list["AUDIOCFG"] and releaseFiles[WRAPPEDNAMES['AUDIOCFG']] == '':
                    print 'ERROR: AUDIOCFG not found in %s' % package_path
                    ans = 0

        except Exception:
            PrintException(verb=self.verboseLevel)
            ans = 0

        finally:
            if IceraToolbox.IsWindows():
                for file,path in releaseFiles.items():
                    if path != '' :
                        path=win32api.GetShortPathName(path).encode('utf-8')
                        releaseFiles[file] = path
            return ans, releaseFiles, chipFW, prodFW

    def releaseUpdate(self, comport, sock_port, args, check=True, releaseFiles={}):
        rsp = 0
        error = 0
        ans = 1
        fwid = ""
        unlockBoard=True
        sock_port=sock_port
        releaseFiles=releaseFiles
        handle=0

        release_path = args[0]
        release_list = args[1]
        if len(args)>2: check = args[2]
        if len(args)>3: releaseFiles = args[3]

        try:
            if check == False and len(releaseFiles) == 0:
                error = 1
                print 'ERROR. Bad function usage'
                
            if check:
                (unlockBoard, noModem, error)=self.isBoardUnlocked(comport,sock_port)

                if not noModem:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        if not self.conn.IsSingleFlash(comport):
                            handle = self.conn.OpenComPort(sock_port, cb=False)
                            if handle == 0:
                                print 'ERROR. Thread %s, opening %s' % (self.getName(), sock_port)
                                self.error = 1
                            else:
                                # Register handle callback
                                CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
                                c_callback = CFUNC(self.updaterlibCb)
                                self.lib.SetLogCallbackFuncEx(handle, c_callback)
                            isf=IceraDualFlashAndroid(self.conn.adb.path, self.adb.devices[0], check_adb=False, handle=handle, UpdaterLib=self.lib)
                        else:
                            isf=IceraSingleFlashAndroid(self.conn.adb.path, self.adb.devices[0], check_adb=False)
                        (err,fwid)=isf.readFWID()
                        if err > 0:
                            val = RistrettoFrameShare.PopUpYesOrNo("Failed to read FWID from modem \nAre you sure you want to continue to flash ?", caption='Confirm Flashing...')
                            if val != wx.ID_YES:
                                error = err
                        if handle:
                            self.conn.CloseComPort(handle, sock_port)
                    else:
                        handle = self.conn.OpenComPort(comport, cb=False)
                        if handle == 0:
                            print 'ERROR. Thread %s, opening %s' % (self.getName(), sock_port)
                            self.error = 1
                        else:
                            # Register handle callback
                            CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
                            c_callback = CFUNC(self.updaterlibCb)
                            self.lib.SetLogCallbackFuncEx(handle, c_callback)
                        (err,fwid)=readFWID(self.lib,handle)
                        if err > 0:
                            val = RistrettoFrameShare.PopUpYesOrNo("Failed to read FWID from modem \nAre you sure you want to continue to flash ?", caption='Confirm Flashing...')
                            if val != wx.ID_YES:
                                error = err
                        if handle:
                            self.conn.CloseComPort(handle, sock_port)
                    
                if error == 0:
                    # Check release package is OK.
                    if IceraToolbox.IsWindows():
                        (ans, releaseFiles, chipFW, prodFW) = self.IsReleasePackageOk(win32api.GetShortPathName(release_path), release_list, fwid=fwid, unlockBoard=unlockBoard)
                    else:
                        (ans, releaseFiles, chipFW, prodFW) = self.IsReleasePackageOk(release_path, release_list, fwid=fwid, unlockBoard=unlockBoard)                    

            if error == 0:
                self.log.DisplayStatus('Platform update in progress...')
                if ans == 1:
                    rsp,error = self._multiCom('RELEASE', comport, sockport=sock_port, file_list=releaseFiles)
                else:
                    error = 1
                    print 'ERROR: Incomplete/Invalid release package'

        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)

        finally:
            if error:
                self.log.DisplayStatus('Platform update failure')
            else:
                self.log.DisplayStatus('Platform update successful')
            return rsp,error


    def updaterlibCb(self, msg):
        # UpdaterLib callback handler.
        self.msg = RistrettoCommon.ParseAndDispMsg(self.msg, msg)
        return 0
        
    def updaterlibMuteCb(self,msg):
        #Mute any output from the Updater lib
        return 0


    # SCAN_TARGET
    def scanTarget(self):
        if self.hif:
            self.hif.mdmPortList = None
        elif self.adb:
            self.adb.devices=[]
        self.disCb()
        self.conn.Scan()
        self.updCb()

    # FILE_UPDATE
    def singleFileUpdate(self, comport, sock_port, fileToUpdate):
        file = None
        archID = -1
        error = 0

        try:
            file = fileToUpdate

            #Convert release_path to ShortPathName in order to handle non-latin characters
            if IceraToolbox.IsWindows():
                file = win32api.GetShortPathName(file).encode('utf-8')

            # Start file programming
            self.log.DisplayStatus('Platform update in progress...')
            if fileToUpdate.endswith('.icz') or fileToUpdate.endswith('.ICZ'):
                # This is an archive file that is supposed to contain valid unlock certificates.
                # Let's call unlock_board to handle such a file.
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB and not self.conn.forwarded:
                    print 'ERROR: You need to perform a port forwarding to unlock this platform.'
                    error=1
                else:
                    rsp,error = self._multiCom('UNLOCK_BOARD', comport, sockport=sock_port, file_list=file)
            else:
                # Perform single file update.
                archID, chip, prod = ReadArchiveIdAndChip(file, self.chip)
                if archID != -1:
                    print '\nWill update platform(s) with %s.\n' % fileToUpdate
                    rsp,error = self._multiCom('FILE', comport, sockport=sock_port, file_list=file)
                else:
                    error = 1

        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)

        finally:
            if error:
                if fileToUpdate:
                    print 'ERROR updating %s...\n' % fileToUpdate
                self.log.DisplayStatus('File update failure...')
            else:
                self.log.DisplayStatus('Platform update finished...')

    # START_UART_SERVER
    def startUartServerForDiscovery(self, args):
        error = 0
        comport = args[1]

        try:
            self.log.DisplayStatus('UART server started on %s'  % comport)

            # No flow control
            flowControl = self.hif.flowControl
            self.hif.flowControl = 0

            self.uartDiscoveryServerHandle = self.hif.OpenComPort(str(comport))
            if self.uartDiscoveryServerHandle:
                self.lib.UartDiscoveryServer(self.uartDiscoveryServerHandle, comport, self.verboseLevel)
            else:
                error = 1

        except Exception:
            error = 1
            PrintException()

        finally:
            self.hif.flowControl = flowControl
            if self.uartDiscoveryServerHandle:
                self.hif.CloseComPort(self.uartDiscoveryServerHandle, comport)
                if self.uartDiscoveryAborted == False:
                    self.log.DisplayStatus('Platform now connected on %s' % comport)
            if error:
                self.log.DisplayStatus('UART server failure.')
            self.uartDiscoveryServerHandle = None
            return error

    def startUartServerForBoardRepair(self, args):
        error = 0
        gauge_value = 0
        uartBt2ToSend = args[1]
        uartAppliToSend = args[2]
        uartComPort = args[3]
        gauge = args[4]
        # No flow control
        flowControl = self.hif.flowControl
        self.hif.flowControl = 0
        # Baudrates might change during boot operation, keep a trace:
        baudrate = self.hif.baudrate

        try:
            gauge.SetValue(1)
            (status, hdr, ext_hdr_bin, zipped) = ReadHeader(uartAppliToSend, self.chip)
            if status == -1:
                print 'ERROR. Invalid application.'
                error = 1
            if zipped:
                if float(self.libversion) >= 8.08:
                    print 'Warning. Compressed application found: may not work properly.'
                else:
                    print 'ERROR. Compressed application found: not supported.'
                    error = 1

            if error == 0:
                self.log.DisplayStatus('Acquiring BT2...')

                # Check we have selected a BT2: read & validate header.
                gauge.SetValue(2)
                arch_id, chip, prod = ReadArchiveIdAndChip(uartBt2ToSend, self.chip)
                if arch_id != 1:
                    error = 1
                    print 'ERROR. Invalid header information: select a valid BT2.'
                else:
                    # Apply baudrate to use to communicate with BROM:
                    self.hif.baudrate = self.hif.bromBaudrate
                    # Open COM port
                    self.boardRepairUartServerHandle = self.hif.OpenComPort(str(uartComPort), block_size=self.hif.bootUartBlockSize)
                    gauge.SetValue(3)
                    if self.boardRepairUartServerHandle:
                        self.lib.UartFileServer(self.boardRepairUartServerHandle, uartBt2ToSend, str(uartComPort), self.verboseLevel)
                        gauge.SetValue(20)
                        if self.boardRepairUartServerHandle:
                            # Close COM port
                            self.hif.CloseComPort(self.boardRepairUartServerHandle, str(uartComPort))
                            # Apply baudrate to use to communicate with appli:
                            self.hif.baudrate = self.hif.appBaudrate
                            # Re-open COM port
                            self.boardRepairUartServerHandle = self.hif.OpenComPort(str(uartComPort), block_size=self.hif.bootUartBlockSize)
                            gauge.SetValue(30)
                            if self.boardRepairUartServerHandle:
                                self.log.DisplayStatus('Acquiring appli...')
                                self.lib.UartFileServer(self.boardRepairUartServerHandle, uartAppliToSend, str(uartComPort), self.verboseLevel)
                                gauge.SetValue(100)
                            else:
                                error = 1
                                self.log.DisplayStatus('Boot sequence stopped...')
                        else:
                            error = 1
                            self.log.DisplayStatus('Boot sequence stopped...')
                    else:
                        error = 1

        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)

        finally:
            self.hif.flowControl = flowControl
            self.hif.baudrate = baudrate
            if self.boardRepairUartServerHandle:
                self.hif.CloseComPort(self.boardRepairUartServerHandle, str(uartComPort))
                if self.bootRepairFromUartAborted == False:
                    self.log.DisplayStatus('Successfull boot sequence')

            if error:
                gauge.SetValue(0)
                self.log.DisplayStatus('Boot sequence failure')
            self.boardRepairUartServerHandle = None
            return error

    def startUartServer(self, args):
        error = 0

        try:
            if args[0] == 'DISCOVERY':
                error = self.startUartServerForDiscovery(args)
            elif args[0] == 'BOARD_REPAIR':
                error = self.startUartServerForBoardRepair(args)
        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)
        finally:
            return error


    # STOP_UART_SERVER
    def stopUartServer(self, args):
        comport = args[1]
        try:
            handle = None
            if args[0] == 'DISCOVERY':
                handle = self.uartDiscoveryServerHandle
                self.uartDiscoveryServerHandle = None
            elif args[0] == 'BOARD_REPAIR':
                handle = self.boardRepairUartServerHandle
                self.boardRepairUartServerHandle = None
            if handle:
                self.lib.UartStopServer(handle)

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.hif.CloseComPort(handle, comport)
            if args[0] == 'DISCOVERY':
                self.uartDiscoveryAborted = True
            elif args[0] == 'BOARD_REPAIR':
                self.bootRepairFromUartAborted = True

    # SET_HIF_TYPE
    def setHifType(self, comport, args):
        handle = None
        err = 1
        rsp = None
        try:
            if self.hif.hifType != None:
                error, comport = self._doSwitchInLoaderMode(comport)
                if not error:
                    handle = self.hif.OpenComPort(comport)
                if handle:
                    cmd="AT%%IHIFTYPE=%d" % self.hif.hifType
                    if cmd:
                        rsp = SendAtCmd(self.lib, handle, cmd)
                        if rsp:
                            if not AT_RSP_ERROR in rsp:
                                err = 0
                                print "Set HIF: %s" % RistrettoCommon.HIF_TYPE[self.hif.hifType]
                                print "\nWARNING: Will apply on next platform reset"
                                if RistrettoCommon.HIF_TYPE[self.hif.hifType] == 'UART':
                                    print "WARNING: Please, remember auto-detect COM port must be disabled to work with UART."
                                print '\n'
            else:
                print 'ERROR: Please select a valid HIF type...'

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if rsp == None:
                print "ERROR. HIF not modified.\n"
            if handle:
                self.hif.CloseComPort(handle, comport)

    #CHECK_LOCK_TYPE
    def checkLockType(self, comport):
        rsp = None
        try:
            handle = self.conn.OpenComPort(comport)
            CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
            self.c_callback = CFUNC(self.updaterlibMuteCb)
            self.lib.SetLogCallbackFuncEx(handle, self.c_callback)
            if handle:
                at_rsp=SendAtCmd(self.lib, handle, str('AT%IPROD'), disp=False)
                rsp = re.search("IPROD:\ Chip\ version:\ *([\w\s]*)\ *OK\ *", at_rsp).group(1)
                rsp = re.search("([^\n\r]*)",rsp).group(1)
        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)
            return rsp
            
    #CHECK_PCID
    def checkPCIDWrapper(self,comport):
        rsp = None
        err=0
        try:
            handle = self.conn.OpenComPort(comport)
            CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
            self.c_callback = CFUNC(self.updaterlibMuteCb)
            self.lib.SetLogCallbackFuncEx(handle, self.c_callback)
            if handle:
                PCID=readPCID(handle, self.lib, verbosity=0)
                if PCID==None:
                    #no value return
                    err=1
        except Exception:
            PrintException(verb=self.verboseLevel)
            err=1

        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)
                rsp=PCID
            return rsp,err
            
    def checkUnlockFileOnServer(self,pcid):
        err=0
        url_base='http://netapp-fr/mobile/Icera_share/Modem_tools/Unlock_certificates'
        try:
            response=urllib2.urlopen(url_base, timeout=120).read()
        except:
            dlg = LoginDialog()
            dlg.ShowModal()
            
        try:
            response=urllib2.urlopen(url_base, timeout=120).read()
        except urllib2.HTTPError, e:
            print "HTTP Error {0}".format(e.code)
            print e.msg
            err=1
            return err
            
        search_result=re.search('(unlock_'+str(pcid)+'\.bin)',response)
        if search_result:
            val = RistrettoFrameShare.PopUpYesOrNo("Unlock certificate for your platform (PCID= {0}) was found\n Do you want to flash it?".format(pcid), caption='Confirm unlock certificate usage...')
            if val == wx.ID_YES:
                unlock_filename=search_result.group(1)
                print "try to open/read: {0}".format(url_base+'/'+unlock_filename)
                try:
                    response = urllib2.urlopen(url_base+'/'+unlock_filename)
                except:
                    print "Unable to download {0}".format(url_base+'/'+unlock_filename)
                    err=1
                        
                handle = open(unlock_filename, 'wb')
                print "Downloading {0}".format(unlock_filename)
                handle.write(response.read())
                handle.close()
        else:
            err=1
            print "unlock_{0}.bin was not found".format(pcid)
            if IceraToolbox.IsWindows():
                val = RistrettoFrameShare.PopUpYesOrNo("Unlock certificate was not found\nDo you want to generate a request?", caption='Confirm unlock certificate request...')
                if val == wx.ID_YES:
                    fw = open("tmpout", "wb")
                    fr = open("tmpout", "r")
                    dlg = wx.TextEntryDialog(None, "Add comment to your unlock certificate request (project, purpose, urgency, ...)", defaultValue=' ')
                    dlg.ShowModal()
                    result = dlg.GetValue()
                    dlg.Destroy()
                    print "Launching Register_device_info -- Please wait"
                    register_info_script=os.path.join(IceraToolbox.BASE_PATH,'androidDevTools','x86','Register_device_info.bat')
                    p = subprocess.Popen(register_info_script, shell=True, stdin = subprocess.PIPE, stdout = fw, stderr = fw, bufsize = 1)
                    p.stdin.write(result)
                    
                    p.stdin.close()
                    fw.close()
                    
                    p.wait()
                    for out in fr.readlines():
                        print out
                    fr.close()
                    os.remove("tmpout")
                
        return err
            

    # LAUNCH_AT_CMD
    def launchAtCommand(self, comport, args):
        '''Can launch a list of AT command and return the result'''
        atCmd=args[0]
        sock_port=args[1]
        handle=None
        if type(atCmd) in [type(""),type(u"")]: singleCmd=True
        else: singleCmd=False
        if singleCmd: atCmd=[atCmd] # backward compatibility
        rsp = None
        err=0
        try:
            if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                comport = sock_port
            handle = self.conn.OpenComPort(comport)
            if handle:
                rsp=[]
                for cmd in atCmd:
                    rsp.append(SendAtCmd(self.lib, handle, str(cmd)))

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.conn.CloseComPort(handle, comport)

            if rsp:
                if singleCmd and rsp[0]: rsp=rsp[0]
            return rsp

    # GET_MEMORY_DUMP
    def getMemoryDump(self, comport, gangimagefile):
        handle = None

        try:
            error, comport = self._doSwitchInLoaderMode(comport,recovery=True)
            if not error:
                handle = self.hif.OpenComPort(comport)
            if handle:
                error, old_manner = MemDump(self.lib, handle, gangimagefile)
                if error == 0:
                    if not old_manner:
                        print 'Start dump decoding.'
                        error = MemDumpDecoder(gangimagefile, self.verboseLevel)

        except Exception:
            PrintException(verb=self.verboseLevel)

        finally:
            if handle:
                self.hif.CloseComPort(handle, comport)

    # DECODE_MEMORY_DUMP
    def decodeMemoryDump(self, gangimagefile):
        try:
            print 'Start dump decoding.'
            MemDumpDecoder(gangimagefile, self.verboseLevel)
        except Exception:
            PrintException()

    # STOP_WAIT_PNPEVENT
    def stopPnpEvent(self):
        self._stopPnpEvent()

    # CONFIGURATION FILES
    def prepareAndProgramConfigFile(self, type, comport, sockport, source):
        self.log.DisplayStatus('Configuration file update on going...')
        error = 0
        try:
            rsp,error = self._multiCom('CONFIG FILE', comport, xml_type=type, sockport=sockport, source=source)
        except Exception:
            PrintException()
        finally:
            if error:
                self.log.DisplayStatus('%s update failure...' % type)
            else:
                self.log.DisplayStatus('%s update successful.' % type)
            return error

    # PROGRAM_XML
    def programXmlCfg(self, comport, sock_port, args):
        xml_type = args[0]
        xml_source = args[1]
        print 'Start %s generation.' % xml_type
        return self.prepareAndProgramConfigFile('%s' % xml_type, comport, sock_port, xml_source)

    # PROGRAM_IMEI
    def programImei(self, comport, sock_port, imei):
        if comport:
            portList = [comport]
        else:
            if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                portList = self.hif.mdmPortList
            elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                portList = self.adb.devices
        if len(portList) > 1:
            print 'ERROR: Cannot program the same IMEI on multiple platforms.'
        else:
            print 'Start imei file generation'
            self.prepareAndProgramConfigFile('IMEI', comport, sock_port, imei)

    # PROGRAM_CALIB
    def programCalibrationFiles(self, comport, sockport, raw_cal_file):
        print 'Start calibration files update'
        error = 0

        try:
            # Build a calibration file: signed with OEM-FACT but without PCID
            ofile = raw_cal_file + '.wrapped'
            buildargs = ['-c', self.chip]
            buildargs.append('-a')
            buildargs.append('CALIB')
            buildargs.append('-i')
            buildargs.append(raw_cal_file)
            buildargs.append('-o')
            buildargs.append(ofile)
            buildargs.append('-k')
            buildargs.append(self.keys[const.ARCH_OEM_FACT_KEY_SET]['path'])
            if self.keys[const.ARCH_OEM_FACT_KEY_SET]['secret'] == False:
                print 'ERROR. % do not allow to sign data file' % self.keys[const.ARCH_OEM_FACT_KEY_SET]['path']
                error = 1
                
            if error != 1:
                if self.verboseLevel>IceraToolbox.VERB_INFO: print buildargs
                BuildIceraFile(buildargs, self.lib)

                if comport:
                    portList = [comport]
                else:
                    if self.conn.mode==RistrettoCommon.RISTRETTO_HIF:
                        portList = self.hif.mdmPortList
                    elif self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                        portList = self.adb.devices
                if len(portList) > 1:
                    print 'ERROR: Cannot program the same calibration file on multiple platforms.'
                    error = 1
                else:
                    # Program file in flash:
                    self.singleFileUpdate(comport, sockport, ofile)

        except Exception:
            error = 1
            PrintException(verb=self.verboseLevel)

        finally:
            if error:
                print 'ERROR. Fail to update calibration successfully on this platform.'
                self.log.DisplayStatus('calibration update failure' %  type)
            return error

    # GET_ARCH_INFO
    def GetDirInfo(self, dir, dispCb):
        file_list = []
        num_of_file = 0
        dispCb('Checking %s...' % dir)
        os.path.walk(dir, SearchAndGetFiles, ['*', file_list]) # Arguments = extension, list
        num_of_file = len(file_list)
        for file in file_list:
            if (os.path.isdir(file) != 0):
                # it is a directory certainly due to some zip extraction...
                file_list.remove(file)
                num_of_file -= 1
        dispCb('\nFound %d file(s):' % num_of_file)
        for file in file_list:
            dispCb(file+'\n')

        for file in file_list:
            self.GetFileInfo(file, dispCb)

    def GetFileInfo(self, file, dispCb=PrintCb):
        ans = 0
        status = 0
        dispCb('\n##########\nFile  %s...' % file)
        if IceraToolbox.IsWindows():
            file=win32api.GetShortPathName(file)
        try:
            # Read header:
            (status, hdr, ext_hdr_bin, zipped) = ReadHeader(file, self.chip, cb=dispCb)

            if status != -1:
                hdr_size = hdr[1]
                file_size = hdr[2]
                entry_addr = hdr[3]
                arch_id = hdr[4] & ~const.ZIP_MODE_MASK
                sign_type = hdr[5]

                # Define arch_type
                signed = False
                bootmap = False
                asn1_spec = ''
                extended_header = False
                prop=const.GetArchPropById(arch_id)
                if hdr_size > const.ARCH_HEADER_BYTE_LEN:
                    extended_header = True
                arch_type=prop.acr
                if arch_id <= 3: # BT2/LDR/IFT/MDM
                    if arch_id == 1: # BT2
                        bootmap = True
                    signed = True
                elif arch_id == 4: # IMEI
                    signed = True
                elif arch_id == 8:
                    asn1_spec = 'AUDIO_CFG'
                elif arch_id == 10:
                    asn1_spec = 'PLAT_CFG'
                elif arch_id == 13:
                    signed = True
                elif arch_id == 15:
                    signed = True
                elif arch_id == 16:
                    signed = True
                elif arch_id == 17:
                    signed = True
                elif arch_id == 21: # BT3
                    signed = True
                else:
                    dispCb('Not supported archive with arch ID: %d' % arch_id)
                    return
                if self.conn.mode==RistrettoCommon.RISTRETTO_ADB:
                    if self.conn.IsSingleFlash():
                        if arch_type == const.ARCH_ACR_LDR:
                            arch_type=const.ARCH_ACR_BT3
                dispCb('%s file' % arch_type)
                if zipped:
                    dispCb('Zipped archive')

                # Check SHA/RSA sig if required
                if signed:
                    keyID, nonce, rsaSign = ReadFooter(file)
                    if prop.key_set != const.ARCH_NO_AUTH:
                        key_path=self.keys[prop.key_set]['path']
                        ans = rsa_sign_icera.RSAVerifyFile(file, key_path, reverse=((self.chip=="9040") or (self.chip=="9140")))
                        if ans == 0:
                            for key in self.prod_keys:
                                if rsa_sign_icera.KeyIdMatching(hex(keyID), key['path']):
                                    key_path = key['path']
                                    break
                            ans = rsa_sign_icera.RSAVerifyFile(file, key_path, reverse=((self.chip=="9040") or (self.chip=="9140")))
                            if ans == 0:
                                dispCb('\nERROR: RSA authentication failure.')
                                dispCb('Fail to authenticate using %s.' % key_path)
                            else:
                                dispCb('\nSHA/RSA authenticated with %s' % key_path)
                        else:
                            dispCb('\nSHA/RSA authenticated with %s' % key_path)

                # Display extended header content when available:
                if extended_header:
                    ext_hdr = DecodeExtendedHeader(file)
                    dispCb('\nExtended Header:')
                    for i in ext_hdr.splitlines():
                        dispCb('%s' % i)

                # Display IMEI value if IMEI file
                if arch_id == 4:
                    fd  = open(file, 'rb')
                    fd.seek(hdr_size)
                    imei_bin =  fd.read(const.IMEI_LENGTH)
                    imei = struct.unpack("<%dB" % const.IMEI_LENGTH, imei_bin)
                    disp = ''
                    for i in imei:
                        disp = disp+'%d' % i
                    dispCb('\nIMEI: %s' % disp.upper())
                    fd.close()


                # Display PCID if a known data file type & signed...
                try:
                    self.ppid_check=prop.ppid_check
                except ValueError:
                    self.ppid_check=prop.pcid_check
                if self.ppid_check:
                    if signed:
                        pcid_offset = (hdr_size
                        + file_size
                        - const.RSA_SIGNATURE_SIZE
                        - const.NONCE_SIZE
                        - const.KEY_ID_BYTE_LEN
                        - const.SHA1_DIGEST_SIZE )
                        if pcid_offset < 0:
                            signed = False
                        else:
                            fd  = open(file, 'rb')
                            fd.seek(pcid_offset)
                            pcid_bin =  fd.read(const.SHA1_DIGEST_SIZE)
                            pcid = struct.unpack("<%dB" % const.SHA1_DIGEST_SIZE, pcid_bin)
                            disp = ''
                            for i in pcid:
                                if i < 16:
                                    disp = disp+'0%x' % i
                                else:
                                    disp = disp+'%x' % i
                            dispCb('\nPCID: %s' % disp.upper())
                            fd.close()

                if signed:
                    # Read keyID
                    dispCb('\nKey ID: 0x%x' % keyID)

                    # Read nonce
                    dispCb('\nNonce: %s' % self.displayByteFromBin(fd=None, len=const.NONCE_SIZE, bin=nonce))

                    # Read signature
                    dispCb('\nRSA sig: %s' % self.displayByteFromBin(fd=None, len=const.RSA_SIGNATURE_SIZE, bin=rsaSign))


                siglen=0
                if signed:
                    siglen+=const.RSA_SIGNATURE_SIZE
                    + const.NONCE_SIZE
                    + const.KEY_ID_BYTE_LEN
                try:
                    self.ppid_check=prop.ppid_check
                except ValueError:
                    self.ppid_check=prop.pcid_check
                if self.ppid_check:
                    siglen+=const.SHA1_DIGEST_SIZE
                f = open(file, 'rb')
                f.seek(const.ARCH_HEADER_BYTE_LEN)
                content = f.read(file_size-siglen).decode('latin-1')
                f.close()
                if content:
                    str=''
                    if asn1_spec=='PLAT_CFG':
                        str='PlatformConfig'
                    if asn1_spec=='AUDIO_CFG':
                        str='AudioParamFile'
                    if str:
                        if str in content:
                            dispCb('Found it is a wrapped XML file:')
                            dispCb(u'{0}'.format(content))

                if bootmap:
                    bt2_footer, bootmap = ReadBt2ExtendedTrailer(file, self.chip)
                    if bt2_footer:
                        if self.chip == '8060':
                            dispCb('\nBT2 boot map:')
                            dispCb('  - IMEM start addr: 0x%x' % bootmap[0])
                            dispCb('  - DMEM load addr: 0x%x' % bootmap[1])
                            dispCb('  - IMEM size: 0x%x' % bootmap[2])
                        dispCb('\nBT2 extended trailer:')
                        dispCb('%s\n' % bt2_footer)
                    else:
                        dispCb('\nNo extended trailer found')

        except Exception:
            PrintException()

        finally:
            dispCb('\n##########')

    def getArchiveInfo(self, args):
        info = args[0]
        infoIsDir = args[1]
        infoDispCb = args[2]

        if infoIsDir == True:
            self.GetDirInfo(info, infoDispCb)
        else:
            self.GetFileInfo(info, infoDispCb)

    # START_FACTORY_BOARD_REPAIR
    def _formatFlash(self, comPort):
        rsp = self.launchAtCommand(comPort, "AT%IFORMAT?")
        if rsp == None or AT_RSP_ERROR in rsp:
            # Cmd not supported...
            cmd = None
        else:
            print "Formatting flash..."
            self.launchAtCommand(comPort, "AT%IFORMAT=icera2010")

    def _isPlatformConfigFile(self, file):
        fd = open(file, 'r')

        lines = fd.readlines()
        if 'PlatformConfig' in lines[0]:
            return True

        fd.close()
        return False

    def _checkFactBoardRepairPackage(self, package_path, files_list):
        ans = 1
        xml_list = []
        wrapped_list = []
        bin_list = []

        releaseFiles = {"device_config":"","product_config":"","loader":"","secondary_boot": "","modem":"","pkgv":""}
        repairFiles = {"secondary_boot":"","loader":""}
        configFiles = {"platform_config":"","calibration":""}

        try:
            # Look for all .wrapped files
            os.path.walk(package_path, SearchAndGetFiles, ['.wrapped', wrapped_list]) # Arguments = extension, list
            # Look for all .xml files
            os.path.walk(package_path, SearchAndGetFiles, ['.xml', xml_list]) # Arguments = extension, list
            # Look for all .bin files
            os.path.walk(package_path, SearchAndGetFiles, ['.bin', bin_list]) # Arguments = extension, list

            # Look for .wrapped files used by repair agent: a BT2 and a LDR in "boot_applis" folder
            for file in wrapped_list:
                arch_id, chip, prod  = ReadArchiveIdAndChip(file, self.chip)
                if arch_id == 1:
                    repairFiles['secondary_boot'] = file

                if arch_id == 3:
                    repairFiles['loader'] = file


            # Look for .wrapped files to be used during release programming
            for file in wrapped_list:
                if 'boot_applis' not in file:
                    arch_id, chip, prod = ReadArchiveIdAndChip(file, self.chip)
                    if arch_id == 0 and files_list["MDM"] == True: releaseFiles['modem'] = file
                    if arch_id == 1: releaseFiles['secondary_boot'] = file # BT2 is always mandatory here
                    if arch_id == 3: releaseFiles['loader'] = file # LDR is always mandatory here

            # Look for .xml custcfg file
            for file in xml_list:
                if self._isDeviceConfigFile(file):
                    releaseFiles['device_config'] = file
                if self._isProductConfigFile(file):
                    releaseFiles['product_config'] = file
                if self._isPlatformConfigFile(file):
                    configFiles['platform_config'] = file

            # Look for .bin calibration file
            for file in bin_list:
                if 'calibration' in file: # poor criteria
                    # TODO: external tool to check calibration file ????
                    configFiles['calibration'] = file

            # Check all required files
            # Files for repair agent:
            if repairFiles['secondary_boot'] == '':
                print 'ERROR. Incomplete repair agent, BT2 is missing.'
                ans = 0
            if repairFiles['loader'] == '':
                print 'ERROR. Incomplete repair agent, LDR is missing.'
                ans = 0
            # Files to program:
            if releaseFiles['secondary_boot'] == '':
                print 'ERROR: BT2 not found in %s' % package_path
                ans = 0
            if releaseFiles['loader'] == '':
                print 'ERROR: LDR not found in %s' % package_path
                ans = 0
            if files_list["DEVICECFG"] and releaseFiles['device_config'] == '':
                print 'ERROR: DEVICECFG not found in %s' % package_path
                ans = 0
            if files_list["PRODUCTCFG"] and releaseFiles['product_config'] == '':
                print 'ERROR: PRODUCTCFG not found in %s' % package_path
                ans = 0
            if files_list["AUDIOCFG"] and releaseFiles['audio_config'] == '':
                print 'ERROR: AUDIOCFG not found in %s' % package_path
                ans = 0
            if configFiles['platform_config'] == '':
                print 'ERROR: PLATCFG not found in %s' % package_path
                ans = 0
            if files_list["MDM"] and releaseFiles['modem'] == '':
                print 'ERROR: MDM not found in %s' % package_path
                ans = 0
            if files_list["CALIB"] and configFiles['calibration'] == '':
                print 'ERROR: Calibration file not found in %s' % package_path

        except Exception:
            PrintException(verb=self.verboseLevel)
            ans = 0

        finally:
            return ans, repairFiles, releaseFiles, configFiles

    def startFactoryBoardRepair(self, args):
        gauge_value = 0
        factoryPackagePath = args[0]
        factoryReleaseFiles = args[1]
        uartComPort = args[2]
        gauge = args[3]
        fullFlashFormat = args[4]

        usbComPort = None

        gauge.SetValue(gauge_value)
        self.FactoryBoardRepairStarted = True

        # 1st check the whole package: 10% of the process time
        (ok, repairFiles, releaseFiles, configFiles)  = self._checkFactBoardRepairPackage(factoryPackagePath, factoryReleaseFiles)
        if ok:
            gauge_value += 10
            gauge.SetValue(gauge_value)

        # Clear modem port list
        self.hif.mdmPortList = None

        # 2nd start board repair server: 40% of the process time
        if ok and self.FactoryBoardRepairStarted:
            if self.startUartServer(args=['BOARD_REPAIR', repairFiles['secondary_boot'],repairFiles['loader'],uartComPort]) != 0:
                print 'ERROR. Factory board repair: boot applis failure.'
                ok = 0
            else:
                gauge_value += 40
                gauge.SetValue(gauge_value)

        # Wait for USB re-enumeration: not part of process percentage...
        if ok and self.FactoryBoardRepairStarted:
            print 'Waiting for USB port...'
            start =  time.time()
            FindUsbPort = False
            while time.time() - start < 30.0:
                if self.FactoryBoardRepairStarted:
                    if self.hif.mdmPortList:
                        FindUsbPort = True
                        usbComPort = self.hif.mdmPortList[0]
                        break
                    time.sleep(1)
                else:
                    break
            if FindUsbPort == False and self.FactoryBoardRepairStarted:
                gauge.SetValue(0)
                print 'ERROR. Factory board repair: timeout waiting for USB enumeration.'
                ok = 0

        # Check if flash must be formatted:
        if fullFlashFormat:
            self._formatFlash(usbComPort)

        # Program 1st the platform config file: 1% of the process time
        if ok and self.FactoryBoardRepairStarted:
            if self.programXmlCfg(usbComPort, ['PLATCFG', configFiles['platform_config']]) != 0:
                gauge.SetValue(0)
                print 'ERROR. Factory board repair: platcfg update failure.'
                ok = 0
            else:
                gauge_value += 1
                gauge.SetValue(gauge_value)

        # Program found configuration files: devicfg, productcfg & customcfg, 3% of the process time...
        if ok and self.FactoryBoardRepairStarted and releaseFiles['device_config']:
            if self.programXmlCfg(usbComPort, ['DEVICECFG', releaseFiles['device_config']]) != 0:
                gauge.SetValue(0)
                print 'ERROR. Factory board repair: devicecfg update failure.'
                ok = 0
            else:
                gauge_value += 1
                gauge.SetValue(gauge_value)
                releaseFiles['device_config'] = ""
        if ok and self.FactoryBoardRepairStarted and releaseFiles['product_config']:
            if self.programXmlCfg(usbComPort, ['PRODUCTCFG', releaseFiles['product_config']]) != 0:
                gauge.SetValue(0)
                print 'ERROR. Factory board repair: productcfg update failure.'
                ok = 0
            else:
                gauge_value += 1
                gauge.SetValue(gauge_value)
                releaseFiles['product_config'] = ""

        # Then perform a release update: 47% of the process time
        if ok and self.FactoryBoardRepairStarted:
            if self.releaseUpdate(usbComPort, [factoryPackagePath, factoryReleaseFiles], check=False, releaseFiles=releaseFiles) != 0:
                gauge.SetValue(0)
                print 'ERROR. Factory board repair: release update failure.'
                ok = 0
            else:
                gauge_value += 47
                gauge.SetValue(gauge_value)

        # Finally program calibration if required
        if ok and self.FactoryBoardRepairStarted:
            if factoryReleaseFiles['CALIB']:
                if self.programCalibrationFiles(usbComPort, configFiles['calibration']) != 0:
                    gauge.SetValue(0)
                    print 'ERROR. Factory board repair: calibration file update failure.'
                    ok = 0

        self.FactoryBoardRepairStarted = False
        if ok:
            gauge.SetValue(100)
            print 'Factory board repair successful.'
        else:
            gauge.SetValue(0)

    # STOP_FACTORY_BOARD_REPAIR
    def stopFactoryBoardRepair(self, args):
        uartComPort = args[0]
        self.stopUartServer(['BOARD_REPAIR', uartComPort])
        self.FactoryBoardRepairStarted = False

    # ADB
    def _adbReboot(self, device):
        '''
        Reboot platform
        '''
        err=0
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Rebooting platform'
            (err, stdout, stderr) = self.conn.adb.Cmd("reboot", device=device)
            if err:
                print 'ERROR: Rebooting platform.\n{0}'.format(stderr)
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbSetProp(self, device, args):
        '''
        Set system property to a given value...
        '''
        err=0
        prop=args[1]
        value=args[2]
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Set prop {0} to {1}'.format(prop, value)
            self.conn.adb.SetProp(prop, value, device)
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbGetProp(self, device, args):
        '''
        Get system property value
        '''
        err=0
        prop=args[1]
        value='Unknown'
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Get {0} prop:'.format(prop)
            value = self.conn.adb.GetProp(prop, device)
            if value:
                print '{0}: {1}'.format(prop, value)
        except Exception:
            PrintException()
            value='Unknown'
            err=1
        finally:
            return value,err

    def _adbForward(self, device, args):
        '''
        Forward a given port to a given socket...
        '''
        err=0
        port=args[1]
        socket=args[2]
        try:
            self.conn.adb.Root(self,device)
            self.conn.adb.WaitForDevice(device)
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Forwarding {0} on {1}'.format(port, socket)
            self.conn.adb.Root( device)
            self.conn.adb.WaitForDevice(device)
            (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="ls -l {0}".format(port), device=device)
            if err or "no such file or directory" in stdout.lower():
                err=1
                return err            
            (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="icera_log_serial_arm -d {0} -o".format(port),device=device)
            if err:
                print 'ERROR: Fail to configure ADB {0}\n{1}'.format(device, stderr)
                return err
            (err, stdout, stderr) = self.conn.adb.Forward(socket, port, device=device)
            if err:
                print 'ERROR: Port forward failure.\n{0}'.format(stderr)
        except Exception:
            PrintException()
            err=1
        finally:
            if not err:
                self.conn.forwarded = True
            return err

    def _adbRil(self, device, action):
        '''
        Handle actions on RIL daemon...
        '''
        err=0
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Performing a {0}'.format(action)
            if action=='STOP_RIL' or action=='RESTART_RIL':
                (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="stop ril-daemon", device=device)
                if err:
                    print 'ERROR: Stopping RIL.\n{0}'.format(stderr)
                    err=1
            if not err:
                if action=='START_RIL' or action=='RESTART_RIL':
                    (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="start ril-daemon", device=device)
                    if err:
                        print 'ERROR: Starting RIL.\n{0}'.format(stderr)
                        err=1
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbFil(self, device, action):
        '''
        Handle actions on FIL daemon...
        '''
        err=0
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Performing a {0}'.format(action)
            if action=='STOP_FIL' or action=='RESTART_FIL':
                (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="stop fil-daemon", device=device)
                if err:
                    print 'ERROR: Stopping FIL.\n{0}'.format(stderr)
                    err=1
            if not err:
                if action=='START_FIL' or action=='RESTART_FIL':
                    (err, stdout, stderr) = self.conn.adb.Cmd("shell", shellArgs="start fil-daemon", device=device)
                    if err:
                        print 'ERROR: Starting RIL.\n{0}'.format(stderr)
                        err=1
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbRemountFs(self, device):
        '''
        Remount file system including modem partition
        '''
        err=0
        try:
            if self.conn.IsSingleFlash():
                if self.verboseLevel>=IceraToolbox.VERB_NONE:
                    print 'Remounting file system'
                sf=IceraSingleFlashAndroid(self.conn.adb.path, device, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
                err=sf.RemountFileSystem()
            else:
                print 'ERROR: remount FS not supported yet...'
                err = 1
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbExtractFiles(self, device, folder):
        '''
        Extract all known platform files in a given folder.
        '''
        err=0
        try:
            if self.conn.IsSingleFlash():
                sf=IceraSingleFlashAndroid(self.conn.adb.path, device, verbosity=self.verboseLevel, check_adb=False, chip=self.chip, prod_keys=self.prod_keys)
            else:
                sf=IceraDualFlashAndroid(self.conn.adb.path, device, verbosity=self.verboseLevel, check_adb=False)
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Extracting device {0} files in {1}'.format(device, folder)
            err,unused=sf.GetPlatformFiles(dst_folder=folder, all=True)
            if not err:
                print 'All files successfully extracted in {0}'.format(folder)

        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def _adbSetRoot(self, device):
        '''
        Set adb root
        '''
        err=0
        try:
            if self.verboseLevel>=IceraToolbox.VERB_NONE:
                print 'Set platform for root user'
            (err, stdout, stderr) = self.conn.adb.Root(device=device)
            self.adb.WaitForDevice(device=device)
            if err:
                print 'ERROR: Setting platform for root user.\n{0}'.format(stderr)
        except Exception:
            PrintException()
            err=1
        finally:
            return err

    def adbAction(self, comport, args):
        err=0
        rsp=[]
        action = args[0]

        if action == 'REBOOT':         err=self._adbReboot(comport)
        if action == 'SETPROP':        err=self._adbSetProp(comport, args)
        if action == 'GETPROP':        rsp,err=self._adbGetProp(comport,args)
        if action == 'FORWARD':        err=self._adbForward(comport,args)
        if action == 'STOP_RIL':       err=self._adbRil(comport, action)
        if action == 'START_RIL':      err=self._adbRil(comport, action)
        if action == 'RESTART_RIL':    err=self._adbRil(comport, action)
        if action == 'STOP_FIL':       err=self._adbFil(comport, action)
        if action == 'START_FIL':      err=self._adbFil(comport, action)
        if action == 'RESTART_FIL':    err=self._adbFil(comport, action)
        if action == 'REMOUNT_FS':     err=self._adbRemountFs(comport)
        if action == 'EXTRACT_FILES':  err=self._adbExtractFiles(comport, args[1])
        if action == 'SET_ROOT':       err=self._adbSetRoot(comport)

        return rsp,err
