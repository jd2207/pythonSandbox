import factoryStation, factoryOperation
import utilities
import argparse

class testOp6(factoryOperation.factoryOperation): 
  '''Test operation where underlying process is very simple action - override do()''' 

  def __init__(self, factoryStation, options=None):

# This class specific stuff
    self.name = 'TestOp6'
    self.description = testOp6.__doc__

# Stuff common to all factoryProcesses
    super(testOp6,self).__init__(factoryStation, options)
    self.txt = "Hello, World!"

  def do(self):          
    self.args = ['fakeCommand']
    self.printToLog(self.txt)
    return super(testOp6,self).do()

 
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description=testOp6.__doc__)
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    

  fs = factoryStation.factoryStation(None, args.test)       # default factoryStation object
  fo = testOp6(fs)
  fo.postResult(fo.do())
  fo.collectLogs()
