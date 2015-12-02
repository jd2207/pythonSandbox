import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected
from operations.operationResult import opResultSuccess


class readModemFwId(operations.sendATCommand.sendATCommand):
  '''Read Modem Firmware ID'''
  
  def __init__(self,factoryStation, options):
    self.name = 'readModemFirmwareID'
    self.description = readModemFwId.__doc__
    self.ATcmd = 'AT%IGETFWID'
    super(readModemFwId,self).__init__(factoryStation, options)

  def processResult(self, errorCode, text):
    if isinstance(super(readModemFwId,self).processResult(errorCode,text), opResultSuccess):
      str_fwid = text.split('\n')
      if len(str_fwid) < 2:
        self.printToLog ( 'FAIL: Unable to get modem firmware id', 0 )
        return opResultUnexpected()
      else:
          mdm_fwid = str_fwid[1]
          fwid_len = len(mdm_fwid)
          mdm_fwid = mdm_fwid[11:fwid_len]
          self.printToLog ('Modem firmware ID: %s' % (mdm_fwid), 1 )
          return opResultSuccess()
    else:
      self.printToLog ( 'FAIL: Unable to get modem firmware id', 0 )
      return opResultUnexpected()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True
  fs = factoryStation.factoryStation(None, testMode)                          # default factoryStation object
  options = {'ATtool' : 'atcmd-itf' }
  fo = readModemFwId( fs, options )
  fo.do()
  fo.postResult(fo.do ())
