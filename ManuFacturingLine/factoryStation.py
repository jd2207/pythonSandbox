import sys, utilities, os

from operations.operationResult import opResultAbort
from operations.operationResult import opResultSuccess


# Outcomes for a given device
BIN_SUCCESS = (0, "Success") 
BIN_FAIL = (1, "Fail")

class factoryStation(object):
  '''Abstract parent class of all factoryStations'''
      
  def __init__ (self, logger=None, testMode=False):

    self.testMode = testMode

# Set defaults if subclasses fail to specify these
    if not hasattr(self,'name'): self.name = 'DUMMY'            
    if not hasattr(self,'desc'): self.desc = 'NO DESCRIPTION'
    if not hasattr(self,'operations'): self.operations = []

# Check if the host has been commissioned for 'this' station 
    try:
      hostStation = os.environ['ICERA_FACTORY_STATION']
    except KeyError:
      print 'FATAL: Installation error - no environment var "ICERA_FACTORY_STATION"'
      sys.exit() if not testMode else None
    else: 
      if not hostStation == self.name:
        print 'FATAL: This station has been configured for %s, not for %s' % (hostStation, self.name) 
        sys.exit() if not testMode else None
        
# A default serialNumber
    self.serNum = utilities.serialNumber() 

# Warning if not debug log specified
    self.logger = logger
    if self.logger == None:
      utilities.logWarning()
        
    self.printToLog("Factory station initialization ...", 5) 
    if self.testMode: self.printToLog(" *** TEST MODE ENABLED *** - FATAL errors will be ignored, subprocesses will not be called", 0) 
        
    if not self.toolPathCheck():
      self.printToLog("FATAL: Tools check failed", 0)
      sys.exit() if not self.testMode else None
    else:
      self.printToLog('Tools look good', 5)
       
  def toolPathCheck(self):                    # Overridden by subclasses
    return True 

  def setProduct(self, prodName=None):               
    self.productName = prodName if not prodName==None else 'prodName'

  def setRadioTester(self):
    rt = utilities.radioTester()
    if (rt.type == None):
      self.printToLog('ERROR: Could not create radioTester object', 0)
      self.radioTester = None
      return False
    else:
      self.radioTester = rt
      self.printToLog('This host assumes a %s radio tester with visa address: %s' % (rt.type, rt.visaAddress), 5)
      return True

  def addOperationsFromDict(self,d):      # Sets up the **ordered** list of operations from the unordered dictionary
    temp = {}
    for i in d.iterkeys():
      opClassName = i
      order = int(d[i]['order'])
      opOptions = d[i]['subItem']
        
# Create an instance of the class associated with the operation
# (Class called opClassName lives in a file/module called opClassName under the operations package)
      module = getattr( __import__('operations.' + opClassName), opClassName)
      opClass = getattr( module, opClassName)
      temp[order] = opClass ( self, opOptions)  
      self.printToLog("Created new instance of %s" % opClassName, 5)  

    for i in sorted(temp): 
      self.operations.append(temp[i])

  
  def deviceLoop(self, collectLogs=False):
    '''Perform a sequencial loop on all defined operations''' 

# Initialize stats      
    self.passes = 0
    self.fails = 0
    self.devices = 0 
    self.inconclusives = 0 

    while (True):
      self.devices += 1
      overall = True
      for op in self.operations:
        result = op.do( ) 
        op.collectLogs() if collectLogs else None  #  - optionally using a serial number, optionally collect logs'''
      
        if isinstance(result, opResultAbort):
          self.printToLog('User chose to quit at serial number %s' % self.serNum.getSN(), 0)
          sys.exit()
        
        if not isinstance(result, opResultSuccess) and not self.testMode: 
          overall = False
          break       # Abort this device and start over on the next device
        
        op.postResult(result)

      self.accumulateStats(overall)
  
  def printToLog(self, text, verbosity=0):                 # For printing to a log 
    output = '[ %s ] %s ' % (self.name, text)
    if self.logger == None:          
      print output
    else: 
      self.logger.lineOut ( output, verbosity  )
      self.logger.flush()

  def accumulateStats(self, overall): 
    '''Accumulate the stats of a given run'''
      
    if not self.testMode:
      if overall: 
        self.passes += 1
      else:
        self.fails += 1
    else:
      self.inconclusives += 1
    
    self.printToLog( 
        ('\n ---------------------------------------------------------------------------------\n' +
           '          OVERALL RESULT SO FAR :  %i DEVICES (%i PASS, %i FAIL, %i INCONCLUSIVE) \n' +
           ' ---------------------------------------------------------------------------------\n') % 
                     (self.devices, self.passes, self.fails, self.inconclusives) )   

  def fileOnPath(self, exe):                               # wrapper on utilities.fileOnPath
    if not utilities.fileOnPath(exe):
      self.printToLog('Command %s NOT found on path' % exe, 5)
      return False
    else:
      self.printToLog('Command %s found on path' % exe, 5)
      return True

  def fileExists(self, filename, text=''):                               # wrapper on utilities.fileOnPath
    if not os.path.exists(filename):
      self.printToLog('FATAL: Cannot find %s %s' % (text, filename), 0)
      return False
    else:
      self.printToLog('%s exists: %s' % (text, filename) , 5)
      return True
    
    