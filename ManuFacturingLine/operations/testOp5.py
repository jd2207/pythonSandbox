import factoryStation, factoryOperation
import utilities
import argparse

class testOp5(factoryOperation.factoryOperation): 
  '''Test operation where underlying process is another python module - override do()''' 

#Inner class to illustrate calling another python module from subProc()
  class abc(object):  
    def abc(self):
      return True, 'Some output text'
      
  def __init__(self, factoryStation, options=None):

# This class specific stuff
    self.name = 'TestOp5'
    self.description = testOp5.__doc__
    self.module = True

# Stuff common to all factoryProcesses
    super(testOp5,self).__init__(factoryStation, options)

  def subModule(self):          # override the parent (which assumes a underlying exe)
    return testOp5.abc().abc()

 
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description=testOp5.__doc__)
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    
  fs = factoryStation.factoryStation(None, args.test)       # default factoryStation object
  
  fo = testOp5(fs)
  fo.postResult(fo.do())
  fo.collectLogs()
