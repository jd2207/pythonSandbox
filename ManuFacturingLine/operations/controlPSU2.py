import factoryStation
import factoryOperation
import utilities
import argparse


class controlPSU2(factoryOperation.factoryOperation):
  ''' To set PSU on or off (RFCV version)'''

  def __init__(self, factoryStation, options):
    self.name = 'controlPSU2'
    self.description = controlPSU2.__doc__
    self.module = True
    self.onOff = options['onOff']
    self.selectable = False
    super(controlPSU2,self).__init__(factoryStation, options)
    self.psu = self.factoryStation.psu

  def subModule(self):
    if not self.factoryStation.testMode:
      if self.onOff=='ON':
        self.psu.PSUOn_P6V()
      if self.onOff=='ICAL':
        self.psu.PSUOn_P6V_iCal()
      if self.onOff=='OFF':
        self.psu.PSUOff()
      return True, self.psu.getLog()
    else:
      return True, "<TEST MODE>: PSU set to " + self.onOff + " - no actual call to psu module"


# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description='PSU Control')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  parser.add_argument( '--onOff', default='OFF', help='ON, OFF or ICAL')
  args = parser.parse_args()    

# Create the logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)

# Create the factory station and attributes    
  fs = factoryStation.factoryStation(debugLog, args.test)       # default factoryStation object
  fs.psu = None
    
# Set options   
  options = { 'onOff' : args.onOff }
  
# Instantiate the operation    
  fo = controlPSU2( fs, options )
  
# Perform the operation and collect the logs 
  fo.postResults(fo.do ())
  fo.collectLogs()
  