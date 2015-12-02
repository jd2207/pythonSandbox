import factoryStation
import factoryOperation
import sys, time
import utilities

from operations.operationResult import opResultSuccess
from operations.operationResult import opResultUnexpected


class sendATCommand(factoryOperation.factoryOperation):
  '''Send an AT command'''

  def __init__(self, factoryStation, options):
  
  # Set default values only if NOT set by subclasses
    if not hasattr(self, 'ATcmd'): self.ATcmd = 'AT'
    if not hasattr(self, 'attempts'): self.attempts = 1
    
    if type(self) is sendATCommand:               # do not overwrite subclasses
      self.name = 'SendATCommand'
      self.description = sendATCommand.__doc__
    super(sendATCommand,self).__init__(factoryStation, options)

  def initialize(self):
    self.successKeyword = 'OK'
    self.ATtool = self.options['ATtool']
    if sys.platform == 'win32': self.ATtool += '.exe' 
    
    if not utilities.fileOnPath(self.ATtool):
      self.printToLog('ERROR: AT tool "%s" NOT found on path' % self.ATtool, 0)
      return False
    else:
      self.printToLog('AT tool "%s" found on path' % self.ATtool, 5)
      return True
  
  def ready(self):
    if not self.detectModem():
      self.readyPrompt = 'ERROR: Modem detection problem.'
      return False
    else:
      return True

  def do(self):            # might not know full AT command until "do()" time
    self.args = [ self.ATtool, self.ATcmd ]
    for i in range(self.attempts):
      self.printToLog('Retrying...', 3) if not (i == 0) else None
      
      result = super(sendATCommand,self).do()
      if not isinstance(result, opResultSuccess):
        time.sleep(5)
      else:
        return result
   
    return opResultUnexpected()
   
  def processResult(self, errorCode, atReply):                     # if bad result, do retries    
    result = super(sendATCommand,self).processResult(errorCode, atReply)
    if isinstance(result, opResultSuccess) and atReply.find(self.ATcmd) >= 0:
      return result
    else:
      return opResultUnexpected()

  def detectModem(self):  #Modem detection check; if detected, it updates the factory Station COM port
    ATresp = '(Serial) '
    waitTime = 30
    self.modemPort = None
            
    errorCode, text = utilities.subProc(self.ATtool)
    if not text.find(ATresp) >= 0:
      self.printToLog('FAIL: Cannot detect modem. Waiting '+str(waitTime)+ ' seconds before re-trying ... ', 0)
      time.sleep(waitTime)
      errorCode, text = utilities.subProc(self.ATtool)
      if not text.find(ATresp) >= 0:
        self.printToLog('FAIL: Modem is not available ', 0)
        return False

    self.printToLog('Modem successfully detected', 2)

    if sys.platform == 'win32':       # for windows, determine the COM port
      strlist = text.split(' ')
      for value in strlist:
        if value.find('COM') >= 0:
          self.printToLog('Modem is at COM port %s' % value, 5)
          self.factoryStation.modemPort = value
          return True
                  
    self.printToLog('WARNING: Cannot determine COM port', 0)
    if self.factoryStation.testMode: self.factoryStation.modemPort = 'COM999'
    return True

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  testMode = True
  fs = factoryStation.factoryStation(None, testMode)                          # default factoryStation object
  
  fo = sendATCommand( fs, {'ATtool' : 'atcmd-itf' } )
  fo.postResult(fo.do())
