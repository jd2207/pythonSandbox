import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected
from operations.operationResult import opResultSuccess


class checkModemFwVer(operations.sendATCommand.sendATCommand):
  '''Check Modem Firmware Version'''
  
  def __init__(self,factoryStation, options):
    self.name = 'checkModemFirmwareVer'
    self.description = checkModemFwVer.__doc__
    self.ATcmd = 'AT+GMR'
    super(checkModemFwVer,self).__init__(factoryStation, options)
    self.version = options [ 'fwVersion' ]
     
  def processResult(self, errorCode, text):
    if isinstance(super(checkModemFwVer,self).processResult(errorCode,text), opResultSuccess):
      if text.find(self.version) >= 0:
        self.printToLog ('Modem firmware version matches expected value', 5)
        return opResultSuccess()
      else:
        self.printToLog ('FAIL: Modem firmware version does not match %s' % self.version, 0)
        return opResultUnexpected()
    else:
      self.printToLog ('FAIL: Unable to get modem firmware version', 0 )
      return opResultUnexpected()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  fs = factoryStation.factoryStation(None , testMode)       # default factoryStation object

  options = {'ATtool' : 'atcmd-itf', 'fwVersion' : 'e1729-nala.4.05_0.6.4'}
  fo = checkModemFwVer( fs, options )
  fo.postResult( fo.do() )
