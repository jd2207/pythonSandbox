# --------------------------------------------------------------------    
#
#  Python module for compact and general classes used by other modules
#
# --------------------------------------------------------------------    

from userInterface import screen
from datetime import datetime
from os.path import join, dirname, basename
import os
import sys
import subprocess
import re

# -------------------------------------------------
#  Functions
# -------------------------------------------------
def subProc(commandLine, debugFlag=False):
  '''Run a commandline as a subprocess'''
  cmdSend = commandLine

  if debugFlag:
    return 0, '<TEST MODE is on> Subprocess command which would be run: %s' % str(cmdSend)
  else: 
    pretext = 'Running subprocess command: %s\n' % str(cmdSend)

    try:
      child = subprocess.Popen(cmdSend, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      errorCode = child.wait()
      cmdLineLog = child.stdout.read() + child.stderr.read()
    except OSError as e:
      errorCode = -1
      cmdLineLog = str(e) 

  return (errorCode, pretext + cmdLineLog) 

def fileOnPath(programName):
  '''Determine if a file is on the system PATH'''
  for path in os.environ["PATH"].split(os.pathsep):
    path = path.strip('"')
    exeFile = os.path.join(path, programName)
    if os.path.isfile(exeFile) and os.access(exeFile, os.X_OK):
      return True
  return False

def cmdLineArgs(parser):
  '''Command line parsing'''          #  Scripts can call this then add their own specific args on top
  parser.add_argument( '--verbosity', type=int, default=5, help='Set the debug level')
  parser.add_argument( '--test', default=False, action='store_true', help='Run in test mode')
  parser.add_argument( '--trace', default='.', help='Debug output logpath')
  parser.add_argument( '-x', '--xml', default=None, help='XML configuration file name')


# -----------------------------------------------------------    
#  Class for Serial Numbers 
# -----------------------------------------------------------    


class serialNumber(object):
  '''For handling serial numbers'''
  
  MDM_SN_REGEX = "[qQ]|[-\w]{10,18}"
  
  def __init__(self,serialStr='NO_SERIAL'):
    self.snString = serialStr
    
  def getSN(self):
    return self.snString 
  
  def getFromUser(self):
    prompt = 'Please scan S/N label (or q to quit)'
    
    while True:
      serial = screen().prompt(prompt)
      if not re.match(serialNumber.MDM_SN_REGEX, serial):
        print 'Invalid entry! Must match this: %s' % serialNumber.MDM_SN_REGEX
      else:
        break
    
    self.snString = serial
    return self

   
# -----------------------------------------------------------    
#  Class for IMEIs
# -----------------------------------------------------------    
class imeiNumber(object):
  
  IMEI_REGEX = "[qQ]|\d{15}"
 
  def getFromUser(self):
    prompt = 'Please scan IMEI (or q to quit)'
    
    while True:
      imeiStr = screen().prompt(prompt)
      if not re.match(imeiNumber.IMEI_REGEX, imeiStr):
        print 'Invalid entry! IMEI must be 15 digits only'
      elif not lunhCheck(imeiStr):
        print 'Invalid entry! IMEI failed lunh check'
      else:
        break
    
    return imeiStr

def lunhCheck(imeiStr): 
  luhnArr = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
  (counter, num, odd) = (0, None, False)
  
  a = list(imeiStr)
  a.reverse()
  for char in a:
    num = int(char)
    counter += num if not odd else luhnArr[num] 
    odd = not odd
  
  return counter % 10 == 0 

  
# -----------------------------------------------------
#  For generating timestamps
# -----------------------------------------------------
class dtStamp :
  def __init__ (self):
    self.dt = datetime.now()
        
  def logfile_tstamp (self):
    return self.dt.strftime('%Y%m%d%H%M%S')
    
  def logentry_tstamp (self):
    return self.dt.strftime('%Y-%m-%d %H:%M:%S')


# -------------------------------------------------------
#  For logging
# -------------------------------------------------------
def logWarning():
  if not screen().promptYN('WARNING: No debug log specified. Continue ?'):
    print 'Quitting...'
    sys.exit()

class logger :            # initialize AND open the log
  
  def __init__ ( self, logpath='.', logname='', verbosity=0):
    self.verbosity = verbosity
    self.logname = join ( logpath, dtStamp().logfile_tstamp() + logname +'.log' )
    try:
      self.LOGFILE = open( self.logname, 'w+')
    except:
      print 'FATAL: Not able to open the log file. Stopping.'
      sys.exit()
    
  def lineOut ( self, text, level=0 ):
    if( level <= self.verbosity ):
      outString = "[ %s ][ %s ] " % (dtStamp().logentry_tstamp(), level ) + text 
      print outString 
      self.LOGFILE.write( outString + '\n')
                
  def flush(self):
    self.LOGFILE.flush()
                
  def dirname(self):
    return dirname (self.logname)

# -----------------------------------------------------------------
#  Log compression classes
# -----------------------------------------------------------------
class logCompressor(object):
  
  def __init__(self, archiveName, flist):
    self.archive = archiveName

    i = 0 
    while ( i < len(flist) ):
      if i == 0:                          # if first time use create
        self.create(flist[0])
      else:                               # otherwise append to the now created archive
        self.append(flist[i])
      i += 1
      
  def create(self, fileToAdd):            # over-ridden by subclasses
    None
    
  def append(self, fileToAdd):            # over-ridden by subclasses
    None


class logCompressorTar(logCompressor):
  
  def __init__(self, archiveName, flist):
    super(logCompressorTar,self).__init__(archiveName, flist)

  def create(self,fName):
    self.tar(fName)              
    
  def append(self,fName):
    self.tar(fName,False)              
  
  def tar(self,fName,create=True):
    opt = 'c' if create else 'r'
    dirN = dirname(fName) 
    if dirN == '': dirN = '.'   
    subprocess.call(['tar', '-'+opt+'f', self.archive+'.tar', '-C', dirN, basename(fName) ])              

    
class logCompressor7z(logCompressor):
  
  def __init__(self, archiveName, flist):
    super(logCompressor7z,self).__init__(archiveName, flist)

  def create(self,fName):
    self.zip7(fName)              
    
  def append(self,fName):
    self.zip7(fName,False)              
  
  def zip7(self,fName,create=True):
    exe = '7z' if not sys.platform == "win32" else '7z.exe'
    subprocess.call( [exe, 'a', self.archive + '.7z', os.path.join('.',fName) ] )     # add '.' to ignore paths of file to be archived              


# -----------------------------------------------------------------
#  Class for radioTester and debugAdapter
# -----------------------------------------------------------------

class debugAdapter(object):
  def __init__(self):

    try:
      icera_license_key = os.environ['ICERA_LICENSE_KEY']
    except KeyError:
      print 'No environment variable "ICERA_LICENSE_KEY"'
    
    self.name = icera_license_key[icera_license_key.find('-net ')+len('-net '):]


class radioTester(object):
  def __init__(self):

    try:
      envVar = os.environ['ICERA_RADIO_TESTER']
      (self.type, self.visaAddress) = envVar.split('-')
    except KeyError:
      print('FATAL: No environment var "ICERA_RADIO_TESTER"')
      (self.type, self.visaAddress) = (None, None)
    
