import os, sys, re, traceback, subprocess

import IceraToolbox
from serialization import Serialization

if IceraToolbox.IsWindows():
    import win32api, win32process

################################
#                              #
#  Constants                   #
#                              #
################################

RISTRETTO_VERSION="15.07"
CHANGELIST='870312'

#Tool mode
RISTRETTO_MODE_BASIC=1
RISTRETTO_MODE_ADVANCED=2
RISTRETTO_MODE_ADVANCED_SWITCH=3

#Interface Modes:
RISTRETTO_HIF=1
RISTRETTO_ADB=2

# Threads actions:
DISPLAY_CRASHINFO   = 1
BUILD_COREDUMP      = 2
CLEAR_CRASHINFO     = 3
UPDATE_RELEASE      = 4
DISPLAY_PLATINFO    = 5
LIST_FILESYSTEM     = 6
SCAN_TARGET         = 7
FILE_UPDATE         = 8
START_UART_SERVER   = 9
STOP_UART_SERVER    = 10
SET_HIF_TYPE        = 11
LAUNCH_AT_CMD       = 12
GET_MEMORY_DUMP     = 13
STOP_WAIT_PNPEVENT  = 14
PROGRAM_XML         = 15
PROGRAM_IMEI        = 16
PROGRAM_CALIB       = 17
GET_ARCH_INFO       = 18
START_FACTORY_BOARD_REPAIR = 19
STOP_FACTORY_BOARD_REPAIR  = 20
DECODE_COREDUMP     = 21
DETECT_CHIP_TYPE    = 22
EXTRACT_ARCHIVE     = 23
ADB                 = 24
DECODE_MEMORY_DUMP  = 25
CHECK_LOCK_TYPE     = 26
CHECK_PCID          = 27

# HIF type
HIF_TYPE = [ "Unknown", "USB", "UART"]
HIF_USB  = 1
HIF_UART = 2
SUPPORTED_UART_BAUDRATES = ['115200', '230400', '460800', '921600']
SUPPORTED_UART_BLOCKSIZE = ['1024', '2048', '4096', '8192', '16384']

# Some AT command strings
AT_CR        = '\r\n'
AT_RSP_OK    = AT_CR + 'OK' + AT_CR
AT_RSP_ERROR = AT_CR + 'ERROR' + AT_CR

# Page Number in main GUI
UPDATE_PAGE_NUMBER       = 0
DEBUG_PAGE_NUMBER        = 1
SETTINGS_PAGE_NUMBER     = 2
BOARD_REPAIR_PAGE_NUMBER = 3
ADB_AP_IF_PAGE_NUMBER    = 4

# Paths and file names
TMP_EXTRACT_FOLDER = os.path.realpath(os.path.join(IceraToolbox.BASE_PATH, 'ristretto','TmpReleasePackage'))
MDM_FILENAME = 'modem.wrapped'
LDR_FILENAME = 'loader.wrapped'
BT2_FILENAME = 'secondary_boot.wrapped'
DEVICECFG_FILENAME = 'deviceConfig.xml'
PRODUCTCFG_FILENAME = 'productConfig.xml'
PKGV_FILENAME = 'package_version.pkgv'

# Icera archive:
# Extended trailer
DMEM_ADDR_MASK = '0x3FFFFFFFL'

valid_basename = IceraToolbox.BASE_PATH
if IceraToolbox.IsWindows():
    valid_basename = win32api.GetLongPathName(IceraToolbox.BASE_PATH)
# Ristretto path
RISTRETTO_PATH = os.path.realpath(os.path.join(valid_basename,'ristretto'))

# Tool Customized Config file
RISTRETTO_CUSTOMIZED_CONFIG_FILE = os.path.realpath(os.path.join(RISTRETTO_PATH, 'config.txt'))

# Tool serialized settings file
RISTRETTO_SETTINGS_FILE = os.path.realpath(os.path.join(RISTRETTO_PATH, '.ristretto'))

# Tool default log file
RISTRETTO_LOG_FILE = os.path.realpath(os.path.join(RISTRETTO_PATH,'.ristretto.log'))

# Default block size for f/w update
DEFAULT_BLOCK_SIZE = 16384

# Default block size for boot from UART acquisition.
DEFAULT_BOOT_UART_BLOCK_SIZE = 8192

def NullFunc(*args): pass

def ParseAndDispMsg(msg, new_msg):
    '''
    Parses content of a message.

    DISPLAYS only part the message contained BEFORE a given separator: \r or \n
    RETURNS part of the message contained AFTER a given separator: \r or \n
    '''
    sep = None
    msg+=new_msg
    if msg.rfind('\r')!=-1:
        sep = '\r'
    if msg.rfind('\n')!=-1:
        sep = '\n'
    if sep:
        print msg[:msg.rfind(sep)]
        msg = msg[msg.rfind(sep)+1:]

    return msg

def GetToolConfig():
    tool_config = {}

    try:
        tool_config["version"] = RISTRETTO_VERSION#eval(RISTRETTO_VERSION)

    except Exception:
        PrintException()

    return tool_config

def FileExist(path, filename):
    '''
    Check file existence
    '''

    ans = 1
    tmp = os.path.join(path, filename)
    if os.path.isfile(tmp) == False:
        print 'File %s not found' % tmp
        ans = 0
    return ans

def SearchAndGetFiles(args, path, files):
    '''
    Search for a given type of file (based on extension)
    in a files list and update list with files found.
    '''
    extension, list = args
    for file in files:
        if file.endswith(extension) or extension == '*':
            list.append(os.path.join(path, file))

def PrintException(verb=IceraToolbox.VERB_INFO, msg=None):
    if verb >= IceraToolbox.VERB_INFO:
        if msg:
            print msg
        type, value, history = sys.exc_info()
        traceback.print_exception(type, value, history, 10)

# Saved settings file
serialization=None
def GetSettings():
    global serialization
    serialization = Serialization(RISTRETTO_SETTINGS_FILE)

    if serialization:
        settings = serialization.GetData()
        if settings: return settings
    return {}

def StoreSettings(settings):
    global serialization
    if serialization:
        serialization.StoreData(settings)

# RESTART
def Restart():
    if IceraToolbox.IsWindows():
        # Will modify base path in IceraToolbox.
        if hasattr(sys, 'frozen'):
            subprocess.Popen('ristretto_core.exe', creationflags=win32process.CREATE_NO_WINDOW)
        else:
            subprocess.Popen('python ristretto.py', creationflags=win32process.CREATE_NO_WINDOW)
    else:
        subprocess.Popen(['python',os.path.join(RISTRETTO_PATH,'ristretto.py')])
    sys.exit()
