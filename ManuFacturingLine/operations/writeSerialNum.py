import factoryStation
import operations.sendATCommand


class writeSerialNum(operations.sendATCommand.sendATCommand):
  '''Write Serial Number'''
  
  def __init__(self,factoryStation, options):
    self.name = 'writeSerialNum'
    self.description = writeSerialNum.__doc__
    super(writeSerialNum,self).__init__(factoryStation, options)

  def do(self):
    self.ATcmd = 'AT%IPARAM=' + self.factoryStation.serNum.getSN()
    return super(writeSerialNum,self).do()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  options = {'ATtool' : 'atcmd-itf'}
  fo = writeSerialNum( fs, options )
  fo.postResult( fo.do() )
  