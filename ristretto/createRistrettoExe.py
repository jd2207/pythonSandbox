#!/usr/bin/env python
#################################################################################################
#  Icera Inc
#  Copyright (c) 2008
#  All rights reserved
#################################################################################################
#
#
#
#
#################################################################################################
'''
createArchive.py: To generate folder used to generate final ristretto.exe.

Create a GUI folder containing:
 - py2exe ristretto_core.exe
 - ICE_ICE/ICE_OEM/OEM-FACT/ICE_DBG dev keys
 - ICE_DBG prod key if it exists for this customer
 - UpdaterLib.dll
'''
import os,sys,re,shutil,traceback,subprocess, platform

# Fixed Paths
ICE_ICE_90xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '9xxx', '9040', 'key0')
ICE_ICE_91xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '9xxx', '9140', 'key0')
ICE_OEM_KEY_FOLDER      = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_OEM', 'key0')
OEM_FACT_KEY_FOLDER     = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-OEM_FACT', 'key0')
OEM_FIELD_KEY_FOLDER    = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-OEM_FIELD', 'key0')
ICE_ICE_PROD_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', 'key1')
ICE_ICE_PROD_90xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', '9xxx', '9040', 'key1')
ICE_ICE_PROD_91xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', '9xxx', '9140', 'key1')
ICE_DBG_KEY_FOLDER      = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_DBG', 'key0')
UPDATER_FOLDER          = os.path.join('downloader','updaterlib','bin','bin.wx32')
UPDATER_FOLDER_LINUX    = os.path.join('downloader', 'updaterlib', 'bin', 'bin.lx{0}'.format(platform.architecture()[0][:2]))
DRIVERS_PUBLIC_FOLDER   = os.path.join('downloader', 'updaterlib', 'public')
RISTRETTO_FOLDER        = os.path.join('ristretto')
CRASH_CHECK_FOLDER      = os.path.join('icera-log-utils','bin.wx32')
USER_GUIDE_FOLDER       = os.path.join(RISTRETTO_FOLDER, 'user_guide')
MSVCR90_STORAGE_FOLDER  = os.path.join(RISTRETTO_FOLDER, 'Microsoft.VC90.CRT')
TOOLS_FOLDER            = os.path.join('modem-utils')
ANDROIDDEVTOOLS_FOLDER  = os.path.join('androidDevTools','x86')

# Sources
ICERA_SW_ROOT           = os.path.join(os.path.dirname(__file__),'..')
P4_SOFTWARE_DEPOT       = '//software/main.br'
ICE_ICE_PROD_90xx_KEY_SOURCE = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_ICE_PROD_90xx_KEY_FOLDER)))
ICE_ICE_PROD_91xx_KEY_SOURCE = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_ICE_PROD_91xx_KEY_FOLDER)))
ICE_ICE_90xx_KEY_SOURCE = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_ICE_90xx_KEY_FOLDER)))
ICE_ICE_91xx_KEY_SOURCE = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_ICE_91xx_KEY_FOLDER)))
ICE_OEM_KEY_SOURCE      = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_OEM_KEY_FOLDER)))
OEM_FACT_KEY_SOURCE     = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',OEM_FACT_KEY_FOLDER)))
OEM_FIELD_KEY_SOURCE    = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',OEM_FIELD_KEY_FOLDER)))
ICE_DBG_KEY_SOURCE      = '/'.join((P4_SOFTWARE_DEPOT, re.sub(r'\\','/',ICE_DBG_KEY_FOLDER)))
UPDATER_SOURCE          = os.path.join(ICERA_SW_ROOT, UPDATER_FOLDER, 'updaterlib.dll')
UPDATER_SOURCE_LINUX    = os.path.join(ICERA_SW_ROOT, UPDATER_FOLDER_LINUX, 'updater.so')
ICERA_ICON              = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'icera.ico')
ICERA_LOGO              = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'logo_Icera.gif')
RISTRETTO               = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'ristretto_core.exe')
CRASH_CHECK             = os.path.join(ICERA_SW_ROOT, CRASH_CHECK_FOLDER, 'crash-check.exe')
CRASH_CHECK_LINUX       = os.path.join(ICERA_SW_ROOT, CRASH_CHECK_FOLDER,  'crash-check')
MSVCP120                = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER, 'msvcp120.dll')
MSVCR120                = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER, 'msvcr120.dll')
REGISTER_DEVICE_INFO    = os.path.join(ICERA_SW_ROOT, ANDROIDDEVTOOLS_FOLDER, 'Register_device_info.bat')
GET_PCID_SH             = os.path.join(ICERA_SW_ROOT, ANDROIDDEVTOOLS_FOLDER, 'get_pcid.sh')

ARCH_TYPE_SOURCE        = os.path.join(ICERA_SW_ROOT, DRIVERS_PUBLIC_FOLDER, 'drv_arch_type.h')
USER_GUIDE_RESOURCES    = os.path.join(ICERA_SW_ROOT, USER_GUIDE_FOLDER)
TOOLS_RESOURCES         = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER)

# Filename where to find PID/VID indications for auto-detect
HWPLAT_FILE = 'hwplatform.h'

class Archive:
    def __init__(self, gui_folder, targetSystem="Windows"):
        self.targetSystem = targetSystem
        self.tool_config_file = os.path.join(ICERA_SW_ROOT, 'ristretto', 'README.txt')
        self.config_file = os.path.join(ICERA_SW_ROOT, 'ristretto', 'config.txt')
        self.cleanup = os.path.join(ICERA_SW_ROOT, 'ristretto', 'cleanup.bat')
        self.gui_folder = gui_folder
        self.gen_paths()

    def gen_paths (self):
        self.appli_folder               = os.path.join(self.gui_folder, RISTRETTO_FOLDER)
        self.appli_ice_ice_90xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_90xx_KEY_FOLDER)
        self.appli_ice_ice_91xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_91xx_KEY_FOLDER)
        self.appli_ice_oem_key_folder   = os.path.join(self.gui_folder, ICE_OEM_KEY_FOLDER)
        self.appli_oem_fact_key_folder  = os.path.join(self.gui_folder, OEM_FACT_KEY_FOLDER)
        self.appli_oem_field_key_folder = os.path.join(self.gui_folder, OEM_FIELD_KEY_FOLDER)
        self.appli_ice_ice_prod_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_KEY_FOLDER)
        self.appli_ice_ice_prod_90xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_90xx_KEY_FOLDER)
        self.appli_ice_ice_prod_91xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_91xx_KEY_FOLDER)
        self.appli_ice_dbg_key_folder   = os.path.join(self.gui_folder, ICE_DBG_KEY_FOLDER)
        self.user_guide_folder          = os.path.join(self.gui_folder, USER_GUIDE_FOLDER)
        if self.targetSystem == "Windows":
            self.appli_updater_folder       = os.path.join(self.gui_folder, UPDATER_FOLDER)
        elif self.targetSystem == "Linux":
            self.appli_updater_folder       = os.path.join(self.gui_folder, UPDATER_FOLDER_LINUX)
        self.appli_usb_profile_folder   = os.path.join(self.gui_folder, DRIVERS_PUBLIC_FOLDER)
        if self.targetSystem == "Windows":
            self.appli_msvcr90_folder       = os.path.join(self.gui_folder, MSVCR90_STORAGE_FOLDER)
        self.appli_crash_check_folder   = os.path.join(self.gui_folder, CRASH_CHECK_FOLDER)
        self.appli_androiddevtools_folder = os.path.join(self.gui_folder, ANDROIDDEVTOOLS_FOLDER)

    # Search all files with a given extension, in a path and copy them in dest:
    def search_and_copy_files(self, args, path, files):
        extension, dest = args
        for file in files:
            if file.endswith(extension):
                shutil.copy(os.path.join(path, file), os.path.join(dest, file))

    # Copy a key set folder in appli
    def copyKeys(self, appli_key_folder, key_source, prod=False):
        os.makedirs(appli_key_folder)
        '/'.join((key_source, 'key.exponent.h'))
        print "p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.exponent.h')),
        '/'.join((key_source, 'key.exponent.h')))
        subprocess.Popen("p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.exponent.h')),
        '/'.join((key_source, 'key.exponent.h'))), shell=True)
        print "p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.modulus.h')),
        '/'.join((key_source, 'key.modulus.h')))
        subprocess.Popen("p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.modulus.h')),
        '/'.join((key_source, 'key.modulus.h'))), shell=True)
        if not prod:
            print "p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'secret.key.hex')),
            '/'.join((key_source, 'secret.key.hex')))
            subprocess.Popen("p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'secret.key.hex')),
            '/'.join((key_source, 'secret.key.hex'))), shell=True)

    def create (self):
        # Copy generated py2exe and icon/logo
        if os.path.isdir(self.gui_folder):
            shutil.rmtree(self.gui_folder);
        os.makedirs(self.appli_folder)
        if self.targetSystem == "Windows":
            shutil.copy(RISTRETTO, self.appli_folder)
            shutil.copy(MSVCP120, self.appli_folder)
            shutil.copy(MSVCR120, self.appli_folder)
        shutil.copy(ICERA_ICON, self.appli_folder)
        shutil.copy(ICERA_LOGO, self.appli_folder)
        if os.path.isfile(self.tool_config_file) == True:
            shutil.copy(self.tool_config_file, self.appli_folder)
        if os.path.isfile(self.config_file) == True:
            shutil.copy(self.config_file, self.appli_folder)
        if os.path.isfile(self.cleanup) == True:
            shutil.copy(self.cleanup, self.appli_folder)

        # Copy dev ICE_ICE keys
        KeyFound=False
        for path,key in  [(self.appli_ice_ice_90xx_key_folder,ICE_ICE_90xx_KEY_SOURCE), \
        (self.appli_ice_ice_91xx_key_folder,ICE_ICE_91xx_KEY_SOURCE)]:
            self.copyKeys(path, key)

        # Copy dev ICE_OEM keys
        self.copyKeys(self.appli_ice_oem_key_folder, ICE_OEM_KEY_SOURCE)

        # Copy dev OEM_FACT keys
        self.copyKeys(self.appli_oem_fact_key_folder, OEM_FACT_KEY_SOURCE)

        # Copy dev OEM_FIELD keys
        self.copyKeys(self.appli_oem_field_key_folder, OEM_FIELD_KEY_SOURCE)

        # Copy prod ICE_ICE keys

        for path,key in  [(self.appli_ice_ice_prod_90xx_key_folder,ICE_ICE_PROD_90xx_KEY_SOURCE),\
        (self.appli_ice_ice_prod_91xx_key_folder,ICE_ICE_PROD_91xx_KEY_SOURCE)]:
            self.copyKeys(path, key,  prod=True)

        # Copy dev ICE_DBG keys
        self.copyKeys(self.appli_ice_dbg_key_folder, ICE_DBG_KEY_SOURCE)

        # Copy UpdaterLib.dll
        os.makedirs(self.appli_updater_folder)
        if self.targetSystem == "Windows":
            shutil.copy(UPDATER_SOURCE, self.appli_updater_folder)
        elif self.targetSystem == "Linux":
            shutil.copy(UPDATER_SOURCE_LINUX, self.appli_updater_folder)
            
        #Copy crash_check
        os.makedirs(self.appli_crash_check_folder)
        if self.targetSystem == "Windows":
            shutil.copy(CRASH_CHECK, self.appli_crash_check_folder)
        elif self.targetSystem == "Linux":
            shutil.copy(CRASH_CHECK_LINUX, self.appli_crash_check_folder)
            
        #Copy unlock certificate request tools
        os.makedirs(self.appli_androiddevtools_folder)
        shutil.copy(REGISTER_DEVICE_INFO, self.appli_androiddevtools_folder)
        shutil.copy(GET_PCID_SH, self.appli_androiddevtools_folder)

        # Copy drv_arch_type.h
        os.makedirs(self.appli_usb_profile_folder)
        shutil.copy(ARCH_TYPE_SOURCE, self.appli_usb_profile_folder)

       # Copy user guide resources
        os.makedirs(self.user_guide_folder)
        os.path.walk(USER_GUIDE_RESOURCES, self.search_and_copy_files, ['.html', self.user_guide_folder]) # Arguments = extension, destination
        os.path.walk(USER_GUIDE_RESOURCES, self.search_and_copy_files, ['.JPG',  self.user_guide_folder]) # Arguments = extension, destination

    #Copy some required MS .dll in RISTRETTO_FOLDER
        if self.targetSystem == "Windows":
            if os.path.isdir(os.path.join(TOOLS_RESOURCES, 'Microsoft.VC90.CRT')):
                shutil.copytree(os.path.join(TOOLS_RESOURCES, 'Microsoft.VC90.CRT'), self.appli_msvcr90_folder)
            elif os.path.isfile(os.path.join(TOOLS_RESOURCES, 'msvcr90.dll')) and os.path.isfile(os.path.join(TOOLS_RESOURCES, 'Microsoft.VC90.CRT.manifest')):
                os.makedirs(self.appli_msvcr90_folder)
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'msvcr90.dll'), self.appli_msvcr90_folder)
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'msvcm90.dll'), self.appli_msvcr90_folder)
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'msvcp90.dll'), self.appli_msvcr90_folder)
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'Microsoft.VC90.CRT.manifest'), self.appli_msvcr90_folder)

            # Copy some tools dependencies
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-b64.exe')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-b64.exe'), self.appli_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-aes.exe')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-aes.exe'), self.appli_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'cygwin1.dll')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'cygwin1.dll'), self.gui_folder)
                
        elif self.targetSystem == "Linux":
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-b64')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-b64'), self.appli_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-aes')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-aes'), self.appli_folder)

if __name__ == '__main__':
    gui_folder = sys.argv[1]
    if 'ForLinux' in sys.argv:
        archive = Archive( gui_folder, targetSystem="Linux")
    else:
        archive = Archive( gui_folder)
    try:
        archive.create()
    except Exception:
        type, value, history = sys.exc_info()
        traceback.print_exception(type, value, history, 10)
        print '\n*** ERROR *** ERROR generating Ristretto archive'
        sys.exit(1)
    exit(0)
