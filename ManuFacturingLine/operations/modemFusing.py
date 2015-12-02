import factoryStation
import operations.sendATCommand

from operations.operationResult import opResultUnexpected


class modemFusing(operations.sendATCommand.sendATCommand):
  '''Modem Fusing'''
  
  def __init__(self, factoryStation, options=None):
    self.name = 'modemFusing'
    self.description = modemFusing.__doc__
    super(modemFusing,self).__init__(factoryStation, options)

  def do(self):
    if not hasattr(self.factoryStation,'fuseImage'): 
      self.printToLog('WARNING: Fuse image not provided', 0)
      return opResultUnexpected()
    else:
      self.ATcmd = 'AT%IFUSEIMAGE=' + self.factoryStation.fuseImage
      return super(modemFusing,self).do()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  fs = factoryStation.factoryStation(None , testMode)                          # default factoryStation object
  fs.fuseImage = '0x0,0x0,0x0,0x0,0x4,0x0,0x0'
  
  fo = modemFusing( fs, {'ATtool' : 'atcmd-itf' } )
  
  fo.postResult( fo.do() )
  
