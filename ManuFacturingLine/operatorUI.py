from factoryConfig import nvpnsParser
import userInterface 
import os.path
import utilities
import argparse, sys 

__version__ = '2014-00-00'

def parseArgs( ):
    
  desc = "This program will provide a menu driven interface for manufacturing functions. Functions will be presented based the selected NVPN and factoryStation"
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-v', '--version', action='version', version="Version: " + __version__)
  parser.add_argument( '--verbosity', type=int, default=0, help='Set the debug level')
  parser.add_argument( '--test', default=False, action='store_true', help='Run in test mode')
  parser.add_argument( '--debug', default=False, action='store_true', help='Run in debug mode')
  parser.add_argument( '--logpath', default='log', help='Path to trace log')
  parser.add_argument( '--nvpn', default=None, help='NVPN value')
  parser.add_argument( '--station', default=None, help='Factory station')
  parser.add_argument( '-x', '--xml', default='factoryFlow.xml', help='XML configuration file name')
  parser.add_argument( '--cfgp', default='example', help='Path to XML configuration')
  args = parser.parse_args()    
  return args


if __name__ == '__main__':

# ------------------------------------------------------
# Get params from args    
# ------------------------------------------------------
  args = parseArgs() 
  verbosity = args.verbosity
  testMode = args.test
  debugMode = args.debug
  logpath = args.logpath
  nvpnID = args.nvpn
  stationID = args.station
  logpath = args.logpath
  xml = os.path.join(args.cfgp, args.xml)
       
  traceLog = utilities.logger (logpath,'',verbosity) 
  s = utilities.screen()

  traceLog.lineOut('Operator log\n'+
                   'CFG: Version: ' + __version__+ '\n'
                   'CFG: Verbosity: ' + str(verbosity) + '\n'
                   'CFG: Test Mode: ' + str(testMode) + '\n'
                   'CFG: Debug Mode: ' + str(debugMode) + '\n'
                   'CFG: Log: ' + traceLog.logname + '\n'
                   'CFG: Config XML: ' + xml + '\n'
                   'CFG: NVPN: ' + str(args.nvpn) + '\n'
                   'CFG: Factory Station: ' + str(args.station) + '\n'
                  )
  
# ------------------------------------------------------
#  Use configuration XML to choose an NPVN and Station 
# ------------------------------------------------------

  title = "NVidia Icera Manufacturing Tools" 
    
# Parse entire factory configuration 
  nvpns = nvpnsParser().itemsFromXML( xml, 'nvpn' )

# -------------------------------------------------------
# User selects an NVPN (if not set by args)
# -------------------------------------------------------
  if nvpnID == None:                    # Select the NVPN using the 'menu' class
    m = userInterface.menu(s,title,'NVPN')
    m.appendFromDict(nvpns)
    nvpnID = m.select()['id']
  else:                                 # Still check that the nvpn provided by command line matches one of those in the XML 
    if not (nvpnID in nvpns):
      traceLog.lineOut('FATAL: nvpn provided (%s) does not exist' % nvpnID)
      sys.exit()
    
  traceLog.lineOut('Chosen NVPV = ' + nvpnID)
  title += '\n' + 'NVPN: ' + nvpnID
  
  
# ----------------------------------------------------------
# User selects a station for this NVPN (if not set by args)
# ----------------------------------------------------------
  stations = nvpns [ nvpnID ] ['subItem'] 
  if stationID == None:                   # Given the nvpn, now select the station using the 'menu' class
    m = userInterface.menu(s,title,'Station')
    m.appendFromDict(stations)
    stationID = m.select()['id']
  else:
    if not (stationID in stations):
      traceLog.lineOut('FATAL: station provided (%s) does not exist for nvpn: %s' % (stationID, nvpnID))
      sys.exit()
  
  traceLog.lineOut('Chosen Station = ' + stationID)
  title += '\n' + 'Station: ' + stationID
    
# -------------------------------------------------------------
# From the selected station, create a factoryStation object, 
#   and populate with operations based on the XML config
# -------------------------------------------------------------
  
  
  module = getattr( __import__('stations.' + stationID), stationID)
  fs = getattr( module, stationID) ( traceLog, testMode )     # stationID is the name of a factoryStation class
  fs.productName = nvpns [ nvpnID ] ['productName'] # Product name associated with the NVPN
  fs.fuseImage = nvpns [ nvpnID ] ['fuseImage'] # Product name associated with the NVPN
  fs.addOperationsFromDict( stations [stationID ] ['subItem'] )   # Use the config XML data to create and add all station operations 
  if not debugMode:
    fs.deviceLoop()       # cycle of operations until user quit
    
  else:                   # all that follows is debugMode - allow selection of individual operations 
  # -------------------------------------------------------------------------------------------------
# For the given NVPN-Station combo, create the station operations menu (and allow "ALL" option)
# -------------------------------------------------------------------------------------------------
    s.clear()
    m = userInterface.menu(s,title,'operation')
    m.allowAll()
    for op in fs.operations:
      if op.selectable: m.append(op.name, op.description, op)    # dont want some ops (like prompt, PSU control) to appear in menu 

# ------------------------------------------------------------        
#   Main operational loop for the chosen station 
# ------------------------------------------------------------
    while (True):
      x = m.select()        # Choose the operation (may be a menu item, a list of menu item (i.e.'ALL') or quit    
      queue = []
      if isinstance(x,list): 
        for i in x:
          queue.append (i['item'])
      else:                           # list is only a single operation    
        queue.append( x['item'])

      for i in queue:
        traceLog.lineOut('Operation '+ i.name + ' added to processing queue')

# ---------------------------------------
#   Loop for each device   
# ---------------------------------------
      while (True):
        
# Perform all chosen operations on the device (with that serial number)
        traceLog.lineOut('Starting the chosen operation(s)', 4)
        for op in queue:
          op.do()
          op.collectLogs()
          traceLog.lineOut('Finished all operations', 3)

        if not s.promptYN('Ready to process next device? (or enter "N" to quit)',True): 
          traceLog.lineOut('User quit to operations menu')
          s.clear()
          break  

