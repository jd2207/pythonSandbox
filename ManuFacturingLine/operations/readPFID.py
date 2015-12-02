import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected, opResultSuccess

class readPFID(operations.sendATCommand.sendATCommand):
  '''Read PCID'''
  
  def __init__(self, factoryStation, options):
    self.ATcmd = 'AT%IPFID'
    self.name = 'readPFID'
    self.description = readPFID.__doc__
    super(readPFID,self).__init__(factoryStation, options)
    
  def processResult(self, errorCode, text):
    if super(readPFID,self).processResult(errorCode,text):
      str_pfid = text.strip().split('\n')
      if len(str_pfid) < 2:
        self.printToLog ( 'FAIL: Unable to get modem PFID', 0 )
        return opResultUnexpected()
      else:
        pfid = str_pfid[2].strip()
        pfid_len = len(pfid)
        mdm_pfid = pfid[8:pfid_len]
        self.printToLog ('Modem PFID: %s' % (mdm_pfid), 1 )
        return opResultSuccess()
    else:
      self.printToLog ( 'FAIL: Unable to get modem PFID', 0 )
      return opResultUnexpected()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True

  fs = factoryStation.factoryStation(None, testMode)         # default factoryStation object
  options = {'ATtool' : 'atcmd-itf'}
  fo = readPFID( fs, options )
  fo.postResult( fo.do() )
  