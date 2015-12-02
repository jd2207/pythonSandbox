import factoryStation, factoryOperation
import utilities

from operations.operationResult import opResultSuccess, opResultAbort     

class scanIMEI(factoryOperation.factoryOperation):
  '''Prompt user to scan or enter the IMEI'''
  
  def __init__(self, factoryStation):
    self.name = 'scanIMEI'
    self.description = scanIMEI.__doc__
    super(scanIMEI, self).__init__(factoryStation)

  def do(self):
    imei = utilities.imeiNumber().getFromUser()
    if not imei.lower() == 'q': 
      self.factoryStation.scannedIMEI = imei
      self.printToLog('New IMEI is %s' %  imei, 5)
      return opResultSuccess()
    else: 
      return opResultAbort()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  fs = factoryStation.factoryStation()                          # default factoryStation object
  fo = scanIMEI(fs)
  fs.operations.append(fo)

  # Perform over and over on different devices
  fs.deviceLoop(False)  # no log collection
  
  