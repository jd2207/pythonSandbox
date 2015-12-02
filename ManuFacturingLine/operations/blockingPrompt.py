import factoryStation, factoryOperation
from userInterface import screen

from operations.operationResult import opResultAbort
from operations.operationResult import opResultSuccess

class blockingPrompt(factoryOperation.factoryOperation):    
  '''Provides a blocking user prompt'''

  def __init__(self, factoryStation, options):
    if type(self) is blockingPrompt:               # do not overwrite subclasses
      self.name = 'BlockingPrompt'
      self.description = blockingPrompt.__doc__
      self.selectable = False
    super(blockingPrompt, self).__init__(factoryStation, options)

  def initialize(self):
    self.readyPrompt = self.options['prompt'] + ' (or q to quit)'
    return True
  
  def do(self, serNum=None):
    resp = screen().prompt(self.readyPrompt)
    return opResultAbort() if resp.lower() == 'q' else opResultSuccess()

# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

  fs = factoryStation.factoryStation()                          # default factoryStation object
  fo = blockingPrompt( fs, { 'prompt' : 'Hit enter to continue'} )
  fo.postResult(fo.do())
  