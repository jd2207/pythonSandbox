import factoryConfig,factoryStation, factoryOperation
import utilities 
import argparse


class testOp3(factoryOperation.factoryOperation): 
  ''' Test operation where some args to the subprocess are hard-wired, 
      some are passed as options, some are attribs of the factoryStation'''
      
  '''If this operation is ran as "main", the options may be set by:
         - specifying an XML on the command line   
         - may be individually set on the command line 
         If no XML, and not set on command line, values 
           
      Other command line arguments specify debuglog, verbosity, test mode etc...
  ''' 

  def __init__(self, factoryStation, options=None):

# This class specific stuff
    self.name = 'TestOp3'
    self.description = testOp3.__doc__

# Stuff common to all factoryProcesses
    super(testOp3,self).__init__(factoryStation, options)

  def initialize(self):
    hardwired1 = 'hardwired1'
    hardwired2 = 'hardwired2'
    self.args = [ self.options['command'], 
                  self.options['arg1'], 
                  self.options['arg2'], 
                  self.options['arg3'], 
                  hardwired1,
                  hardwired2,
                  self.factoryStation.attrib1,
                  self.factoryStation.attrib2
                ]
    return True


if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description=testOp3.__doc__)
  utilities.cmdLineArgs(parser)                  # general args from parent class
  parser.add_argument( '--cmd', default='def_command', help='Command to run')
  parser.add_argument( '--arg1', default='def_arg1', help='Command arg1')
  parser.add_argument( '--arg2', default='def_arg2', help='Command arg2')
  parser.add_argument( '--arg3', default='def_arg3', help='Command arg3')
  args = parser.parse_args()    

# Create the logger  
  debugLog = utilities.logger (args.trace, '', args.verbosity)

# Create the factory station and attributes    
  fs = factoryStation.factoryStation(debugLog, args.test)       # default factoryStation object
  fs.attrib1 = 'attrib1'
  fs.attrib2 = 'attrib2'
  
# Set options   
  if args.xml == None:            # set default values if no XML
    options = { 'command' : args.cmd, 
                'arg1' : args.arg1,
                'arg2' : args.arg2,
                'arg3' : args.arg3
              }
  else:
    fs.printToLog('Getting options from XML', 5)
    options = factoryConfig.operationsParser().itemsFromXML( args.xml, 'operation' )['testOp3']['subItem']
  
# Instantiate the operation    
  fo = testOp3( fs, options )
  
# Perform the operation and collect the logs 
  fo.postResult(fo.do())
  fo.collectLogs()
  