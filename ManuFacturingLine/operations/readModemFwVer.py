import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected
from operations.operationResult import opResultSuccess


class readModemFwVer(operations.sendATCommand.sendATCommand):
  '''Read Modem Firmware Version'''
  
  def __init__(self,factoryStation, options):
    self.name = 'readModemFWVer'
    self.description = readModemFwVer.__doc__
    self.ATcmd = 'AT+GMR'
    super(readModemFwVer,self).__init__(factoryStation, options)
     
  def processResult(self, errorCode, text):
    if isinstance(super(readModemFwVer,self).processResult(errorCode,text), opResultSuccess):
      str_fw = text.split('\n')
      if len(str_fw) < 4:
        self.printToLog ('FAIL: Unable to get modem firmware version', 0 )
        return opResultUnexpected()
      else:
        self.printToLog ('Modem firmware version: %s' % ( str_fw[4] ), 1)
        return opResultSuccess()
    else:
      self.printToLog ('FAIL: Unable to get modem firmware version', 0 )
      return opResultUnexpected()
    
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)        # default factoryStation object
  fo = readModemFwVer( fs, {'ATtool' : 'atcmd-itf' } )
  
  fo.postResult( fo.do() )
  