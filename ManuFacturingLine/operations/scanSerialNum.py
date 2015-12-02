import factoryStation, factoryOperation
import utilities

from operations.operationResult import opResultSuccess, opResultAbort


class scanSerialNum(factoryOperation.factoryOperation):
  '''Prompt user to scan or enter the serial number'''
  
  def __init__(self, factoryStation):
    self.name = 'scanSerialNum'
    self.description = scanSerialNum.__doc__
    super(scanSerialNum, self).__init__(factoryStation )

  def do(self):
    serNum = utilities.serialNumber().getFromUser()
    if not serNum.getSN().lower() == 'q': 
      self.factoryStation.serNum = serNum
      self.printToLog('Scanned serial number is %s' %  serNum.getSN(), 5)
      return opResultSuccess()
    else: 
      return opResultAbort()


# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  fs = factoryStation.factoryStation()                          # default factoryStation object
  fo = scanSerialNum(fs)
  fs.operations.append(fo)
  
  # Perform over and over on different devices
  fs.deviceLoop(False)  # no log collection

  