import factoryStation, factoryOperation
import utilities
import argparse


class testOp4(factoryOperation.factoryOperation): 
  '''Test operation where command and args are from one option string passed''' 

  def __init__(self, factoryStation, options=None):

# This class specific stuff
    self.name = 'TestOp4'
    self.description = testOp4.__doc__

# Stuff common to all factoryProcesses
    super(testOp4,self).__init__(factoryStation, options)

  def initialize(self):
    self.args = []
    for arg in self.options['subprocess'].split(' '):
      self.args.append(arg)

    return True

 
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description=testOp4.__doc__)
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    

  fs = factoryStation.factoryStation(None, args.test)       # default factoryStation object
  options = { 'subprocess' : 'command arg1 arg2 arg3 arg4' }
  
  fo = testOp4( fs, options )
  fo.postResult(fo.do())
  fo.collectLogs()

