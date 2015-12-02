import factoryStation
import utilities, argparse

from operations.blockingPrompt import blockingPrompt
from operations.testOp1 import testOp1
from operations.testOp2 import testOp2
from operations.testOp3 import testOp3
from operations.testOp4 import testOp4
from operations.testOp5 import testOp5
from operations.testOp6 import testOp6

class testStation(factoryStation.factoryStation):
  
  def __init__(self, logger=None, testMode=None):
    self.name = 'testStation'
    self.desc = testStation.__doc__
    self.attrib1 = 'attrib1'
    self.attrib2 = 'attrib2'
    super(testStation,self).__init__(logger, testMode)
        
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='simple test station')
  utilities.cmdLineArgs(parser)                  # general args 
  args = parser.parse_args()    

# Debug logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)

  fs = testStation( None, args.test)       

  fs.operations.append ( blockingPrompt( fs, { 'prompt' : 'Hit a key when ready.' }))
  fs.operations.append ( testOp1( fs ))
  fs.operations.append ( testOp2( fs, { 'command' : 'ls', 'option1' : '-al'} ))

  fs.attrib1 = 'attrib1'
  fs.attrib2 = 'attrib2'
  fs.operations.append ( testOp3( fs, { 'command' : 'command', 
                                        'arg1' : 'arg1',
                                        'arg2' : 'arg2',
                                        'arg3' : 'arg3'
                                       }))
  fs.operations.append ( testOp4( fs, { 'subprocess' : 'command arg1 arg2 arg3 arg4' }))
  fs.operations.append ( testOp5( fs ))
  fs.operations.append ( testOp6( fs ))
  fs.deviceLoop()               # loop for multiple devices
  
  
