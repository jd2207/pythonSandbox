import factoryStation
import operations.sendATCommand


class forceFactoryMode(operations.sendATCommand.sendATCommand):
  '''Force Factory Mode'''

  def __init__(self,factoryStation, options):
    self.ATcmd = 'AT%MODE=2'
    self.name = 'forceFactoryMode'
    self.description = forceFactoryMode.__doc__
    super(forceFactoryMode,self).__init__(factoryStation, options)


# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  fs = factoryStation.factoryStation(None , testMode)       # default factoryStation object
  options = {'ATtool' : 'atcmd-itf' }
  fo = forceFactoryMode( fs, options )
  fo.postResult(fo.do ())
  