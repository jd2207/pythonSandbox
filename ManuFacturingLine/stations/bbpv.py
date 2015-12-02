import factoryStation, factoryConfig
import utilities
import os, sys
import argparse
import pwOnOff

from operations.blockingPrompt import blockingPrompt
from operations.smokeTest import smokeTest
from operations.bringupTest import bringupTest
from operations.fwProgramming import fwProgramming
from operations.forceFactoryMode import forceFactoryMode
from operations.readModemFwVer import readModemFwVer
from operations.writeSerialNum import writeSerialNum
from operations.interfaceTest import interfaceTest
from operations.modemFusing import modemFusing


class bbpv(factoryStation.factoryStation):
  '''FW first-time programming, Interface test and fusing'''
  
  def __init__(self, logger=None, testMode=False):
    self.name = 'BBPV'
    self.desc = bbpv.__doc__

    super(bbpv,self).__init__(logger, testMode)

  def toolPathCheck(self):

    # Check debug adapter is configured ------------------
    try: 
      adapter = utilities.debugAdapter()
      self.adapter = adapter
    except:
      self.printToLog('FATAL: Cannot verify the debug adapter', 0)
      if not self.testMode:
        sys.exit() 
    
    # Set SDK path --------------------------------------
    sdkPath = ''
    try:
      sdkPath = os.path.join(os.environ['ICERA_ROOT'], 'dxp-bare','examples','bringup_ice9040')
      self.printToLog('SDK installation found at %s' % sdkPath, 5)
    except KeyError:
      self.printToLog('FATAL: SDK not correctly installed - no environment var "ICERA_ROOT"', 0)
      if not self.testMode: sys.exit()
    else: 
      if not os.path.isdir(sdkPath):
        self.printToLog('FATAL: SDK not correctly installed - no directory at ' + sdkPath, 0)
        if not self.testMode: sys.exit()
    
    self.sdkPath = sdkPath
    self.setPSU()
  
    return True

  def setPSU(self):
    self.psu = None
    if not self.testMode:
      try:
        self.psu = pwOnOff.FactoryPower()
      except:
        self.printToLog('FATAL: PSU cannot be initialized', 0)
        sys.exit() if not self.testMode else None
    else:
      self.printToLog('<TEST MODE> PSU set to %s' % self.psu, 5)
      
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='bbpv')
  utilities.cmdLineArgs(parser)                  # general args 
  args = parser.parse_args()    

# Debug logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)
    
# Create BBPV station object and attributes
  fs = bbpv( debugLog, args.test)       
  fs.setProduct('i500_1720_att')
  fs.powerMeterVisaAddress=''  
    
# Add the operations sequence
  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Please insert board. Press Enter when done.' })) 
  fs.operations.append ( smokeTest( fs, None ) )
  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Please CONNECT debug adaptor (green box). Press Enter when done.' })) 
#  fs.operations.append ( controlPSU 
  fs.operations.append ( bringupTest( fs, { 'commandLine' : 'BRINGUP_ICE9040_DDR_TAL.bat -warmboottest' })) 
  fs.operations.append ( fwProgramming ( fs, { 'args' : '-9040 -hwplat p2341',
                                               'sourcePackage' : '',
                                              'gangImage' : 'gang_image'
                                              } )) 
#  fs.operations.append ( controlPSU
  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Please probe and check the supply voltage at C11 on the modem module. Press Enter when done.' })) 
  fs.operations.append ( forceFactoryMode( fs, {'ATtool' : 'atcmd-itf'} ))  
  fs.operations.append ( readModemFwVer( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( writeSerialNum( fs, {'ATtool' : 'atcmd-itf'} ) )  
  
  ifTestOptions = factoryConfig.operationsParser().itemsFromXML( 'example/interfaceTest.xml', 'operation' )['iftest']['subItem']
  fs.operations.append ( interfaceTest( fs, ifTestOptions ) )

  fs.fuseImage = '0x0,0x0,0x0,0x0,0x4,0x0,0x0'
  fs.operations.append ( modemFusing( fs, {'ATtool' : 'atcmd-itf'} ) )  
  
  fs.deviceLoop()               # loop for multiple devices
  
