import factoryStation, factoryOperation
from operations.operationResult import opResultUnexpected
from operations.operationResult import opResultSuccess
import utilities
import os.path
import argparse


class fwProgramming(factoryOperation.factoryOperation):
  '''Modem firmware programming via NEXUS'''
    
  def __init__(self, factoryStation, options):
    self.name = 'fwProgramming'
    self.description = fwProgramming.__doc__
    self.successKeyword = 'NAND1 programmed'
    self.adapter = factoryStation.adapter
    super(fwProgramming,self).__init__(factoryStation, options)
    
  def initialize(self):
    currFolderPath = os.path.abspath(os.curdir)
    srcPackageFolderPath = os.path.join(currFolderPath, self.options ['sourcePackage'])
    if not self.factoryStation.fileExists(srcPackageFolderPath, 'source package'):
      if not self.factoryStation.testMode: return False
    
    gangImage = os.path.join(currFolderPath,'gang_images',self.options ['gangImage'])
    if not self.factoryStation.fileExists(gangImage, 'gang image'):
      if not self.factoryStation.testMode: return False

    fs_push_all_path = os.path.join(srcPackageFolderPath, 'integration_tools', 'flash_programmer', 'bin', 'flash_prog.py')
    if self.factoryStation.fileExists(fs_push_all_path, 'fw programming tool'):
      if not self.factoryStation.testMode: return False
        
    self.args = [' python ', fs_push_all_path ]
    for arg in self.options['args'].split(' '):
      self.args.append(arg)
    self.args.append('-ada ' + self.adapter.name)
    self.args.append('-gangprog ' + gangImage)
    return True
  
  def processResult(self, errorCode, gotExpectedOutput, reply):
    if not errorCode == 0:
      if errorCode > 0:
        self.printToLog('FAIL:' + hex(errorCode), 0) 
      else:
        self.printToLog('FAIL:' + hex(errorCode&0xffffffff), 0) 
      return opResultUnexpected()
    
    return opResultSuccess()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='fwProgramming')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  args = parser.parse_args()    
  
# Factory Station and attributes
  fs = factoryStation.factoryStation( None, args.test)       # default factoryStation object 
  fs.adapter = utilities.debugAdapter()
  fs.sdkPath  = os.path.join(os.environ['ICERA_ROOT'], 'dxp-bare','examples','bringup_ice9040')
  
    # FW programming
  fo = fwProgramming(  fs, { 'args' : '-9040 -hwplat p2341',
                             'sourcePackage' : '',
                             'gangImage' : 'gang_image'
                            } )
  fo.postResult(fo.do ())     
  