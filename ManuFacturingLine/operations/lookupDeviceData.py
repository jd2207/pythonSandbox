import factoryOperation, factoryStation
import operations.scanIMEI
import productionDeviceData
import os.path

from operations.operationResult import opResultSuccess, opResultNoIMEIinProdDeviceData        


class lookupDeviceData(factoryOperation.factoryOperation):
  ''' Obtain device specific data '''
  
  def __init__(self,factoryStation, options):
    self.name = 'lookupDeviceData'
    self.description = lookupDeviceData.__doc__
    super(lookupDeviceData,self).__init__(factoryStation, options)

  def initialize(self):
    currFolderPath = os.path.abspath(os.curdir)
    prodDevDataFile = os.path.join(currFolderPath, self.options['prodDevData'])
    if not self.factoryStation.fileExists(prodDevDataFile,'Production device data'):
      return False
    
    self.pdd = productionDeviceData.productionDeviceData(prodDevDataFile)
    return True

  def do(self, serNum=None):

    if not (self.factoryStation.scannedIMEI in self.pdd):
      self.printToLog('WARNING: Scanned IMEI has no entry in the production device data')
      return opResultNoIMEIinProdDeviceData()
    
    imeiRecord = self.pdd[self.factoryStation.scannedIMEI]
    self.factoryStation.imeiFile = imeiRecord['IMEI Filename']
    self.printToLog('IMEI record to be used is %s' % self.factoryStation.imeiFile, 3)
    self.factoryStation.devCfgFile = imeiRecord['DeviceConfig Filename']
    self.printToLog('Device Config file to be used is %s' % self.factoryStation.devCfgFile, 3)
    return opResultSuccess()
  
      
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = False
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  
  fo1 = operations.scanIMEI.scanIMEI( fs )
  fo2 = lookupDeviceData(  fs, { 'prodDevData' : 'production_files.csv' }  )
  
  fo1.do()
  fo2.postResult( fo2.do ())
  
  
  
  