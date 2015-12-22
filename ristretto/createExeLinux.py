'''

createExeLinux.py: To freeze and build python code: 



Freezing is based on cx_Freeze that you can download here:

http://cx-freeze.sourceforge.net/



BETA VERSION



Create a GUI folder containing:

 - ristretto freezing code

 - icera asn1 tool

 - ICE_ICE/ICE_OEM/OEM-FACT/ICE_DBG dev keys

 - ICE_DBG

 - UpdaterLib.dll

 - supported hwplatform.h

Outputs: build/RISTRETTO_GUI

'''

#################################################################################################

# Imports

#################################################################################################



import sha, dbhash, anydbm, shelve, encodings
import glob
import shutil
import os,platform, sys

from cx_Freeze import setup, Executable

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
if os.path.join(base_path, 'modem-utils') not in sys.path:
    sys.path.append(os.path.join(base_path, 'modem-utils'))
os.environ['ICERA_SW_PATH'] = base_path

import IceraToolbox
import RistrettoCommon

tool_version = RistrettoCommon.GetToolConfig()["version"]

setup(
    name = 'ristretto_core',
    executables = [Executable('ristretto.py',
            targetName="ristretto_core",
            path = base_path,
            compress = True,
            copyDependentFiles = True,
            appendScriptToExe = True,
            appendScriptToLibrary = True,
            )],
    version=tool_version,
    author='Hugo DUPRAS',
    options = {"build_exe": {
            "build_exe":'build/RISTRETTO_GUI/ristretto',
            "bin_includes":['libxml2.so.2','libwx_gtk2u_adv-2.8.so.0',
             'libwx_gtk2u_core-2.8.so.0', 'libwx_baseu_net-2.8.so.0',
             'libwx_baseu-2.8.so.0', 'libtiff.so.5','libjbig.so.0',
             'libwx_gtk2u_html-2.8.so.0'],
            "includes" : ["lxml", "lxml._elementpath", 'libxml2'],
            "packages" : ['sha','dbhash', 'anydbm','shelve', 'encodings'],
            "copy_dependent_files" : 'True'
          }}
    )

