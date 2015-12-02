import factoryStation
import factoryOperation
import utilities
import smokeTst
import argparse


class smokeTest(factoryOperation.factoryOperation):
  '''Smoke Test for PSU control'''
  
  def __init__(self, factoryStation, options=None):
    self.name = 'smokeTest'
    self.description = smokeTest.__doc__
    self.readyPrompt = "Please disconnect debug adaptor. Press Enter when done."
    self.module = True
    super(smokeTest,self).__init__(factoryStation, options)

  def subModule(self):          
    try:
      out = smokeTst.smoketest()
      result, output = out[0], ' '.join(out[1:])
      return result, output
    except:
      return 0, 'FATAL ERROR: Problem executing subModule smokeTst.smoketest'


# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  
  # Command line arguments and defaults
  parser = argparse.ArgumentParser(description='Invoke smokeTest')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    

  debugLog = utilities.logger (args.trace, '', args.verbosity)

  fs = factoryStation.factoryStation()                          # default factoryStation object
  fo = smokeTest( fs )

  fo.postResult( fo.do() )

