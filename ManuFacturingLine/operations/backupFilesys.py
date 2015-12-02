import factoryStation
import operations.sendATCommand
import time

from operations.operationResult import opResultSuccess


class backupFilesys(operations.sendATCommand.sendATCommand):
  '''Backup modem file system'''
  def __init__(self, factoryStation, options):
    
    self.name = 'backupFileSys'
    self.description = backupFilesys.__doc__
    super(backupFilesys,self).__init__(factoryStation, options)
  
  def do(self):
    self.ATcmd = 'AT%MODE=1'
    super(backupFilesys,self).do()
    self.ATcmd = 'AT%IBACKUP'
    super(backupFilesys,self).do()
    time.sleep(2)
    self.ATcmd = 'AT%IFLIST=3'
    super(backupFilesys,self).do()
    return opResultSuccess()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True
  
  fs = factoryStation.factoryStation(None , testMode)       # default factoryStation object
  options = {'ATtool' : 'atcmd-itf' }
  fo = backupFilesys( fs, options )

  fo.postResult( fo.do() )
  
  
  