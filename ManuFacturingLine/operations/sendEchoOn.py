import factoryStation
import operations.sendATCommand

class sendEchoOn(operations.sendATCommand.sendATCommand):
  '''Send echo ON to modem'''

  def __init__(self,factoryStation, options):
    self.name = 'sendEchoOn'
    self.description = sendEchoOn.__doc__
    self.ATcmd = 'ATE1'
    super(sendEchoOn,self).__init__(factoryStation, options)
  
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  
  fs = factoryStation.factoryStation(None, testMode)       # default factoryStation object
  fo = sendEchoOn( fs, {'ATtool' : 'atcmd-itf' } )
  fo.postResult( fo.do() )
  