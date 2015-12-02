import factoryConfig
import factoryStation
import factoryOperation
import utilities 
import operations.sendATCommand
import os.path
import argparse


class interfaceTest(factoryOperation.factoryOperation):
  '''Interface test tool'''
    
  def __init__(self,factoryStation,options):
    self.name = 'ifaceTest'
    self.description = interfaceTest.__doc__
    self.logFileName = os.path.join(factoryStation.logger.dirname(), utilities.dtStamp().logfile_tstamp() + self.name  + '.log')
    self.logs = [ self.logFileName ]
    self.arch = 'win32'
    super(interfaceTest,self).__init__(factoryStation,options)
        
  def initialize(self):
    curDir = os.path.abspath(os.curdir)
    self.tool = os.path.join(curDir, 'interfacetest', 'bin', 'interfacetest.exe')    
    if not self.factoryStation.fileExists(self.tool, 'Tool for operation: ' + self.name ):
      if not self.factoryStation.testMode: return False
    
    self.configPath = os.path.join(curDir, 'interfacetest', 'configuration')
    if not self.factoryStation.fileExists(self.configPath, 'Configuration path for ' + self.name):
      if not self.factoryStation.testMode: return False

  def do(self):
    sysConfig = self.options['sysConfig']
    prodDefs = self.options['prodDefs']
    icalCableLossXML = self.options['cableLoss']
    icalCableLossDivXML = self.options['cableLossDiv'] 
    prodName = self.factoryStation.productName

    modemPort = self.factoryStation.modemPort     
    self.args = [ self.tool, 
                  '--config_file=' + os.path.join(self.configPath, sysConfig),
                  '--product=' + prodName,
                  '--product_dir=' + os.path.join(self.configPath, prodDefs), 
                  '--cable_loss_file=' + os.path.join(self.configPath, icalCableLossXML),
                  '--cable_loss_div_file=' + os.path.join(self.configPath, icalCableLossDivXML), 
                  '--port=%s,115200,HARDWARE' % modemPort
                ]
    va = self.factoryStation.powerMeterVisaAddress
    if not va == '':
      self.args.append('--power_meter_visa_address=%s' % va )
    
    return super(interfaceTest,self).do()
    
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description='Interface test')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  parser.add_argument( '--sysConfig',      default = 'ical_system_config.xml',    help = 'Configuration file')
  parser.add_argument( '--prodDefs',       default = 'product_definitions',       help = 'Product Definitions file')
  parser.add_argument( '--cableLoss',      default = 'ical_cable_loss.xml',       help = 'Cable Loss (Main)')
  parser.add_argument( '--cableLossDiv',   default = 'ical_cable_loss.xml',       help = 'Cable Loss (Div)')
  args = parser.parse_args()    

# Debug Logger
  debugLog = utilities.logger (args.trace, '', args.verbosity)

# Factory Station and attributes
  fs = factoryStation.factoryStation(debugLog, args.test)       # default factoryStation object
  fs.productName = 'i500_1720_att'
  fs.powerMeterVisaAddress = '1234'
      
# Set options   
  if args.xml == None:            # set default values if no XML
    options = { 'sysConfig' : args.sysConfig,
                'prodDefs' : args.prodDefs,
                'cableLoss' : args.cableLoss,
                'cableLossDiv' : args.cableLossDiv ,
              }  
  else:
    debugLog.lineOut('Getting options from XML')
    options = factoryConfig.operationsParser().itemsFromXML( args.xml, 'operation' )['interfaceTest']['subItem']
  
# Create operation instance (also need an sendATCommand to retrieve COM port info)
  fo1 = operations.sendATCommand.sendATCommand( fs, {'ATtool' : 'atcmd-itf' } )
  fo2 = interfaceTest( fs, options )

# Perform the operation once
  fo1.do()
  fo2.postResult(fo2.do())
  fo2.collectLogs()
  
  