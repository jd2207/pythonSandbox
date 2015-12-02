import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected, opResultSuccess


class readPCID(operations.sendATCommand.sendATCommand):
  '''Read PCID'''
  
  def __init__(self, factoryStation, options):
    self.ATcmd = 'AT%IPCID'
    self.name = 'readPCID'
    self.description = readPCID.__doc__
    super(readPCID,self).__init__(factoryStation, options)
    
  def processResult(self, errorCode, text):
    if super(readPCID,self).processResult(errorCode,text):
      str_pcid = text.strip().split('\n')
      if len(str_pcid) < 2:
        self.printToLog ( 'FAIL: Unable to get modem PCID', 0 )
        return opResultUnexpected()
      else:
        pcid = str_pcid[2].strip()
        pcid_len = len(pcid)
        mdm_pcid = pcid[8:pcid_len]
        self.printToLog ('Modem PCID: %s' % (mdm_pcid), 1 )
        return opResultSuccess()
    else:
      self.printToLog ( 'FAIL: Unable to get modem PCID', 0 )
      return opResultUnexpected()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)              # default factoryStation object
  options = {'ATtool' : 'atcmd-itf'}
  fo = readPCID( fs, options )
  fo.postResult( fo.do() )
