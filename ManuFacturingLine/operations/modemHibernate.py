import factoryStation
import operations.sendATCommand


class modemHibernate(operations.sendATCommand.sendATCommand):
  '''Modem Hibernate Enable/Disable'''
  
  def __init__(self,factoryStation, options):
    self.name = 'modemHibernate'
    self.description = modemHibernate.__doc__
    disableFlag = ( 1 if options ['disable'] == 'ON' else 0 )
    self.ATcmd = 'AT%%IHIBD=%d,1' % disableFlag
    super(modemHibernate,self).__init__(factoryStation, options)

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  testMode = True
  
  fs = factoryStation.factoryStation(None , testMode)                          # default factoryStation object
  options = {'ATtool' : 'atcmd-itf', 'disable' : 'ON' }
  fo = modemHibernate( fs, options )
  fo.postResult( fo.do() )
  
  options = {'ATtool' : 'atcmd-itf', 'disable' : 'OFF' }
  fo = modemHibernate( fs, options )

  fo.postResult( fo.do() )
  