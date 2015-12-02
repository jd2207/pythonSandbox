import factoryStation
import operations.sendATCommand
import operations.operationResult
import utilities

from operations.operationResult import opResultSuccess

class opUnableReadMdmSn(operations.operationResult.operationResult):
  def __init__(self):
    self.code = 11
    self.desc = 'Unable to get modem SN'

class opModemSnEmpty(operations.operationResult.operationResult):
  def __init__(self):
    self.code = 12
    self.desc = 'Modem serial number is empty'


    
class readSerialNum(operations.sendATCommand.sendATCommand):
  '''Read Serial Number'''
  
  def __init__(self,factoryStation, options):
    self.name = 'readSerialNum'
    self.description = readSerialNum.__doc__
    super(readSerialNum,self).__init__(factoryStation, options)

  def do(self, serNum=None):
    self.ATcmd = 'AT%IPARAM'
    return super(readSerialNum,self).do()

  def processResult(self, errorCode, text):
    if isinstance(super(readSerialNum,self).processResult(errorCode,text), opResultSuccess):
      str_sn = text.strip().split('\n')
      if len(str_sn) < 3:
        return opUnableReadMdmSn()

      str_sn_2 = str_sn[3].strip().split(' ')
      if len(str_sn_2) < 2:
        return opUnableReadMdmSn()

      mdm_sn = str_sn_2[1]
      if mdm_sn.find('<empty>') >= 0:
        return  opModemSnEmpty() 
      
      self.printToLog('Serial number read: %s' % mdm_sn) 
      self.factoryStation.serNum = utilities.serialNumber(mdm_sn)
      return opResultSuccess
    else:
      return opUnableReadMdmSn()


# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  options = {'ATtool' : 'atcmd-itf' }
  fo = readSerialNum( fs, options )
  fo.postResult( fo.do() )
