import factoryStation
import sys

class custom(factoryStation.factoryStation):
  '''Custom operations'''
  
  def __init__(self, logger=None, testMode=None):
    self.name = 'CUSTOM'
    self.desc = custom.__doc__
    super(custom,self).__init__(logger, testMode)

  def setAttribs(self,attribs):
    self.fuseImage = attribs ['fuseImage']
 
  def toolPathCheck(self):
    # Detect modem, get COM port
    if not self.detectModem():
      sys.exit()

    return True
