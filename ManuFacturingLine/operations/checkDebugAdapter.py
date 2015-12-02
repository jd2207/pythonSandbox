import factoryOperation, factoryStation
import utilities
import time, os, sys

from operations.operationResult import opResultSuccess, opResultDebugAdapterNoPing, opResultDebugAdapterNoDXPrun        


class checkDebugAdapter(factoryOperation.factoryOperation):
  '''Check connection to debug adapter'''
  
  def __init__(self, factoryStation, options):
    self.name = 'checkDebugAdapter'
    self.description = checkDebugAdapter.__doc__
    self.successKeyword = 'Reply from'
    super(checkDebugAdapter,self).__init__(factoryStation)

  def initialize(self):
    self.dhcpStop = "icera-dhcp-stop.bat" if sys.platform == "win32" else "icera-dhcpd-stop"
    self.dhcpStart = "icera-dhcp-start.bat" if sys.platform == "win32" else "icera-dhcpd-start"

    for f in (self.dhcpStart, self.dhcpStop, 'dxp-run'):
      if not self.factoryStation.fileOnPath(f):
        self.printToLog('FATAL: Command %s not found on path' % f, 0)
        if not self.factoryStation.testMode: return False
    
    return True

  def do(self):
    countArg = '-c' if not sys.platform == "win32" else '-n'
    self.args = ['ping', countArg, '3', self.factoryStation.adapter.name]
    
    if not isinstance(super(checkDebugAdapter,self).do(), opResultSuccess):
      self.printToLog('WARNING: Cannot communicate with the debug Adapter - bouncing DHCP', 1)
      os.system(self.dhcpStop); time.sleep(1); os.system(self.dhcpStart)

      if not isinstance(super(checkDebugAdapter,self).do(), opResultSuccess):
        self.printToLog('ERROR: Cannot communicate with the debug Adapter', 0)
        return opResultDebugAdapterNoPing()

    self.successKeyword = 'sent and received [1024] ECHO messages Ok'
    self.args = ['dxp-run','-ada', self.factoryStation.adapter.name, '-acmd', 'aux -echoseqtest 1024', '-int']
    if not isinstance(super(checkDebugAdapter,self).do(), opResultSuccess):
      return opResultDebugAdapterNoDXPrun()        
     
    return opResultSuccess()
  
      
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True

# Create a dummy factory station 
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  fs.adapter = utilities.debugAdapter()
  
  fo = checkDebugAdapter( fs, None)
  fo.postResult( fo.do ())
  
  
  
  
  