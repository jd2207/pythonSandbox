import factoryStation
import operations.sendATCommand


class unlockEngMode(operations.sendATCommand.sendATCommand):
  '''Unlock engineering mode'''

  def __init__(self,factoryStation, options):
    self.name = 'unlockEngMode'
    self.description = unlockEngMode.__doc__
    self.ATcmd = 'AT%IPWD="iceraempwd",0'
    super(unlockEngMode,self).__init__(factoryStation, options)

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  options = {'ATtool' : 'atcmd-itf'}
  fo = unlockEngMode( fs, options )
  fo.postResult( fo.do() )
