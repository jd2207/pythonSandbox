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
createArchive.py: To generate folder used to update ristretto.exe for cust use.

Create a GUI folder containing:
 - ICE_DBG prod key if it exists for this customer
 - Cust config file
'''
import os,sys,re,shutil,traceback, subprocess,stat

# Fixed Paths
PROD_KEY_FOLDER = '/'.join(('drivers', 'private', 'arch', 'keys'))
RISTRETTO_FOLDER        = os.path.join('ristretto')

# Sources

P4_SOFTWARE_DEPOT       = '//software/main.br'
os.environ["P4PORT"]    = 'p4proxy-ukdc:2025'


######################################
REFERENCE_PLATFORM_LIST=['pc300', 'e300sd', 'e302', 'e400', 'e410', 'e450', 'p1001', 'p1002', 'i500-121']

# Fixed Paths
ASN1_FOLDER             = os.path.join('asn1', 'tools', 'bin', 'icera') # asn1_tool is always copied in icera folder inside ristretto.exe
ICE_ICE_KEY_FOLDER      = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', 'key0')
ICE_ICE_8xxx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '8xxx', 'key0')
ICE_ICE_9xxx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '9xxx', 'key0')
ICE_ICE_90xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '9xxx', '9040', 'key0')
ICE_ICE_91xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_ICE', '9xxx', '9140', 'key0')
ICE_OEM_KEY_FOLDER      = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_OEM', 'key0')
OEM_FACT_KEY_FOLDER     = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-OEM_FACT', 'key0')
OEM_FIELD_KEY_FOLDER    = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-OEM_FIELD', 'key0')
ICE_DBG_PROD_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_DBG', 'key1')
ICE_ICE_PROD_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', 'key1')
ICE_ICE_PROD_90xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', '9xxx', '9040', 'key1')
ICE_ICE_PROD_91xx_KEY_FOLDER = os.path.join('drivers', 'private', 'arch', 'keys', 'prod-ICE_ICE', '9xxx', '9140', 'key1')
ICE_DBG_KEY_FOLDER      = os.path.join('drivers', 'private', 'arch', 'keys', 'dev-ICE_DBG', 'key0')
UPDATER_FOLDER          = os.path.join('integration_tools', 'updaterlib', 'bin', 'win32')
UPDATER_FOLDER_LINUX    = os.path.join('integration_tools', 'updaterlib', 'bin', 'linux')
HWPLATFORM_FOLDER       = os.path.join('drivers', 'private', 'hwplatform')
DRIVERS_PUBLIC_FOLDER   = os.path.join('drivers', 'public')
TOOLS_FOLDER            = os.path.join('tools')

# Sources
ICERA_SW_ROOT           = os.path.join(os.path.dirname(__file__),'..', '..')
ICE_ICE_PROD_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_PROD_KEY_FOLDER)
ICE_ICE_PROD_90xx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_PROD_90xx_KEY_FOLDER)
ICE_ICE_PROD_91xx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_PROD_91xx_KEY_FOLDER)
ICE_ICE_KEY_SOURCE      = os.path.join(ICERA_SW_ROOT, ICE_ICE_KEY_FOLDER)
ICE_ICE_8xxx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_8xxx_KEY_FOLDER)
ICE_ICE_9xxx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_9xxx_KEY_FOLDER)
ICE_ICE_90xx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_90xx_KEY_FOLDER)
ICE_ICE_91xx_KEY_SOURCE = os.path.join(ICERA_SW_ROOT, ICE_ICE_91xx_KEY_FOLDER)
ICE_OEM_KEY_SOURCE      = os.path.join(ICERA_SW_ROOT, ICE_OEM_KEY_FOLDER)
OEM_FACT_KEY_SOURCE     = os.path.join(ICERA_SW_ROOT, OEM_FACT_KEY_FOLDER)
OEM_FIELD_KEY_SOURCE    = os.path.join(ICERA_SW_ROOT, OEM_FIELD_KEY_FOLDER)
ICE_DBG_KEY_SOURCE      = os.path.join(ICERA_SW_ROOT, ICE_DBG_KEY_FOLDER)
UPDATER_SOURCE          = os.path.join(ICERA_SW_ROOT, UPDATER_FOLDER, 'Updater.dll')
UPDATER_SOURCE_LINUX    = os.path.join(ICERA_SW_ROOT, UPDATER_FOLDER_LINUX, 'Updater.so')
MSVCP100                = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER, 'msvcp100.dll')
MSVCR100                = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER, 'msvcr100.dll')
HWPLATFORM_SOURCE       = os.path.join(ICERA_SW_ROOT, HWPLATFORM_FOLDER)
USB_PROFILE_SOURCE      = os.path.join(ICERA_SW_ROOT, DRIVERS_PUBLIC_FOLDER, 'drv_usb_profile_ids_table.h')
USB_PROFILE_ALT_SOURCE  = os.path.join(ICERA_SW_ROOT, DRIVERS_PUBLIC_FOLDER, 'drv_usb_profile_ids.h')
ARCH_TYPE_SOURCE        = os.path.join(ICERA_SW_ROOT, DRIVERS_PUBLIC_FOLDER, 'drv_arch_type.h')
FS_CFG_SOURCE           = os.path.join(ICERA_SW_ROOT, DRIVERS_PUBLIC_FOLDER, 'drv_fs_cfg.h')
TOOLS_RESOURCES         = os.path.join(ICERA_SW_ROOT, TOOLS_FOLDER)

# Filename where to find PID/VID indications for auto-detect
HWPLAT_FILE = 'hwplatform.h'
######################################


class Archive:
    RISTRETTO_FOLDER        = os.path.join('tools', 'ristretto')
    USER_GUIDE_FOLDER       = os.path.join(RISTRETTO_FOLDER, 'user_guide')
    USER_GUIDE_RESOURCES    = os.path.join(ICERA_SW_ROOT, USER_GUIDE_FOLDER)
    MSVCR90_STORAGE_FOLDER  = os.path.join(RISTRETTO_FOLDER, 'Microsoft.VC90.CRT')
    ICERA_ICON              = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'icera.ico')
    ICERA_LOGO              = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'logo_Icera.gif')
    RISTRETTO               = os.path.join(ICERA_SW_ROOT, RISTRETTO_FOLDER, 'ristretto_core.exe')
    
    def __init__(self, cust, gui_folder, custasn1="icera", targetSystem="Windows"):
        self.cust = cust
        self.targetSystem = targetSystem
        if targetSystem == "Windows":
            self.asn1_source = os.path.join(ICERA_SW_ROOT, 'asn1', 'tools', 'bin', custasn1, 'asn1_tool.exe')
        elif targetSystem == "Linux":
            self.asn1_source = os.path.join(ICERA_SW_ROOT, 'asn1', 'tools', 'bin', custasn1, 'asn1')
        self.tool_config_file = os.path.join(ICERA_SW_ROOT, 'tools', 'ristretto', 'README.txt')
        self.config_file = os.path.join(ICERA_SW_ROOT, 'tools', 'ristretto', 'release', self.cust, 'config.txt')
        self.gui_folder = gui_folder
        self.gen_paths()

    def gen_paths (self):
        self.appli_folder               = os.path.join(self.gui_folder, self.RISTRETTO_FOLDER)
        self.appli_asn1_folder          = os.path.join(self.gui_folder, ASN1_FOLDER)
        self.appli_ice_ice_key_folder   = os.path.join(self.gui_folder, ICE_ICE_KEY_FOLDER)
        self.appli_ice_ice_8xxx_key_folder = os.path.join(self.gui_folder, ICE_ICE_8xxx_KEY_FOLDER)
        self.appli_ice_ice_9xxx_key_folder = os.path.join(self.gui_folder, ICE_ICE_9xxx_KEY_FOLDER)
        self.appli_ice_ice_90xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_90xx_KEY_FOLDER)
        self.appli_ice_ice_91xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_91xx_KEY_FOLDER)
        self.appli_ice_oem_key_folder   = os.path.join(self.gui_folder, ICE_OEM_KEY_FOLDER)
        self.appli_oem_fact_key_folder  = os.path.join(self.gui_folder, OEM_FACT_KEY_FOLDER)
        self.appli_oem_field_key_folder = os.path.join(self.gui_folder, OEM_FIELD_KEY_FOLDER)
        self.appli_ice_dbg_prod_key_folder = os.path.join(self.gui_folder, ICE_DBG_PROD_KEY_FOLDER)
        self.appli_ice_ice_prod_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_KEY_FOLDER)
        self.appli_ice_ice_prod_90xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_90xx_KEY_FOLDER)
        self.appli_ice_ice_prod_91xx_key_folder = os.path.join(self.gui_folder, ICE_ICE_PROD_91xx_KEY_FOLDER)
        self.appli_ice_dbg_key_folder   = os.path.join(self.gui_folder, ICE_DBG_KEY_FOLDER)
        self.user_guide_folder          = os.path.join(self.gui_folder, self.USER_GUIDE_FOLDER)
        if self.targetSystem == "Windows":
            self.appli_updater_folder       = os.path.join(self.gui_folder, UPDATER_FOLDER)
        elif self.targetSystem == "Linux":
            self.appli_updater_folder       = os.path.join(self.gui_folder, UPDATER_FOLDER_LINUX)
        self.appli_hwplatform_folder    = os.path.join(self.gui_folder, HWPLATFORM_FOLDER)
        self.appli_usb_profile_folder   = os.path.join(self.gui_folder, DRIVERS_PUBLIC_FOLDER)
        if self.targetSystem == "Windows":
            self.appli_msvcr90_folder       = os.path.join(self.gui_folder, self.MSVCR90_STORAGE_FOLDER)
        self.appli_tools_folder         = os.path.join(self.gui_folder, TOOLS_FOLDER)

    # Search all files with a given extension, in a path and copy them in dest:
    def search_and_copy_files(self, args, path, files):
        extension, dest = args
        for file in files:
            if file.endswith(extension):
                shutil.copy(os.path.join(path, file), os.path.join(dest, file))

    # Search all files named 'hwplatform.h' and dedicated to cust:
    def search_hwplat (self, args, path, files):
        filename, folder = args
        pattern = re.compile(self.cust)
        for file in files:
            if file == filename:
                basename = os.path.basename(path)
                if (pattern.search(basename)) or (self.cust == 'icera_internal') or (basename in REFERENCE_PLATFORM_LIST):
                    header  = os.path.join(path, file)
                    dirname = os.path.join(folder, basename)
                    os.makedirs(dirname)
                    shutil.copy(header, dirname)

    # Search production ICE_DBG dedicated to cust:
    def search_ICEDBG (self, args, path, files):
        pattern = re.compile('production.*ice.*dbg.*'+self.cust.lower()+'.*')
        # copy first prod key that matches this customer
        if pattern.search(path.lower()) and self.appli_ice_dbg_prod_key_folder:
            self.copyKeys(self.appli_ice_dbg_prod_key_folder, os.path.join(path,os.listdir(path)[0]), prod=True)
            self.appli_ice_dbg_prod_key_folder = None

    # Copy a key set folder in appli
    def copyKeys(self, appli_key_folder, key_source, prod=False):
        os.makedirs(appli_key_folder)
        shutil.copy(os.path.join(key_source, 'key.exponent.h'), appli_key_folder)
        shutil.copy(os.path.join(key_source, 'key.modulus.h'), appli_key_folder)
        if not prod: shutil.copy(os.path.join(key_source, 'secret.key.hex'), appli_key_folder)

    def create (self):
        # Copy generated py2exe and icon/logo
        if os.path.isdir(self.gui_folder):
            shutil.rmtree(self.gui_folder);
        os.makedirs(self.appli_folder)
        if self.targetSystem == "Windows":
            shutil.copy(self.RISTRETTO, self.appli_folder)
            shutil.copy(MSVCP100, self.appli_folder)
            shutil.copy(MSVCR100, self.appli_folder)
        shutil.copy(self.ICERA_ICON, self.appli_folder)
        shutil.copy(self.ICERA_LOGO, self.appli_folder)
        if os.path.isfile(self.tool_config_file) == True:
            shutil.copy(self.tool_config_file, self.appli_folder)
        if os.path.isfile(self.config_file) == True:
            shutil.copy(self.config_file, self.appli_folder)

        # Copy icera asn1 tool
        os.makedirs(self.appli_asn1_folder)
        shutil.copy(self.asn1_source, self.appli_asn1_folder)

        # Copy dev ICE_ICE keys
        KeyFound=False
        for path,key in  [(self.appli_ice_ice_key_folder,ICE_ICE_KEY_SOURCE), (self.appli_ice_ice_8xxx_key_folder,ICE_ICE_8xxx_KEY_SOURCE),\
        (self.appli_ice_ice_90xx_key_folder,ICE_ICE_90xx_KEY_SOURCE), (self.appli_ice_ice_91xx_key_folder,ICE_ICE_91xx_KEY_SOURCE),\
        (self.appli_ice_ice_9xxx_key_folder,ICE_ICE_9xxx_KEY_SOURCE)]:
            if os.path.exists(os.path.join(key, 'key.exponent.h')) and os.path.exists(os.path.join(key, 'key.modulus.h')):
                self.copyKeys(path, key)
                KeyFound=True

        if not KeyFound:
            print '\n*** WARNING *** NO ICE_ICE Key found'

        # Copy dev ICE_OEM keys
        self.copyKeys(self.appli_ice_oem_key_folder, ICE_OEM_KEY_SOURCE)

        # Copy dev OEM_FACT keys
        self.copyKeys(self.appli_oem_fact_key_folder, OEM_FACT_KEY_SOURCE)

        # Copy dev OEM_FIELD keys
        if os.path.isdir(OEM_FIELD_KEY_SOURCE):
            self.copyKeys(self.appli_oem_field_key_folder, OEM_FIELD_KEY_SOURCE)

        # Copy prod ICE_DBG keys
        os.path.walk(os.path.join(ICE_DBG_KEY_SOURCE,'..','..'), self.search_ICEDBG, [])

        # Copy prod ICE_ICE keys
        KeyFound=False
        for path,key in  [(self.appli_ice_ice_prod_key_folder,ICE_ICE_PROD_KEY_SOURCE), (self.appli_ice_ice_prod_90xx_key_folder,ICE_ICE_PROD_90xx_KEY_SOURCE),\
        (self.appli_ice_ice_prod_91xx_key_folder,ICE_ICE_PROD_91xx_KEY_SOURCE)]:
            if os.path.exists(os.path.join(key, 'key.exponent.h')) and os.path.exists(os.path.join(key, 'key.modulus.h')):
                self.copyKeys(path, key,  prod=True)
                KeyFound=True

        if not KeyFound:
            print '\n*** WARNING *** NO ICE_ICE PROD Key found'

        # Copy dev ICE_DBG keys
        if os.path.isdir(ICE_DBG_KEY_SOURCE):
            self.copyKeys(self.appli_ice_dbg_key_folder, ICE_DBG_KEY_SOURCE)

        # Copy UpdaterLib.dll
        os.makedirs(self.appli_updater_folder)
        if self.targetSystem == "Windows":
            shutil.copy(UPDATER_SOURCE, self.appli_updater_folder)
        elif self.targetSystem == "Linux":
            shutil.copy(UPDATER_SOURCE_LINUX, self.appli_updater_folder)

        # Copy required hwplatform.h files
        os.path.walk(HWPLATFORM_SOURCE, self.search_hwplat, [HWPLAT_FILE, self.appli_hwplatform_folder]) # Arguments = Filename + Folder

        # Copy drv_usb_profile_ids.h and drv_arch_type.h, drv_fs_config.h
        os.makedirs(self.appli_usb_profile_folder)
        if os.path.isfile(USB_PROFILE_SOURCE):
            shutil.copy(USB_PROFILE_SOURCE, self.appli_usb_profile_folder)
        shutil.copy(USB_PROFILE_ALT_SOURCE, self.appli_usb_profile_folder)
        shutil.copy(ARCH_TYPE_SOURCE, self.appli_usb_profile_folder)
        shutil.copy(FS_CFG_SOURCE, self.appli_usb_profile_folder)

        # Copy user guide resources
        os.makedirs(self.user_guide_folder)
        os.path.walk(self.USER_GUIDE_RESOURCES, self.search_and_copy_files, ['.html', self.user_guide_folder]) # Arguments = extension, destination
        os.path.walk(self.USER_GUIDE_RESOURCES, self.search_and_copy_files, ['.JPG',  self.user_guide_folder]) # Arguments = extension, destination

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
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'mkisofs.exe')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'mkisofs.exe'), self.appli_tools_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'cygwin1.dll')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'cygwin1.dll'), self.appli_tools_folder)
                
        elif self.targetSystem == "Linux":
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-b64')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-b64'), self.appli_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'icera-aes')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'icera-aes'), self.appli_folder)
            if os.path.isfile(os.path.join(TOOLS_RESOURCES, 'mkisofs')):
                shutil.copy(os.path.join(TOOLS_RESOURCES, 'mkisofs'), self.appli_tools_folder)




class custRelease:
    ICERA_SW_ROOT           = os.path.join(os.path.dirname(__file__),'..')
    RISTRETTO_FOLDER        = os.path.join('ristretto')
    def __init__(self, cust, gui_folder, targetSystem="Windows"):
        self.cust = cust
        self.targetSystem = targetSystem
        self.config_file = os.path.join(self.ICERA_SW_ROOT, 'ristretto', 'release', self.cust, 'config.txt')
        self.gui_folder = gui_folder
        self.gen_paths()

    def gen_paths (self):
        self.appli_folder = os.path.join(self.gui_folder, RISTRETTO_FOLDER)
        self.appli_prod_key_folder  = os.path.join(self.gui_folder, PROD_KEY_FOLDER)
        
        # Search production ICE_DBG dedicated to cust:
    def search_PRODKEY (self, Type):
        P4_path=''
        P4_paths=[]
        match = re.match(r'([A-Z]{3,5})_([A-Z]{3,5})',Type)
        typeA=match.group(1)
        typeB=match.group(2)
        dirFound=False
        print "p4 dirs //software/main.br/drivers/private/arch/keys/prod*{0}*{1}*".format(typeA, typeB)
        p=subprocess.Popen("p4 dirs //software/main.br/drivers/private/arch/keys/prod*{0}*{1}*".format(typeA, typeB), stdout=subprocess.PIPE, shell=True)
        pattern = re.compile('prod.*'+typeA.lower()+'.*'+typeB.lower()+'.*'+self.cust.lower()+'.*')
        for line in p.stdout:
            if pattern.search(line.lower()):
                P4_paths.append(line.strip())
                dirFound=True
        if not dirFound:
            print "No {0}_{1} key found for {2}".format(typeA, typeB, self.cust)
            return
        
        for P4_path in P4_paths:
            print "p4 files {0}/... ".format(P4_path)
            p=subprocess.Popen("p4 files {0}/... ".format(P4_path), stdout=subprocess.PIPE, shell=True)
            output = p.stdout.read()
            
            pattern = re.compile('key.modulus.h')
            pattern2 = re.compile('key.exponent.h')
            if (pattern.search(output) and pattern2.search(output)):
                folder_name=os.path.basename(P4_path)
                appli_prod_key_folder_cust=os.path.join(self.appli_prod_key_folder,folder_name,'key')
                self.copyKeys(appli_prod_key_folder_cust, "{0}/...".format(P4_path))           


    # Copy a key set folder in appli
    def copyKeys(self, appli_key_folder, key_source):
        if not os.path.exists(appli_key_folder):
            os.makedirs(appli_key_folder)
        print "p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.exponent.h')),
        '/'.join((key_source, 'key.exponent.h')))
        subprocess.Popen("p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.exponent.h')),
        '/'.join((key_source, 'key.exponent.h'))), shell=True).wait()
        print "p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.modulus.h')),
        '/'.join((key_source, 'key.modulus.h')))
        subprocess.Popen("p4 print -m1 -o {0} {1}".format('/'.join((appli_key_folder, 'key.modulus.h')),
        '/'.join((key_source, 'key.modulus.h'))), shell=True).wait()


    def create (self):
        # Copy generated py2exe and icon/logo
        # Do not clean gui_folder when build is done for Linux
        if os.path.isdir(self.gui_folder) and self.targetSystem == "Windows":
            for (dirpath, dirnames, filenames) in os.walk(self.gui_folder):
                for dirname in dirnames:
                    os.chmod(os.path.join(dirpath,dirname), stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
                for filename in filenames:
                    os.chmod(os.path.join(dirpath,filename),stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
            shutil.rmtree(self.gui_folder);
        try:
            os.makedirs(self.appli_folder)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(self.appli_folder):
                pass
            else: raise
        if os.path.isfile(self.config_file) == True:
            shutil.copy(self.config_file, self.appli_folder)
        
        for type in ['ICE_DBG','ICE_OEM','OEM_FACT','OEM_FIELD']:
            self.search_PRODKEY(type)

if __name__ == '__main__':
    cust = sys.argv[1]
    gui_folder = sys.argv[2]
    custasn1="icera"
    
    if 'ForLinux' in sys.argv:
        if len(sys.argv)!=4:
            custasn1 = sys.argv[3]

        asn1_source = os.path.join(ICERA_SW_ROOT, 'asn1', 'tools', 'bin', custasn1, 'asn1_tool.exe')
        if os.path.exists(asn1_source):
            archive = Archive(cust, gui_folder, custasn1, targetSystem="Linux")
        else:           
            archive = custRelease(cust, gui_folder, targetSystem="Linux")
    else:
        if len(sys.argv)!=3:
            custasn1 = sys.argv[3]

        asn1_source = os.path.join(ICERA_SW_ROOT, 'asn1', 'tools', 'bin', custasn1, 'asn1_tool.exe')
        if os.path.exists(asn1_source):
            archive = Archive(cust,gui_folder,custasn1)
        else:
            archive = custRelease(cust, gui_folder)
    try:
        archive.create()
        if os.path.isdir(gui_folder):
            for (dirpath, dirnames, filenames) in os.walk(gui_folder):
                for dirname in dirnames:
                    os.chmod(os.path.join(dirpath,dirname), 0755)
                for filename in filenames:
                    os.chmod(os.path.join(dirpath,filename),0755)
    except Exception:
        type, value, history = sys.exc_info()
        traceback.print_exception(type, value, history, 10)
        print '\n*** ERROR *** ERROR generating Ristretto archive'
        sys.exit(1)
    exit(0)
