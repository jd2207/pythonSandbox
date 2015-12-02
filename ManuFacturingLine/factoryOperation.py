import utilities, sys
from userInterface import screen 
from os.path import join, dirname

from operations.operationResult import opResultTestMode
from operations.operationResult import opResultSuccess
from operations.operationResult import opResultUnexpected
from operations.operationResult import opResultSubprocessFail


class factoryOperation(object):
    
  def __init__(self, factoryStation, options=None):
    
    self.factoryStation = factoryStation
    self.logger = factoryStation.logger
    self.options = options
    self.serialNum = utilities.serialNumber()

    # Force defaults for items which usually overridden by subclasses
    if not hasattr(self,'name'): self.name = 'NO NAME'
    if not hasattr(self,'description'): self.description = ''
    if not hasattr(self,'successKeyword'): self.successKeyword = ''
    if not hasattr(self,'readyPrompt'): self.readyPrompt = None
    if not hasattr(self,'logs'): self.logs = []
    if not hasattr(self,'args'): self.args = []
    if not hasattr(self,'module'): self.module = False
    if not hasattr(self,'arch'): self.arch = None
    if not hasattr(self,'selectable'): self.selectable = True     # set to false only for those ops which UI does not allow on menu 
    
    # Check if operation can run on this system
    if not self.arch == None:
      if not sys.platform == self.arch:
          self.printToLog("FATAL: Operation %s must be run on a %s system" % (self.name, self.arch), 0)
          sys.exit() if not self.factoryStation.testMode else None
    
    if self.initialize():
      self.printToLog("Operation %s initialized" % self.name, 5)
    else:
      self.printToLog("FATAL: Operation %s failed initialization check" % self.name, 0)
      sys.exit() if not self.factoryStation.testMode else None

  def initialize(self):        
# Overridden by subclasses. 
# Used to process self.options (parameters which are factoryStation independent), and also takes account of factory station dependent values
# Also checks if necessary tools, paths etc specific to this operation are available  
    self.printToLog("WARNING: factory operation %s has no initialize() method" % self.name, 5)
    return True
        
  def do(self):

# Ready check loop
    reTry = True
    while not self.ready() and reTry:                               
      if not (self.readyPrompt == None):
        reTry = screen().promptYN(self.readyPrompt + ' Retry?')

# Run the underlying process or module    
    reply = ''
    if self.module:                           # for operations which call a python module  
      if not self.factoryStation.testMode:
        errorCode, reply = self.subModule()
      else:
        self.printToLog('<TEST MODE>: Dummy call to module %s' % self.name , 0)
    else:                                     # for operations which use a subprocess
      if len(self.args) == 0:
        self.printToLog('FATAL: No command or arguments supplied for the subprocess of operation: %s' % self.name, 0)
        sys.exit() if not self.factoryStation.testMode else None
      else:
        errorCode, reply = utilities.subProc(self.args, self.factoryStation.testMode)    # run the subprocess

    self.printToLog(reply, 5)   # Record the output of the subprocess

# Derive a result object 
    if not self.factoryStation.testMode: 
      return self.processResult(errorCode, reply) 
    else:
      return opResultTestMode()
    
  def ready(self):              #  may be overridden by operations that need a ready check
    return True
    
  def collectLogs(self, dest=None):
# Creates a new archive (tar,7z etc) file, in same folder as main debug log.
# The archive gathers all logs associated with this factory Operation

    self.printToLog ('Collecting logs', 3)

    fName = utilities.dtStamp().logfile_tstamp() + '_' + self.name + '_' + self.serialNum.getSN() 
    dirName = '.' if self.logger == None else dirname(self.logger.logname) 
    archiveName = join ( dirName, fName )
    
    if len(self.logs) > 0 :
      utilities.logCompressor7z(archiveName,self.logs)
      self.printToLog ('Logs bundled to '+archiveName, 3)
    else:
      self.printToLog ('WARNING: The operation specified no logs for collection', 1)
    
  def processResult(self, errorCode, text=''):   
    '''Return a operationResult object'''                  
    result = opResultSuccess() 
    if errorCode == -1:
      result = opResultSubprocessFail() 
    if not text.find(self.successKeyword) >= 0:
      result = opResultUnexpected()

    return result

  def postResult(self, result):
    self.printToLog( 'RESULT: %s (%i)' % (result.desc, result.code), 0 )

  def printToLog(self, text, verbosity=0):                 # For printing to a log 
    output = "[ %s ][ %s ] %s" % (self.factoryStation.serNum.getSN(), self.name, text)
    if self.logger == None:          
      print output
    else: 
      self.logger.lineOut ( output, verbosity  )
