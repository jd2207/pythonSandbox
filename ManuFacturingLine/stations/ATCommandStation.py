import factoryStation
import argparse, utilities

from operations.blockingPrompt import blockingPrompt
from operations.sendEchoOn import sendEchoOn
from operations.readModemFwVer import readModemFwVer
from operations.checkModemFwVer import checkModemFwVer
from operations.readModemFwId import readModemFwId
from operations.readPCID import readPCID
from operations.readPFID import readPFID
from operations.readSerialNum import readSerialNum
from operations.writeSerialNum import writeSerialNum
from operations.unlockEngMode import unlockEngMode
from operations.forceFactoryMode import forceFactoryMode
from operations.modemFusing import modemFusing
from operations.backupFilesys import backupFilesys


class ATCommandStation(factoryStation.factoryStation):
  '''For testing AT command operations'''
  
  def __init__(self, logger=None, testMode=None):
    self.name = 'ATCommandStation'
    self.desc = ATCommandStation.__doc__
    super(ATCommandStation,self).__init__(logger, testMode)
        
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='AT Command test Station')
  utilities.cmdLineArgs(parser)                  # general args 
  args = parser.parse_args()    

# Debug logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)

  fs = ATCommandStation( None, args.test)       
  
  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Please insert board. Press Enter when done.' }))
  fs.operations.append ( sendEchoOn( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( readModemFwVer( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( checkModemFwVer( fs, {'ATtool' : 'atcmd-itf', 'fwVersion' : 'e1729-nala.4.05_0.6.4'} ) )
  fs.operations.append ( readModemFwId( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( readPCID( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( readPFID( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( readSerialNum( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( writeSerialNum( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( unlockEngMode( fs, {'ATtool' : 'atcmd-itf'} ) )   
  fs.operations.append ( forceFactoryMode( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( modemFusing ( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( backupFilesys ( fs, {'ATtool' : 'atcmd-itf'} ) )
  
  fs.deviceLoop()               # loop for multiple devices
  
  
