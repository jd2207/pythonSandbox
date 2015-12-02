import factoryOperation, factoryStation
import os.path
from operations.operationResult import opResultDownloadFileNotFound
import operations.sendATCommand 


class downloadFile(factoryOperation.factoryOperation):
  '''download files'''
  
  def __init__(self, factoryStation, options):
    if type(self) is downloadFile:                   # do not overwrite subclasses
      self.name = 'download'
      self.description = downloadFile.__doc__
    self.arch = 'win32'
    super(downloadFile,self).__init__(factoryStation, options)
  
  def initialize(self):
    currFolderPath = os.path.abspath(os.curdir)
    self.tool = os.path.join(currFolderPath, 'downloader.exe')
    self.factoryStation.fileExists(self.tool,'Downloader tool')

  def do(self, fileName):
    self.modemPort = self.factoryStation.modemPort
    
    if not os.path.exists(fileName):
      self.printToLog('WARNING: Cannot find file "%s"' % fileName, 0)
      return opResultDownloadFileNotFound()
    else:      
      self.args = [ self.tool, 
                  '-d' + self.modemPort,
                  '-f' + fileName
                  ]
      return super(downloadFile, self).do()

      
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True

# Create a dummy factory station 
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  fo = downloadFile(  fs, None )
  
# Create operation instance (also need an sendATCommand to retrieve COM port info)
  fo1 = operations.sendATCommand.sendATCommand( fs, {'ATtool' : 'atcmd-itf' } )
  fo2 = downloadFile( fs, None )

# Perform the operation once
  fo1.do()
  fo2.postResult( fo.do('imeiFile') )
