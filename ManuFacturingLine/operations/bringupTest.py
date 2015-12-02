import factoryStation
import factoryOperation
from operations.operationResult import opResultSuccess
import os.path
import utilities
import argparse


class bringupTest(factoryOperation.factoryOperation):
  '''Launch bringup tests'''

  def __init__(self, factoryStation, options):
    self.name = 'bringUpTests'
    self.description = bringupTest.__doc__
    self.successKeyword = 'ALL TESTS PASSED'
    super(bringupTest,self).__init__(factoryStation, options)
    
  def initialize(self):
    if not self.factoryStation.fileExists( self.factoryStation.sdkPath, 'SDK path'):
      if not self.factoryStation.testMode: return False

    adapterName = self.factoryStation.adapter.name
    self.args = []
    for arg in self.options['commandLine'].split(' '):
      self.args.append(arg)
    
    cmd = self.args[0]
    if not self.factoryStation.fileOnPath( cmd):
      if not self.factoryStation.testMode: return False
    
    self.args.append('-ada '+ adapterName)
    return True

  def do(self):
    backupCurdir = os.path.abspath(os.path.curdir)
    os.chdir(self.factoryStation.sdkPath)
    self.printToLog('Current directory changed to SDK path: %s' % self.factoryStation.sdkPath, 3)
    super(bringupTest,self).do()
    os.chdir(backupCurdir)
    self.printToLog('Current directory changed back to: ' + backupCurdir, 3)
    return opResultSuccess()
 
  
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Interface test')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    
  
# Factory Station and attributes
  fs = factoryStation.factoryStation( None, args.test)       # default factoryStation object
  fs.adapter = utilities.debugAdapter()
  fs.sdkPath = os.path.join(os.environ['ICERA_ROOT'], 'dxp-bare','examples','bringup_ice9040')
  
# Perform the operation once
  fo = bringupTest( fs, { 'commandLine' : 'BRINGUP_ICE9040_DDR_TAL.bat -warmboottest' } )
  fo.postResult( fo.do() )     
  