import factoryStation, factoryConfig
import utilities
from operations.blockingPrompt import blockingPrompt
from operations.readModemFwVer import readModemFwVer
from operations.readSerialNum import readSerialNum
from operations.iCal import iCal
from operations.resice import resice
import sys
import pwOnOff_visa
import argparse


class rfcv(factoryStation.factoryStation):
  '''RF and Calibration Validation operations'''
  
  def __init__(self, logger=None, testMode=None):
    self.name = 'RFCV'
    self.desc = rfcv.__doc__
    super(rfcv,self).__init__(logger, testMode)

  def toolPathCheck(self):
    self.setPSU()
    
    if not self.setRadioTester(): return False
    return True

  def setPSU(self):
    self.psu = None
    if not self.testMode:
      try:
        if type(self) is rfcv:
          self.psu = pwOnOff_visa.FactoryPower()
      except:
        self.printToLog('FATAL: PSU cannot be initialized', 0)
        sys.exit()
    else:
        self.printToLog('<TEST MODE> PSU set to %s' % self.psu, 5)
        
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
 
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='rfcv')
  utilities.cmdLineArgs(parser)                  # general args 
  args = parser.parse_args()    

# Debug logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)
    
# Create RFCV station object and attributes
  fs = rfcv( debugLog, args.test)       
  fs.setProduct('i500_1720_att')

# Add the operations sequence
  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Please insert board. Press Enter when done.' }))
  fs.operations.append ( readSerialNum( fs, {'ATtool' : 'atcmd-itf'} ) )
  fs.operations.append ( readModemFwVer( fs, {'ATtool' : 'atcmd-itf'} ) )
  
  iCalOptions = factoryConfig.operationsParser().itemsFromXML( 'example/ical.xml', 'operation' )['ical']['subItem']
  fs.operations.append ( iCal( fs, iCalOptions ) )

  resiceOptions = factoryConfig.operationsParser().itemsFromXML( 'example/resice.xml', 'operation' )['resice']['subItem']
  fs.operations.append ( resice( fs, resiceOptions ) )
  
  fs.deviceLoop()               # loop for multiple devices
